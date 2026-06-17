"""
Сервис для управления подписками и лимитами
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.database import DatabaseManager
from telegram_bot.models import User, Subscription, Payment
from config import settings

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Сервис для управления подписками"""
    
    SUBSCRIPTION_PLANS = {
        "free": {
            "name": "FREE",
            "name_kz": "Тегін",
            "price": 0,
            "currency": "KZT",
            "daily_limit": 3,
            "features": [
                "3 запроса в день",
                "Базовые функции",
                "Карта дня",
                "Да/Нет расклады"
            ]
        },
        "premium": {
            "name": "PREMIUM",
            "name_kz": "Премиум",
            "price": 2500,
            "currency": "KZT",
            "daily_limit": -1,  # Безлимит
            "features": [
                "Безлимит запросов",
                "Все функции",
                "PDF-отчёты",
                "Приоритетная поддержка"
            ]
        },
        "vip": {
            "name": "VIP",
            "name_kz": "VIP",
            "price": 15000,
            "currency": "KZT",
            "daily_limit": -1,  # Безлимит
            "features": [
                "Живая консультация",
                "Персональный прогноз",
                "Закрытое комьюнити",
                "Эксклюзивные материалы"
            ]
        }
    }
    
    @staticmethod
    async def get_user_subscription(user_id: int) -> Dict[str, Any]:
        """Получить информацию о подписке пользователя"""
        async with DatabaseManager.get_session() as session:
            try:
                # Получить пользователя
                result = await session.execute(
                    select(User).where(User.telegram_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    return {"error": "Пользователь не найден"}
                
                # Получить активную подписку
                result = await session.execute(
                    select(Subscription)
                    .where(
                        and_(
                            Subscription.user_id == user.id,
                            Subscription.is_active == True,
                            Subscription.end_date > datetime.now()
                        )
                    )
                )
                subscription = result.scalar_one_or_none()
                
                # Определить текущий план
                if subscription:
                    plan_type = subscription.plan_type
                else:
                    plan_type = "free"
                
                plan_info = SubscriptionService.SUBSCRIPTION_PLANS.get(plan_type, {})
                
                return {
                    "user_id": user.id,
                    "plan_type": plan_type,
                    "plan_name": plan_info.get("name", "Unknown"),
                    "plan_name_kz": plan_info.get("name_kz", "Белгісіз"),
                    "daily_limit": plan_info.get("daily_limit", 3),
                    "features": plan_info.get("features", []),
                    "is_active": subscription is not None,
                    "expires_at": subscription.end_date if subscription else None,
                    "daily_requests": user.daily_requests,
                    "total_requests": user.total_requests
                }
                
            except Exception as e:
                logger.error(f"Ошибка при получении подписки: {e}")
                return {"error": "Ошибка при получении подписки"}
    
    @staticmethod
    async def can_make_request(user_id: int) -> Dict[str, Any]:
        """Проверить, может ли пользователь сделать запрос"""
        subscription_info = await SubscriptionService.get_user_subscription(user_id)
        
        if "error" in subscription_info:
            return subscription_info
        
        # Проверить лимиты
        daily_limit = subscription_info["daily_limit"]
        daily_requests = subscription_info["daily_requests"]
        
        if daily_limit == -1:  # Безлимит
            return {"can_request": True, "reason": "unlimited"}
        
        if daily_requests >= daily_limit:
            return {
                "can_request": False,
                "reason": "daily_limit_exceeded",
                "daily_requests": daily_requests,
                "daily_limit": daily_limit
            }
        
        return {"can_request": True, "reason": "within_limit"}
    
    @staticmethod
    async def increment_request_count(user_id: int) -> bool:
        """Увеличить счётчик запросов пользователя"""
        async with DatabaseManager.get_session() as session:
            try:
                # Получить пользователя
                result = await session.execute(
                    select(User).where(User.telegram_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    return False
                
                # Обновить счётчики
                await session.execute(
                    update(User)
                    .where(User.id == user.id)
                    .values(
                        daily_requests=User.daily_requests + 1,
                        total_requests=User.total_requests + 1,
                        last_activity=datetime.now()
                    )
                )
                await session.commit()
                return True
                
            except Exception as e:
                logger.error(f"Ошибка при увеличении счётчика запросов: {e}")
                await session.rollback()
                return False
    
    @staticmethod
    async def reset_daily_limits() -> int:
        """Сбросить дневные лимиты всех пользователей"""
        async with DatabaseManager.get_session() as session:
            try:
                result = await session.execute(
                    update(User)
                    .values(daily_requests=0)
                )
                await session.commit()
                return result.rowcount
                
            except Exception as e:
                logger.error(f"Ошибка при сбросе дневных лимитов: {e}")
                await session.rollback()
                return 0
    
    @staticmethod
    async def create_subscription(user_id: int, plan_type: str, 
                                payment_id: Optional[int] = None) -> Dict[str, Any]:
        """Создать подписку для пользователя"""
        async with DatabaseManager.get_session() as session:
            try:
                # Получить пользователя
                result = await session.execute(
                    select(User).where(User.telegram_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    return {"error": "Пользователь не найден"}
                
                # Проверить план
                if plan_type not in SubscriptionService.SUBSCRIPTION_PLANS:
                    return {"error": "Неверный тип подписки"}
                
                plan_info = SubscriptionService.SUBSCRIPTION_PLANS[plan_type]
                
                # Деактивировать старые подписки
                await session.execute(
                    update(Subscription)
                    .where(
                        and_(
                            Subscription.user_id == user.id,
                            Subscription.is_active == True
                        )
                    )
                    .values(is_active=False)
                )
                
                # Создать новую подписку
                start_date = datetime.now()
                end_date = start_date + timedelta(days=30)  # 30 дней
                
                subscription = Subscription(
                    user_id=user.id,
                    plan_type=plan_type,
                    price=plan_info["price"],
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True,
                    auto_renew=True,
                    payment_id=payment_id
                )
                
                session.add(subscription)
                
                # Обновить тип подписки пользователя
                await session.execute(
                    update(User)
                    .where(User.id == user.id)
                    .values(
                        subscription_type=plan_type,
                        subscription_start=start_date,
                        subscription_end=end_date,
                        daily_limit=plan_info["daily_limit"]
                    )
                )
                
                await session.commit()
                
                return {
                    "success": True,
                    "subscription_id": subscription.id,
                    "plan_type": plan_type,
                    "start_date": start_date,
                    "end_date": end_date
                }
                
            except Exception as e:
                logger.error(f"Ошибка при создании подписки: {e}")
                await session.rollback()
                return {"error": "Ошибка при создании подписки"}
    
    @staticmethod
    async def cancel_subscription(user_id: int) -> Dict[str, Any]:
        """Отменить подписку пользователя"""
        async with DatabaseManager.get_session() as session:
            try:
                # Получить пользователя
                result = await session.execute(
                    select(User).where(User.telegram_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    return {"error": "Пользователь не найден"}
                
                # Деактивировать активные подписки
                result = await session.execute(
                    update(Subscription)
                    .where(
                        and_(
                            Subscription.user_id == user.id,
                            Subscription.is_active == True
                        )
                    )
                    .values(is_active=False, auto_renew=False)
                )
                
                # Обновить тип подписки пользователя
                await session.execute(
                    update(User)
                    .where(User.id == user.id)
                    .values(
                        subscription_type="free",
                        subscription_start=None,
                        subscription_end=None,
                        daily_limit=3
                    )
                )
                
                await session.commit()
                
                return {
                    "success": True,
                    "message": "Подписка отменена"
                }
                
            except Exception as e:
                logger.error(f"Ошибка при отмене подписки: {e}")
                await session.rollback()
                return {"error": "Ошибка при отмене подписки"}
    
    @staticmethod
    async def get_subscription_stats() -> Dict[str, Any]:
        """Получить статистику подписок"""
        async with DatabaseManager.get_session() as session:
            try:
                # Общее количество пользователей
                result = await session.execute(select(User))
                total_users = len(result.scalars().all())
                
                # Пользователи по типам подписок
                result = await session.execute(
                    select(User.subscription_type, User.id)
                )
                users_by_type = {}
                for subscription_type, user_id in result:
                    users_by_type[subscription_type] = users_by_type.get(subscription_type, 0) + 1
                
                # Активные подписки
                result = await session.execute(
                    select(Subscription)
                    .where(
                        and_(
                            Subscription.is_active == True,
                            Subscription.end_date > datetime.now()
                        )
                    )
                )
                active_subscriptions = len(result.scalars().all())
                
                # Доходы за месяц
                month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                result = await session.execute(
                    select(Payment.amount)
                    .where(
                        and_(
                            Payment.status == "completed",
                            Payment.created_at >= month_start
                        )
                    )
                )
                monthly_revenue = sum(amount for amount in result.scalars().all())
                
                return {
                    "total_users": total_users,
                    "users_by_type": users_by_type,
                    "active_subscriptions": active_subscriptions,
                    "monthly_revenue": monthly_revenue
                }
                
            except Exception as e:
                logger.error(f"Ошибка при получении статистики подписок: {e}")
                return {"error": "Ошибка при получении статистики"}
    
    @staticmethod
    async def check_expired_subscriptions() -> int:
        """Проверить и деактивировать истёкшие подписки"""
        async with DatabaseManager.get_session() as session:
            try:
                # Деактивировать истёкшие подписки
                result = await session.execute(
                    update(Subscription)
                    .where(
                        and_(
                            Subscription.is_active == True,
                            Subscription.end_date <= datetime.now()
                        )
                    )
                    .values(is_active=False)
                )
                
                expired_count = result.rowcount
                
                # Обновить пользователей с истёкшими подписками
                await session.execute(
                    update(User)
                    .where(
                        and_(
                            User.subscription_type != "free",
                            User.subscription_end <= datetime.now()
                        )
                    )
                    .values(
                        subscription_type="free",
                        subscription_start=None,
                        subscription_end=None,
                        daily_limit=3
                    )
                )
                
                await session.commit()
                return expired_count
                
            except Exception as e:
                logger.error(f"Ошибка при проверке истёкших подписок: {e}")
                await session.rollback()
                return 0


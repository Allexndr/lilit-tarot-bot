"""
Сервис для админ-панели
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.database import DatabaseManager
from telegram_bot.models import User, Reading, Payment, Subscription, Analytics
from telegram_bot.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)


class AdminService:
    """Сервис для админ-панели"""
    
    @staticmethod
    async def get_dashboard_stats() -> Dict[str, Any]:
        """Получить статистику для дашборда"""
        async with DatabaseManager.get_session() as session:
            try:
                # Общее количество пользователей
                result = await session.execute(select(func.count(User.id)))
                total_users = result.scalar()
                
                # Новые пользователи за последние 30 дней
                month_ago = datetime.now() - timedelta(days=30)
                result = await session.execute(
                    select(func.count(User.id))
                    .where(User.registration_date >= month_ago)
                )
                new_users_30d = result.scalar()
                
                # Активные пользователи за последние 7 дней
                week_ago = datetime.now() - timedelta(days=7)
                result = await session.execute(
                    select(func.count(User.id))
                    .where(User.last_activity >= week_ago)
                )
                active_users_7d = result.scalar()
                
                # Общее количество запросов
                result = await session.execute(select(func.sum(User.total_requests)))
                total_requests = result.scalar() or 0
                
                # Запросы за последние 30 дней
                result = await session.execute(
                    select(func.count(Reading.id))
                    .where(Reading.created_at >= month_ago)
                )
                requests_30d = result.scalar()
                
                # Доходы за месяц
                result = await session.execute(
                    select(func.sum(Payment.amount))
                    .where(
                        and_(
                            Payment.status == "completed",
                            Payment.created_at >= month_ago
                        )
                    )
                )
                monthly_revenue = result.scalar() or 0
                
                # Доходы за все время
                result = await session.execute(
                    select(func.sum(Payment.amount))
                    .where(Payment.status == "completed")
                )
                total_revenue = result.scalar() or 0
                
                # Статистика подписок
                subscription_stats = await SubscriptionService.get_subscription_stats()
                
                return {
                    "total_users": total_users,
                    "new_users_30d": new_users_30d,
                    "active_users_7d": active_users_7d,
                    "total_requests": total_requests,
                    "requests_30d": requests_30d,
                    "monthly_revenue": monthly_revenue,
                    "total_revenue": total_revenue,
                    "subscription_stats": subscription_stats
                }
                
            except Exception as e:
                logger.error(f"Ошибка при получении статистики дашборда: {e}")
                return {"error": "Ошибка при получении статистики"}
    
    @staticmethod
    async def get_users_list(page: int = 1, limit: int = 50, 
                            search: Optional[str] = None) -> Dict[str, Any]:
        """Получить список пользователей"""
        async with DatabaseManager.get_session() as session:
            try:
                offset = (page - 1) * limit
                
                # Базовый запрос
                query = select(User)
                
                # Поиск по имени или username
                if search:
                    query = query.where(
                        or_(
                            User.first_name.ilike(f"%{search}%"),
                            User.last_name.ilike(f"%{search}%"),
                            User.username.ilike(f"%{search}%")
                        )
                    )
                
                # Общее количество
                count_result = await session.execute(select(func.count(User.id)))
                total_count = count_result.scalar()
                
                # Получить пользователей
                query = query.order_by(User.registration_date.desc()).offset(offset).limit(limit)
                result = await session.execute(query)
                users = result.scalars().all()
                
                # Форматировать данные
                users_data = []
                for user in users:
                    users_data.append({
                        "id": user.id,
                        "telegram_id": user.telegram_id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "subscription_type": user.subscription_type,
                        "total_requests": user.total_requests,
                        "daily_requests": user.daily_requests,
                        "registration_date": user.registration_date,
                        "last_activity": user.last_activity,
                        "total_spent": user.total_spent
                    })
                
                return {
                    "users": users_data,
                    "total_count": total_count,
                    "page": page,
                    "limit": limit,
                    "total_pages": (total_count + limit - 1) // limit
                }
                
            except Exception as e:
                logger.error(f"Ошибка при получении списка пользователей: {e}")
                return {"error": "Ошибка при получении списка пользователей"}
    
    @staticmethod
    async def get_user_details(user_id: int) -> Dict[str, Any]:
        """Получить детальную информацию о пользователе"""
        async with DatabaseManager.get_session() as session:
            try:
                # Получить пользователя
                result = await session.execute(
                    select(User).where(User.telegram_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    return {"error": "Пользователь не найден"}
                
                # Получить подписки
                result = await session.execute(
                    select(Subscription)
                    .where(Subscription.user_id == user.id)
                    .order_by(Subscription.created_at.desc())
                )
                subscriptions = result.scalars().all()
                
                # Получить платежи
                result = await session.execute(
                    select(Payment)
                    .where(Payment.user_id == user.id)
                    .order_by(Payment.created_at.desc())
                )
                payments = result.scalars().all()
                
                # Получить последние запросы
                result = await session.execute(
                    select(Reading)
                    .where(Reading.user_id == user.id)
                    .order_by(Reading.created_at.desc())
                    .limit(10)
                )
                readings = result.scalars().all()
                
                return {
                    "user": {
                        "id": user.id,
                        "telegram_id": user.telegram_id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "subscription_type": user.subscription_type,
                        "total_requests": user.total_requests,
                        "daily_requests": user.daily_requests,
                        "registration_date": user.registration_date,
                        "last_activity": user.last_activity,
                        "total_spent": user.total_spent
                    },
                    "subscriptions": [
                        {
                            "id": sub.id,
                            "plan_type": sub.plan_type,
                            "price": sub.price,
                            "start_date": sub.start_date,
                            "end_date": sub.end_date,
                            "is_active": sub.is_active,
                            "created_at": sub.created_at
                        }
                        for sub in subscriptions
                    ],
                    "payments": [
                        {
                            "id": payment.id,
                            "amount": payment.amount,
                            "currency": payment.currency,
                            "status": payment.status,
                            "created_at": payment.created_at,
                            "completed_at": payment.completed_at
                        }
                        for payment in payments
                    ],
                    "recent_readings": [
                        {
                            "id": reading.id,
                            "question": reading.question,
                            "created_at": reading.created_at,
                            "cost": reading.cost
                        }
                        for reading in readings
                    ]
                }
                
            except Exception as e:
                logger.error(f"Ошибка при получении деталей пользователя: {e}")
                return {"error": "Ошибка при получении деталей пользователя"}
    
    @staticmethod
    async def get_payments_list(page: int = 1, limit: int = 50, 
                              status: Optional[str] = None) -> Dict[str, Any]:
        """Получить список платежей"""
        async with DatabaseManager.get_session() as session:
            try:
                offset = (page - 1) * limit
                
                # Базовый запрос
                query = select(Payment, User).join(User, Payment.user_id == User.id)
                
                # Фильтр по статусу
                if status:
                    query = query.where(Payment.status == status)
                
                # Общее количество
                count_result = await session.execute(select(func.count(Payment.id)))
                total_count = count_result.scalar()
                
                # Получить платежи
                query = query.order_by(Payment.created_at.desc()).offset(offset).limit(limit)
                result = await session.execute(query)
                payments_data = result.all()
                
                # Форматировать данные
                payments = []
                for payment, user in payments_data:
                    payments.append({
                        "id": payment.id,
                        "user_id": payment.user_id,
                        "user_name": f"{user.first_name} {user.last_name}" if user.first_name else user.username,
                        "amount": payment.amount,
                        "currency": payment.currency,
                        "status": payment.status,
                        "payment_type": payment.payment_type,
                        "provider": payment.provider,
                        "created_at": payment.created_at,
                        "completed_at": payment.completed_at
                    })
                
                return {
                    "payments": payments,
                    "total_count": total_count,
                    "page": page,
                    "limit": limit,
                    "total_pages": (total_count + limit - 1) // limit
                }
                
            except Exception as e:
                logger.error(f"Ошибка при получении списка платежей: {e}")
                return {"error": "Ошибка при получении списка платежей"}
    
    @staticmethod
    async def get_analytics_data(days: int = 30) -> Dict[str, Any]:
        """Получить аналитические данные"""
        async with DatabaseManager.get_session() as session:
            try:
                start_date = datetime.now() - timedelta(days=days)
                
                # Регистрации по дням
                result = await session.execute(
                    select(
                        func.date(User.registration_date).label('date'),
                        func.count(User.id).label('count')
                    )
                    .where(User.registration_date >= start_date)
                    .group_by(func.date(User.registration_date))
                    .order_by('date')
                )
                registrations_by_day = [
                    {"date": str(date), "count": count}
                    for date, count in result
                ]
                
                # Запросы по дням
                result = await session.execute(
                    select(
                        func.date(Reading.created_at).label('date'),
                        func.count(Reading.id).label('count')
                    )
                    .where(Reading.created_at >= start_date)
                    .group_by(func.date(Reading.created_at))
                    .order_by('date')
                )
                requests_by_day = [
                    {"date": str(date), "count": count}
                    for date, count in result
                ]
                
                # Доходы по дням
                result = await session.execute(
                    select(
                        func.date(Payment.created_at).label('date'),
                        func.sum(Payment.amount).label('amount')
                    )
                    .where(
                        and_(
                            Payment.created_at >= start_date,
                            Payment.status == "completed"
                        )
                    )
                    .group_by(func.date(Payment.created_at))
                    .order_by('date')
                )
                revenue_by_day = [
                    {"date": str(date), "amount": amount or 0}
                    for date, amount in result
                ]
                
                # Популярные типы запросов
                result = await session.execute(
                    select(
                        Reading.spread_id,
                        func.count(Reading.id).label('count')
                    )
                    .where(Reading.created_at >= start_date)
                    .group_by(Reading.spread_id)
                    .order_by(func.count(Reading.id).desc())
                    .limit(10)
                )
                popular_requests = [
                    {"spread_id": spread_id, "count": count}
                    for spread_id, count in result
                ]
                
                return {
                    "registrations_by_day": registrations_by_day,
                    "requests_by_day": requests_by_day,
                    "revenue_by_day": revenue_by_day,
                    "popular_requests": popular_requests
                }
                
            except Exception as e:
                logger.error(f"Ошибка при получении аналитических данных: {e}")
                return {"error": "Ошибка при получении аналитических данных"}
    
    @staticmethod
    async def update_user_subscription(user_id: int, plan_type: str, 
                                     days: int = 30) -> Dict[str, Any]:
        """Обновить подписку пользователя (админ)"""
        try:
            result = await SubscriptionService.create_subscription(user_id, plan_type)
            return result
        except Exception as e:
            logger.error(f"Ошибка при обновлении подписки: {e}")
            return {"error": "Ошибка при обновлении подписки"}
    
    @staticmethod
    async def reset_user_limits(user_id: int) -> Dict[str, Any]:
        """Сбросить лимиты пользователя"""
        async with DatabaseManager.get_session() as session:
            try:
                await session.execute(
                    update(User)
                    .where(User.telegram_id == user_id)
                    .values(daily_requests=0)
                )
                await session.commit()
                
                return {"success": True, "message": "Лимиты пользователя сброшены"}
                
            except Exception as e:
                logger.error(f"Ошибка при сбросе лимитов: {e}")
                await session.rollback()
                return {"error": "Ошибка при сбросе лимитов"}


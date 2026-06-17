"""
Интеграция с платёжной системой Robokassa для Казахстана
"""

import hashlib
import hmac
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import aiohttp

from config import settings

logger = logging.getLogger(__name__)


class RobokassaPayment:
    """Класс для работы с Robokassa"""
    
    def __init__(self):
        self.login = settings.robokassa_login
        self.password1 = settings.robokassa_password1
        self.password2 = settings.robokassa_password2
        self.test_mode = settings.robokassa_test_mode
        
        if self.test_mode:
            self.base_url = "https://auth.robokassa.ru/Merchant/Index.aspx"
        else:
            self.base_url = "https://auth.robokassa.ru/Merchant/Index.aspx"
    
    def _generate_signature(self, params: Dict[str, Any], password: str) -> str:
        """Генерировать подпись для Robokassa"""
        # Сортируем параметры по ключу
        sorted_params = sorted(params.items())
        
        # Создаём строку для подписи
        sign_string = ":".join([f"{key}={value}" for key, value in sorted_params])
        sign_string += f":{password}"
        
        # Генерируем MD5 хеш
        signature = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
        return signature
    
    def create_payment_url(self, amount: int, description: str, 
                          order_id: str, user_id: int) -> Dict[str, Any]:
        """Создать URL для оплаты"""
        try:
            # Параметры для Robokassa
            params = {
                "MerchantLogin": self.login,
                "OutSum": amount / 100,  # Переводим из тиынов в тенге
                "Description": description,
                "InvId": order_id,
                "Culture": "ru",
                "Encoding": "utf-8",
                "IsTest": "1" if self.test_mode else "0",
                "UserID": str(user_id)
            }
            
            # Генерируем подпись
            signature = self._generate_signature(params, self.password1)
            params["SignatureValue"] = signature
            
            # Создаём URL
            payment_url = f"{self.base_url}?{urlencode(params)}"
            
            return {
                "success": True,
                "payment_url": payment_url,
                "order_id": order_id,
                "amount": amount,
                "description": description
            }
            
        except Exception as e:
            logger.error(f"Ошибка при создании URL оплаты: {e}")
            return {"error": "Ошибка при создании URL оплаты"}
    
    def verify_payment(self, amount: int, order_id: str, 
                      signature: str) -> bool:
        """Проверить подпись платежа"""
        try:
            # Параметры для проверки
            params = {
                "OutSum": amount / 100,
                "InvId": order_id
            }
            
            # Генерируем подпись с паролем 2
            expected_signature = self._generate_signature(params, self.password2)
            
            return signature.lower() == expected_signature.lower()
            
        except Exception as e:
            logger.error(f"Ошибка при проверке платежа: {e}")
            return False
    
    async def get_payment_status(self, order_id: str) -> Dict[str, Any]:
        """Получить статус платежа"""
        try:
            # В реальной реализации здесь будет запрос к API Robokassa
            # Пока возвращаем заглушку
            return {
                "success": True,
                "status": "completed",
                "order_id": order_id
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении статуса платежа: {e}")
            return {"error": "Ошибка при получении статуса платежа"}


class TelegramStarsPayment:
    """Класс для работы с Telegram Stars"""
    
    def __init__(self):
        self.bot_token = settings.bot_token
    
    async def create_payment(self, amount: int, description: str, 
                           user_id: int) -> Dict[str, Any]:
        """Создать платеж через Telegram Stars"""
        try:
            # В реальной реализации здесь будет создание инвойса через Telegram Bot API
            # Пока возвращаем заглушку
            return {
                "success": True,
                "payment_id": f"stars_{user_id}_{amount}",
                "amount": amount,
                "description": description,
                "currency": "XTR"  # Telegram Stars
            }
            
        except Exception as e:
            logger.error(f"Ошибка при создании платежа Telegram Stars: {e}")
            return {"error": "Ошибка при создании платежа"}
    
    async def verify_payment(self, payment_id: str) -> Dict[str, Any]:
        """Проверить статус платежа Telegram Stars"""
        try:
            # В реальной реализации здесь будет проверка через Telegram Bot API
            # Пока возвращаем заглушку
            return {
                "success": True,
                "status": "completed",
                "payment_id": payment_id
            }
            
        except Exception as e:
            logger.error(f"Ошибка при проверке платежа Telegram Stars: {e}")
            return {"error": "Ошибка при проверке платежа"}


class PaymentService:
    """Сервис для работы с платежами"""
    
    def __init__(self):
        self.robokassa = RobokassaPayment()
        self.telegram_stars = TelegramStarsPayment()
    
    async def create_subscription_payment(self, user_id: int, plan_type: str, 
                                        payment_method: str = "robokassa") -> Dict[str, Any]:
        """Создать платеж для подписки"""
        from telegram_bot.subscription_service import SubscriptionService
        
        # Получить информацию о плане
        plan_info = SubscriptionService.SUBSCRIPTION_PLANS.get(plan_type)
        if not plan_info:
            return {"error": "Неверный тип подписки"}
        
        amount = plan_info["price"]
        description = f"Подписка {plan_info['name']} - АРУАХ"
        order_id = f"sub_{user_id}_{plan_type}_{int(datetime.now().timestamp())}"
        
        if payment_method == "robokassa":
            return self.robokassa.create_payment_url(amount, description, order_id, user_id)
        elif payment_method == "telegram_stars":
            return await self.telegram_stars.create_payment(amount, description, user_id)
        else:
            return {"error": "Неподдерживаемый метод оплаты"}
    
    async def create_consultation_payment(self, user_id: int, 
                                        payment_method: str = "robokassa") -> Dict[str, Any]:
        """Создать платеж для VIP консультации"""
        amount = 15000  # 15,000 тенге
        description = "VIP консультация - АРУАХ"
        order_id = f"consult_{user_id}_{int(datetime.now().timestamp())}"
        
        if payment_method == "robokassa":
            return self.robokassa.create_payment_url(amount, description, order_id, user_id)
        elif payment_method == "telegram_stars":
            return await self.telegram_stars.create_payment(amount, description, user_id)
        else:
            return {"error": "Неподдерживаемый метод оплаты"}
    
    async def verify_payment(self, payment_id: str, amount: int, 
                           signature: Optional[str] = None) -> Dict[str, Any]:
        """Проверить платеж"""
        if payment_id.startswith("stars_"):
            return await self.telegram_stars.verify_payment(payment_id)
        else:
            # Robokassa платеж
            if not signature:
                return {"error": "Отсутствует подпись для Robokassa"}
            
            is_valid = self.robokassa.verify_payment(amount, payment_id, signature)
            return {
                "success": is_valid,
                "status": "completed" if is_valid else "failed"
            }


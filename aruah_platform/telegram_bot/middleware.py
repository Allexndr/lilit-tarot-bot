"""
Middleware для Telegram бота АРУАХ
"""

import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from telegram_bot.services import UserService

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    """Middleware для работы с пользователями"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Обработка middleware"""
        if isinstance(event, Update) and event.message:
            # Получить пользователя
            user = await UserService.get_or_create_user(
                telegram_id=event.message.from_user.id,
                username=event.message.from_user.username,
                first_name=event.message.from_user.first_name,
                last_name=event.message.from_user.last_name
            )
            data['user'] = user
            
        elif isinstance(event, Update) and event.callback_query:
            # Получить пользователя из callback query
            user = await UserService.get_or_create_user(
                telegram_id=event.callback_query.from_user.id,
                username=event.callback_query.from_user.username,
                first_name=event.callback_query.from_user.first_name,
                last_name=event.callback_query.from_user.last_name
            )
            data['user'] = user
        
        return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Обработка middleware"""
        if isinstance(event, Update) and event.message:
            logger.info(f"Сообщение от {event.message.from_user.id}: {event.message.text}")
        elif isinstance(event, Update) and event.callback_query:
            logger.info(f"Callback от {event.callback_query.from_user.id}: {event.callback_query.data}")
        
        return await handler(event, data)


class RateLimitMiddleware(BaseMiddleware):
    """Middleware для ограничения частоты запросов"""
    
    def __init__(self, max_requests_per_minute: int = 10):
        self.max_requests_per_minute = max_requests_per_minute
        self.user_requests = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Обработка middleware"""
        user_id = None
        
        if isinstance(event, Update) and event.message:
            user_id = event.message.from_user.id
        elif isinstance(event, Update) and event.callback_query:
            user_id = event.callback_query.from_user.id
        
        if user_id:
            # Проверить лимит запросов
            if not self._check_rate_limit(user_id):
                logger.warning(f"Превышен лимит запросов для пользователя {user_id}")
                return  # Не обрабатывать запрос
        
        return await handler(event, data)
    
    def _check_rate_limit(self, user_id: int) -> bool:
        """Проверить лимит запросов"""
        import time
        
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Очистить старые запросы
        if user_id in self.user_requests:
            self.user_requests[user_id] = [
                req_time for req_time in self.user_requests[user_id] 
                if req_time > minute_ago
            ]
        else:
            self.user_requests[user_id] = []
        
        # Проверить лимит
        if len(self.user_requests[user_id]) >= self.max_requests_per_minute:
            return False
        
        # Добавить текущий запрос
        self.user_requests[user_id].append(current_time)
        return True


def setup_middleware(dp):
    """Настроить middleware для диспетчера"""
    # Добавить middleware в порядке выполнения
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    
    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())


#!/usr/bin/env python3
"""
Скрипт для устранения конфликтов webhook и getUpdates
"""

import asyncio
from aiogram import Bot
from config import settings


async def fix_webhook():
    """Удалить webhook и очистить pending updates"""
    bot = Bot(token=settings.bot_token)
    
    try:
        # Удаляем webhook
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook удален")
        
        # Получаем информацию о боте
        me = await bot.get_me()
        print(f"✅ Бот найден: @{me.username} - {me.first_name}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(fix_webhook()) 
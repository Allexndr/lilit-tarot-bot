#!/usr/bin/env python3
"""
Простой тест работы бота
"""

import asyncio
from aiogram import Bot
from config import settings


async def test_bot():
    """Проверить работу бота"""
    bot = Bot(token=settings.bot_token)
    
    try:
        # Получаем информацию о боте
        me = await bot.get_me()
        print(f"✅ Бот работает: @{me.username} - {me.first_name}")
        print(f"📍 ID: {me.id}")
        print(f"🔗 Ссылка: https://t.me/{me.username}")
        
        # Проверяем статус
        webhook_info = await bot.get_webhook_info()
        print(f"📡 Webhook URL: {webhook_info.url or 'Не установлен'}")
        print(f"📨 Pending updates: {webhook_info.pending_update_count}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(test_bot()) 
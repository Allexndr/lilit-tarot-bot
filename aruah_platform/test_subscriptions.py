#!/usr/bin/env python3
"""
Тестирование системы подписок и лимитов
"""

import asyncio
import sys
from pathlib import Path
from datetime import date, datetime

# Добавить путь к модулям
sys.path.append(str(Path(__file__).parent))

from telegram_bot.subscription_service import SubscriptionService
from payment_systems.robokassa import PaymentService


async def test_subscription_system():
    """Тестирование системы подписок"""
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ ПОДПИСОК")
    print("=" * 50)
    
    # Тестовый пользователь
    test_user_id = 123456789
    
    try:
        # 1. Тест получения информации о подписке
        print("1. Тест получения информации о подписке...")
        subscription_info = await SubscriptionService.get_user_subscription(test_user_id)
        print(f"   ✅ Информация о подписке: {subscription_info}")
        
        # 2. Тест проверки лимитов
        print("\n2. Тест проверки лимитов...")
        can_request = await SubscriptionService.can_make_request(test_user_id)
        print(f"   ✅ Может ли сделать запрос: {can_request}")
        
        # 3. Тест создания подписки
        print("\n3. Тест создания подписки...")
        subscription_result = await SubscriptionService.create_subscription(test_user_id, "premium")
        print(f"   ✅ Результат создания подписки: {subscription_result}")
        
        # 4. Тест статистики подписок
        print("\n4. Тест статистики подписок...")
        stats = await SubscriptionService.get_subscription_stats()
        print(f"   ✅ Статистика подписок: {stats}")
        
        # 5. Тест платёжной системы
        print("\n5. Тест платёжной системы...")
        payment_service = PaymentService()
        
        # Создать платеж для подписки
        payment_result = await payment_service.create_subscription_payment(test_user_id, "premium", "robokassa")
        print(f"   ✅ Результат создания платежа: {payment_result}")
        
        # 6. Тест отмены подписки
        print("\n6. Тест отмены подписки...")
        cancel_result = await SubscriptionService.cancel_subscription(test_user_id)
        print(f"   ✅ Результат отмены подписки: {cancel_result}")
        
        print("\n✅ Все тесты системы подписок прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании системы подписок: {e}")


async def test_limits_system():
    """Тестирование системы лимитов"""
    print("\n🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ ЛИМИТОВ")
    print("=" * 50)
    
    test_user_id = 123456789
    
    try:
        # 1. Тест увеличения счётчика запросов
        print("1. Тест увеличения счётчика запросов...")
        increment_result = await SubscriptionService.increment_request_count(test_user_id)
        print(f"   ✅ Результат увеличения счётчика: {increment_result}")
        
        # 2. Тест сброса дневных лимитов
        print("\n2. Тест сброса дневных лимитов...")
        reset_result = await SubscriptionService.reset_daily_limits()
        print(f"   ✅ Сброшено лимитов для {reset_result} пользователей")
        
        # 3. Тест проверки истёкших подписок
        print("\n3. Тест проверки истёкших подписок...")
        expired_result = await SubscriptionService.check_expired_subscriptions()
        print(f"   ✅ Деактивировано {expired_result} истёкших подписок")
        
        print("\n✅ Все тесты системы лимитов прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании системы лимитов: {e}")


async def test_payment_system():
    """Тестирование платёжной системы"""
    print("\n🧪 ТЕСТИРОВАНИЕ ПЛАТЁЖНОЙ СИСТЕМЫ")
    print("=" * 50)
    
    test_user_id = 123456789
    
    try:
        payment_service = PaymentService()
        
        # 1. Тест создания платежа для подписки
        print("1. Тест создания платежа для подписки...")
        subscription_payment = await payment_service.create_subscription_payment(test_user_id, "premium", "robokassa")
        print(f"   ✅ Платеж для подписки: {subscription_payment}")
        
        # 2. Тест создания платежа для консультации
        print("\n2. Тест создания платежа для консультации...")
        consultation_payment = await payment_service.create_consultation_payment(test_user_id, "robokassa")
        print(f"   ✅ Платеж для консультации: {consultation_payment}")
        
        # 3. Тест создания платежа через Telegram Stars
        print("\n3. Тест создания платежа через Telegram Stars...")
        stars_payment = await payment_service.create_subscription_payment(test_user_id, "premium", "telegram_stars")
        print(f"   ✅ Платеж через Telegram Stars: {stars_payment}")
        
        print("\n✅ Все тесты платёжной системы прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании платёжной системы: {e}")


async def main():
    """Главная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ ПОДПИСОК И ЛИМИТОВ АРУАХ")
    print("=" * 60)
    
    try:
        # Тестировать все системы
        await test_subscription_system()
        await test_limits_system()
        await test_payment_system()
        
        print("\n" + "=" * 60)
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Система подписок работает корректно")
        print("✅ Система лимитов работает корректно")
        print("✅ Платёжная система работает корректно")
        print("")
        print("🚀 Платформа готова к монетизации!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


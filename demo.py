#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования функций Telegram-бота ЛИЛИТ
"""

import asyncio
from datetime import date
from bot.services import TarotService, DestinyMatrixService, AstroService
from bot.tarot_data import MAJOR_ARCANA, TAROT_SPREADS


def demo_tarot_card():
    """Демонстрация работы с картой Таро"""
    print("🔮 ДЕМОНСТРАЦИЯ: Случайная карта Таро")
    print("=" * 50)
    
    card = TarotService.get_random_card()
    interpretation = TarotService.interpret_card(card, "Карта дня")
    
    print(interpretation)
    print("\n")


def demo_three_card_spread():
    """Демонстрация расклада на 3 карты"""
    print("🛤 ДЕМОНСТРАЦИЯ: Расклад 'Путь'")
    print("=" * 50)
    
    cards = TarotService.get_cards_for_spread("three_cards")
    positions = ["Прошлое", "Настоящее", "Будущее"]
    
    print("🛤 **РАСКЛАД 'ПУТЬ'**\n")
    
    for i, (card, position) in enumerate(zip(cards, positions)):
        interpretation = TarotService.interpret_card(card, position)
        print(interpretation)
        if i < len(cards) - 1:
            print("\n" + "="*30 + "\n")
    
    print("\n✨ **ОБЩИЙ СОВЕТ:**")
    print("Помните: прошлое дало вам опыт, настоящее — возможности, будущее — надежды.")
    print("\n")


def demo_arcana_dialogue():
    """Демонстрация диалога с Арканом"""
    print("🎭 ДЕМОНСТРАЦИЯ: Диалог с Арканом")
    print("=" * 50)
    
    # Возьмем первый доступный Аркан
    arcana_id = 0  # Дурак
    arcana = MAJOR_ARCANA[arcana_id]
    
    print(f"🎭 **Диалог с Арканом: {arcana['name']}**\n")
    print(f"*{arcana['arcana_personality']}*\n")
    
    import random
    advice = random.choice(arcana['arcana_voice_phrases'])
    print(f"💬 {advice}")
    print(f"✨ {arcana['upright_short']}")
    print("\n")


def demo_destiny_matrix():
    """Демонстрация Матрицы Судьбы"""
    print("🌟 ДЕМОНСТРАЦИЯ: Матрица Судьбы")
    print("=" * 50)
    
    # Пример даты рождения
    birth_date = date(1990, 5, 15)
    
    positions = DestinyMatrixService.calculate_matrix(birth_date)
    interpretation = DestinyMatrixService.interpret_matrix(positions)
    
    print(f"📅 Дата рождения: {birth_date.strftime('%d.%m.%Y')}\n")
    print(interpretation)
    print("\n")


def demo_astro_forecast():
    """Демонстрация астропрогноза"""
    print("🌟 ДЕМОНСТРАЦИЯ: Астропрогноз")
    print("=" * 50)
    
    # Пример даты рождения для определения знака зодиака
    birth_date = date(1990, 5, 15)  # Телец
    
    zodiac_sign = AstroService.get_zodiac_sign(birth_date)
    forecast = AstroService.generate_daily_forecast(zodiac_sign)
    
    print(f"📅 Дата рождения: {birth_date.strftime('%d.%m.%Y')}")
    print(forecast)
    print("\n")


def demo_available_spreads():
    """Демонстрация доступных раскладов"""
    print("📋 ДЕМОНСТРАЦИЯ: Доступные расклады")
    print("=" * 50)
    
    for spread_id, spread_info in TAROT_SPREADS.items():
        premium_mark = "💎" if spread_info['is_premium'] else "🆓"
        print(f"{premium_mark} **{spread_info['name']}** ({spread_info['card_count']} карт)")
        print(f"   📝 {spread_info['description']}")
        print(f"   🏷️ Категория: {spread_info['category']}")
        print()


def main():
    """Главная функция демонстрации"""
    print("🌙 ЛИЛИТ - Telegram-бот Таро")
    print("🎯 ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ")
    print("=" * 70)
    print()
    
    # Запуск всех демонстраций
    demo_tarot_card()
    demo_three_card_spread()
    demo_arcana_dialogue()
    demo_destiny_matrix()
    demo_astro_forecast()
    demo_available_spreads()
    
    print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("\nДля запуска бота используйте команду:")
    print("python3 main.py")
    print("\nТокен бота уже настроен в config.py")
    print("Бот готов к работе в Telegram!")


if __name__ == "__main__":
    main() 
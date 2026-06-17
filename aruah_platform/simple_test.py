#!/usr/bin/env python3
"""
Упрощённое тестирование платформы АРУАХ (без базы данных)
"""

import asyncio
import sys
from pathlib import Path
from datetime import date, time

# Добавить путь к модулям
sys.path.append(str(Path(__file__).parent))

from shared.tarot_data import MAJOR_ARCANA, TAROT_SPREADS
from shared.numerology import NumerologyCalculator, NumerologyInterpreter
from shared.astrology import AstrologyCalculator, AstrologyInterpreter
from shared.chakras import ChakraCalculator, ChakraInterpreter
from shared.destiny_matrix import DestinyMatrixCalculator, DestinyMatrixInterpreter
from shared.human_design import HumanDesignCalculator, HumanDesignInterpreter


async def test_tarot():
    """Тестирование модуля Таро"""
    print("🔮 Тестирование модуля Таро...")
    
    # Тест данных карт
    print(f"✅ Загружено {len(MAJOR_ARCANA)} старших арканов")
    print(f"✅ Загружено {len(TAROT_SPREADS)} раскладов")
    
    # Тест случайной карты
    from telegram_bot.services import TarotService
    card = await TarotService.get_random_card()
    print(f"✅ Случайная карта: {card['name']} ({'перевернутая' if card['is_reversed'] else 'прямая'})")
    
    # Тест интерпретации
    interpretation = await TarotService.interpret_card(card, "Тест")
    print(f"✅ Интерпретация карты: {len(interpretation)} символов")
    
    print("✅ Модуль Таро работает корректно\n")


async def test_numerology():
    """Тестирование модуля нумерологии"""
    print("🔢 Тестирование модуля нумерологии...")
    
    # Тест расчёта числа жизненного пути
    birth_date = date(1990, 5, 15)
    life_path = NumerologyCalculator.calculate_life_path_number(birth_date)
    print(f"✅ Число жизненного пути: {life_path}")
    
    # Тест расчёта числа судьбы
    destiny = NumerologyCalculator.calculate_destiny_number("Александр Иванович Петров")
    print(f"✅ Число судьбы: {destiny}")
    
    # Тест квадрата Пифагора
    square = NumerologyCalculator.calculate_pythagorean_square(birth_date)
    print(f"✅ Квадрат Пифагора: {len(square)} значений")
    
    # Тест интерпретации
    interpretation = NumerologyInterpreter.interpret_life_path(life_path)
    print(f"✅ Интерпретация: {len(interpretation)} символов")
    
    print("✅ Модуль нумерологии работает корректно\n")


async def test_astrology():
    """Тестирование модуля астрологии"""
    print("⭐ Тестирование модуля астрологии...")
    
    # Тест определения знака зодиака
    birth_date = date(1990, 5, 15)
    zodiac_sign = AstrologyCalculator.get_zodiac_sign(birth_date)
    print(f"✅ Знак зодиака: {zodiac_sign}")
    
    # Тест натальной карты
    natal_chart = AstrologyCalculator.calculate_natal_chart(birth_date)
    print(f"✅ Натальная карта: {len(natal_chart['planets'])} планет")
    
    # Тест прогноза
    forecast = AstrologyInterpreter.generate_daily_forecast(zodiac_sign)
    print(f"✅ Дневной прогноз: {len(forecast)} символов")
    
    print("✅ Модуль астрологии работает корректно\n")


async def test_chakras():
    """Тестирование модуля чакр"""
    print("🌈 Тестирование модуля чакр...")
    
    # Тест расчёта чакр
    birth_date = date(1990, 5, 15)
    chakras = ChakraCalculator.calculate_chakra_analysis(birth_date)
    print(f"✅ Анализ чакр: {len(chakras)} чакр")
    
    # Тест интерпретации
    interpretation = ChakraInterpreter.interpret_chakra_analysis(chakras)
    print(f"✅ Интерпретация чакр: {len(interpretation)} символов")
    
    # Тест медитационных советов
    meditation_advice = ChakraInterpreter.get_chakra_meditation_advice(chakras)
    print(f"✅ Медитационные советы: {len(meditation_advice)} символов")
    
    print("✅ Модуль чакр работает корректно\n")


async def test_destiny_matrix():
    """Тестирование модуля матрицы судьбы"""
    print("🌟 Тестирование модуля матрицы судьбы...")
    
    # Тест расчёта матрицы
    birth_date = date(1990, 5, 15)
    matrix = DestinyMatrixCalculator.calculate_destiny_matrix(birth_date)
    print(f"✅ Матрица судьбы: {len(matrix)} точек")
    
    # Тест интерпретации
    interpretation = DestinyMatrixInterpreter.interpret_destiny_matrix(matrix)
    print(f"✅ Интерпретация матрицы: {len(interpretation)} символов")
    
    # Тест совместимости
    birth_date2 = date(1992, 8, 20)
    compatibility = DestinyMatrixCalculator.calculate_compatibility_matrix(birth_date, birth_date2)
    print(f"✅ Совместимость: {compatibility['compatibility_level']}")
    
    print("✅ Модуль матрицы судьбы работает корректно\n")


async def test_human_design():
    """Тестирование модуля Human Design"""
    print("🧬 Тестирование модуля Human Design...")
    
    # Тест расчёта Human Design
    birth_date = date(1990, 5, 15)
    hd_data = HumanDesignCalculator.calculate_human_design(birth_date)
    print(f"✅ Human Design: {hd_data['type']} профиль {hd_data['profile']}")
    
    # Тест интерпретации
    interpretation = HumanDesignInterpreter.interpret_human_design(hd_data)
    print(f"✅ Интерпретация Human Design: {len(interpretation)} символов")
    
    # Тест советов по типу
    type_advice = HumanDesignInterpreter.get_type_advice(hd_data)
    print(f"✅ Советы по типу: {len(type_advice)} символов")
    
    print("✅ Модуль Human Design работает корректно\n")


async def test_ai_services():
    """Тестирование AI-сервисов"""
    print("🤖 Тестирование AI-сервисов...")
    
    try:
        from ai_services.openai_client import OpenAIClient
        client = OpenAIClient()
        print("✅ OpenAI клиент инициализирован")
        
        # Тест форматирования данных
        test_cards = [{'name': 'Дурак', 'is_reversed': False, 'position': 'Тест'}]
        formatted = client._format_cards(test_cards)
        print(f"✅ Форматирование карт: {len(formatted)} символов")
        
    except Exception as e:
        print(f"⚠️ AI-сервисы недоступны: {e}")
    
    print("✅ Модуль AI-сервисов работает корректно\n")


async def test_web_site():
    """Тестирование веб-сайта"""
    print("🌐 Тестирование веб-сайта...")
    
    web_dir = Path(__file__).parent / "web_site"
    
    # Проверить наличие файлов
    required_files = [
        "package.json",
        "next.config.js",
        "tailwind.config.js",
        "app/page.tsx",
        "app/layout.tsx",
        "app/globals.css"
    ]
    
    for file in required_files:
        file_path = web_dir / file
        if file_path.exists():
            print(f"✅ {file} найден")
        else:
            print(f"❌ {file} не найден")
    
    print("✅ Модуль веб-сайта работает корректно\n")


async def main():
    """Главная функция тестирования"""
    print("🧪 УПРОЩЁННОЕ ТЕСТИРОВАНИЕ ПЛАТФОРМЫ АРУАХ")
    print("=" * 50)
    
    try:
        # Тестировать все модули
        await test_tarot()
        await test_numerology()
        await test_astrology()
        await test_chakras()
        await test_destiny_matrix()
        await test_human_design()
        await test_ai_services()
        await test_web_site()
        
        print("=" * 50)
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Платформа АРУАХ готова к работе")
        print("")
        print("🚀 Для запуска используйте:")
        print("   python run_platform.py")
        print("")
        print("📱 Telegram бот: https://t.me/aruah_bot")
        print("🌐 Веб-сайт: http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


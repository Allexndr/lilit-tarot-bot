#!/usr/bin/env python3
"""
Демонстрация возможностей платформы АРУАХ
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


async def demo_tarot():
    """Демонстрация модуля Таро"""
    print("🔮 ДЕМОНСТРАЦИЯ ТАРО")
    print("=" * 40)
    
    # Показать несколько карт
    print("Старшие Арканы:")
    for i in range(5):
        card_data = MAJOR_ARCANA.get(i, {})
        print(f"  {i}: {card_data.get('name', 'Неизвестно')}")
    
    print(f"\nВсего карт: {len(MAJOR_ARCANA)}")
    
    # Показать расклады
    print("\nДоступные расклады:")
    for name, info in TAROT_SPREADS.items():
        print(f"  {name}: {info['name']} ({info['card_count']} карт)")
    
    print()


async def demo_numerology():
    """Демонстрация модуля нумерологии"""
    print("🔢 ДЕМОНСТРАЦИЯ НУМЕРОЛОГИИ")
    print("=" * 40)
    
    # Тестовые данные
    birth_date = date(1990, 5, 15)
    name = "Александр Иванович Петров"
    
    # Число жизненного пути
    life_path = NumerologyCalculator.calculate_life_path_number(birth_date)
    print(f"Дата рождения: {birth_date}")
    print(f"Число жизненного пути: {life_path}")
    
    # Число судьбы
    destiny = NumerologyCalculator.calculate_destiny_number(name)
    print(f"Имя: {name}")
    print(f"Число судьбы: {destiny}")
    
    # Квадрат Пифагора
    square = NumerologyCalculator.calculate_pythagorean_square(birth_date)
    print(f"Квадрат Пифагора: {square}")
    
    # Персональный год
    personal_year = NumerologyCalculator.calculate_personal_year(birth_date, 2024)
    print(f"Персональный год 2024: {personal_year}")
    
    print()


async def demo_astrology():
    """Демонстрация модуля астрологии"""
    print("⭐ ДЕМОНСТРАЦИЯ АСТРОЛОГИИ")
    print("=" * 40)
    
    # Тестовые данные
    birth_date = date(1990, 5, 15)
    birth_time = time(14, 30)
    birth_place = "Алматы, Казахстан"
    
    # Знак зодиака
    zodiac_sign = AstrologyCalculator.get_zodiac_sign(birth_date)
    print(f"Дата рождения: {birth_date}")
    print(f"Знак зодиака: {zodiac_sign}")
    
    # Натальная карта
    natal_chart = AstrologyCalculator.calculate_natal_chart(birth_date, birth_time, birth_place)
    print(f"Натальная карта: {len(natal_chart['planets'])} планет")
    
    # Восходящий знак
    rising_sign = AstrologyCalculator.get_rising_sign(birth_time)
    print(f"Восходящий знак: {rising_sign}")
    
    # Дневной прогноз
    forecast = AstrologyInterpreter.generate_daily_forecast(zodiac_sign)
    print(f"Дневной прогноз: {forecast[:100]}...")
    
    print()


async def demo_chakras():
    """Демонстрация модуля чакр"""
    print("🌈 ДЕМОНСТРАЦИЯ ЧАКР")
    print("=" * 40)
    
    # Тестовые данные
    birth_date = date(1990, 5, 15)
    
    # Анализ чакр
    chakras = ChakraCalculator.calculate_chakra_analysis(birth_date)
    print(f"Дата рождения: {birth_date}")
    print(f"Анализ чакр: {len(chakras)} чакр")
    
    # Показать состояние каждой чакры
    for chakra_id, chakra in chakras.items():
        print(f"  {chakra['name']}: {chakra['level']} ({chakra['percentage']}%)")
    
    # Общий балл баланса
    balance_score = ChakraCalculator.get_chakra_balance_score(chakras)
    print(f"Общий баланс чакр: {balance_score}%")
    
    print()


async def demo_destiny_matrix():
    """Демонстрация модуля матрицы судьбы"""
    print("🌟 ДЕМОНСТРАЦИЯ МАТРИЦЫ СУДЬБЫ")
    print("=" * 40)
    
    # Тестовые данные
    birth_date = date(1990, 5, 15)
    
    # Матрица судьбы
    matrix = DestinyMatrixCalculator.calculate_destiny_matrix(birth_date)
    print(f"Дата рождения: {birth_date}")
    print(f"Матрица судьбы: {len(matrix)} точек")
    
    # Основные точки
    main_points = ['personal_destiny', 'social_destiny', 'spiritual_destiny', 'karma_mother', 'karma_father']
    print("Основные точки:")
    for point in main_points:
        arcana_num = matrix[point]
        print(f"  {point}: {arcana_num}")
    
    # Совместимость
    birth_date2 = date(1992, 8, 20)
    compatibility = DestinyMatrixCalculator.calculate_compatibility_matrix(birth_date, birth_date2)
    print(f"Совместимость с {birth_date2}: {compatibility['compatibility_level']}")
    
    print()


async def demo_human_design():
    """Демонстрация модуля Human Design"""
    print("🧬 ДЕМОНСТРАЦИЯ HUMAN DESIGN")
    print("=" * 40)
    
    # Тестовые данные
    birth_date = date(1990, 5, 15)
    birth_time = time(14, 30)
    birth_place = "Алматы, Казахстан"
    
    # Human Design
    hd_data = HumanDesignCalculator.calculate_human_design(birth_date, birth_time, birth_place)
    print(f"Дата рождения: {birth_date}")
    print(f"Время рождения: {birth_time}")
    print(f"Место рождения: {birth_place}")
    print(f"Тип: {hd_data['type']}")
    print(f"Профиль: {hd_data['profile']}/6")
    print(f"Авторитет: {hd_data['authority']}")
    print(f"Стратегия: {hd_data['strategy']}")
    
    # Определённые центры
    print(f"Определённые центры: {len(hd_data['defined_centers'])}")
    for center in hd_data['defined_centers']:
        print(f"  {center}")
    
    # Неопределённые центры
    print(f"Неопределённые центры: {len(hd_data['undefined_centers'])}")
    for center in hd_data['undefined_centers']:
        print(f"  {center}")
    
    print()


async def demo_ai_integration():
    """Демонстрация AI-интеграции"""
    print("🤖 ДЕМОНСТРАЦИЯ AI-ИНТЕГРАЦИИ")
    print("=" * 40)
    
    try:
        from ai_services.openai_client import OpenAIClient
        client = OpenAIClient()
        print("✅ OpenAI клиент инициализирован")
        
        # Тест форматирования данных
        test_cards = [
            {'name': 'Дурак', 'is_reversed': False, 'position': 'Прошлое'},
            {'name': 'Маг', 'is_reversed': True, 'position': 'Настоящее'},
            {'name': 'Императрица', 'is_reversed': False, 'position': 'Будущее'}
        ]
        
        formatted_cards = client._format_cards(test_cards)
        print("Форматирование карт:")
        print(formatted_cards)
        
        # Тест контекста пользователя
        user_context = {
            'name': 'Александр',
            'birth_date': '1990-05-15',
            'gender': 'мужской',
            'city': 'Алматы'
        }
        
        formatted_context = client._format_user_context(user_context)
        print(f"Контекст пользователя: {formatted_context}")
        
    except Exception as e:
        print(f"⚠️ AI-сервисы недоступны: {e}")
    
    print()


async def demo_web_site():
    """Демонстрация веб-сайта"""
    print("🌐 ДЕМОНСТРАЦИЯ ВЕБ-САЙТА")
    print("=" * 40)
    
    web_dir = Path(__file__).parent / "web_site"
    
    # Проверить наличие файлов
    files_to_check = [
        "package.json",
        "next.config.js",
        "tailwind.config.js",
        "app/page.tsx",
        "app/layout.tsx",
        "app/globals.css"
    ]
    
    print("Файлы веб-сайта:")
    for file in files_to_check:
        file_path = web_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {file} ({size} байт)")
        else:
            print(f"  ❌ {file} не найден")
    
    print(f"\nДля запуска веб-сайта:")
    print(f"  cd {web_dir}")
    print(f"  npm install")
    print(f"  npm run dev")
    print(f"  Откройте http://localhost:3000")
    
    print()


async def main():
    """Главная функция демонстрации"""
    print("🌙 ДЕМОНСТРАЦИЯ ПЛАТФОРМЫ АРУАХ")
    print("=" * 50)
    print("Первая в Казахстане комплексная эзотерическая платформа")
    print("Таро • Нумерология • Астрология • Чакры • Матрица Судьбы • Human Design")
    print("=" * 50)
    print()
    
    # Демонстрация всех модулей
    await demo_tarot()
    await demo_numerology()
    await demo_astrology()
    await demo_chakras()
    await demo_destiny_matrix()
    await demo_human_design()
    await demo_ai_integration()
    await demo_web_site()
    
    print("=" * 50)
    print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("")
    print("🚀 Для запуска платформы:")
    print("   python run_platform.py")
    print("")
    print("🧪 Для тестирования:")
    print("   python test_platform.py")
    print("")
    print("📱 Telegram бот: https://t.me/aruah_bot")
    print("🌐 Веб-сайт: http://localhost:3000")
    print("")
    print("💎 Монетизация:")
    print("   FREE: 3 запроса/день")
    print("   PREMIUM: 2,500₸/мес")
    print("   VIP: 15,000₸/консультация")
    print("")
    print("📊 Прогноз доходов:")
    print("   Месяц 6: 4,250,000₸/мес")
    print("   Месяц 12: 17,500,000₸/мес")
    print("   ROI: 2,417% за первый год")
    print("")
    print("АРУАХ - Ваш проводник в мире эзотерических знаний 🌙✨")


if __name__ == "__main__":
    asyncio.run(main())


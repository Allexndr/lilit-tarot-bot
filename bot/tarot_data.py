"""
Данные карт Таро с интерпретациями на русском языке
"""

MAJOR_ARCANA = {
    0: {"name": "Дурак", "name_en": "The Fool", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m00.jpg", "arcana_type": "major", "upright_short": "Начни смело новый путь"},
    1: {"name": "Маг", "name_en": "The Magician", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m01.jpg", "arcana_type": "major", "upright_short": "У тебя есть все необходимое"},
    2: {"name": "Верховная Жрица", "name_en": "The High Priestess", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m02.jpg", "arcana_type": "major", "upright_short": "Слушай свой внутренний голос"},
    3: {"name": "Императрица", "name_en": "The Empress", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m03.jpg", "arcana_type": "major", "upright_short": "Время цветения и роста"},
    4: {"name": "Император", "name_en": "The Emperor", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m04.jpg", "arcana_type": "major", "upright_short": "Возьми ответственность"},
    5: {"name": "Иерофант", "name_en": "The Hierophant", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m05.jpg", "arcana_type": "major", "upright_short": "Доверься традициям"},
    6: {"name": "Влюбленные", "name_en": "The Lovers", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m06.jpg", "arcana_type": "major", "upright_short": "Сделай выбор сердцем"},
    7: {"name": "Колесница", "name_en": "The Chariot", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m07.jpg", "arcana_type": "major", "upright_short": "Вперед к победе"},
    8: {"name": "Сила", "name_en": "Strength", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m08.jpg", "arcana_type": "major", "upright_short": "Прояви мягкую силу"},
    9: {"name": "Отшельник", "name_en": "The Hermit", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m09.jpg", "arcana_type": "major", "upright_short": "Найди ответ внутри себя"},
    10: {"name": "Колесо Фортуны", "name_en": "Wheel of Fortune", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m10.jpg", "arcana_type": "major", "upright_short": "Перемены неизбежны"},
    11: {"name": "Справедливость", "name_en": "Justice", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m11.jpg", "arcana_type": "major", "upright_short": "Будь честен с собой"},
    12: {"name": "Повешенный", "name_en": "The Hanged Man", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m12.jpg", "arcana_type": "major", "upright_short": "Посмотри под другим углом"},
    13: {"name": "Смерть", "name_en": "Death", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m13.jpg", "arcana_type": "major", "upright_short": "Конец старого — начало нового"},
    14: {"name": "Умеренность", "name_en": "Temperance", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m14.jpg", "arcana_type": "major", "upright_short": "Найди баланс"},
    15: {"name": "Дьявол", "name_en": "The Devil", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m15.jpg", "arcana_type": "major", "upright_short": "Освободись от оков"},
    16: {"name": "Башня", "name_en": "The Tower", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m16.jpg", "arcana_type": "major", "upright_short": "Разрушение для обновления"},
    17: {"name": "Звезда", "name_en": "The Star", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m17.jpg", "arcana_type": "major", "upright_short": "Надежда светит тебе"},
    18: {"name": "Луна", "name_en": "The Moon", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m18.jpg", "arcana_type": "major", "upright_short": "Доверься интуиции"},
    19: {"name": "Солнце", "name_en": "The Sun", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m19.jpg", "arcana_type": "major", "upright_short": "Радость и успех"},
    20: {"name": "Суд", "name_en": "Judgement", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m20.jpg", "arcana_type": "major", "upright_short": "Время пробуждения"},
    21: {"name": "Мир", "name_en": "The World", "image": "https://raw.githubusercontent.com/ekelen/tarot-api/master/static/cards/m21.jpg", "arcana_type": "major", "upright_short": "Цикл завершен успешно"},
}

MINOR_ARCANA_SUITS = {
    "cups": {
        "name": "Кубки",
        "element": "Вода",
        "theme": "Эмоции, любовь, отношения, духовность"
    },
    "wands": {
        "name": "Жезлы",
        "element": "Огонь", 
        "theme": "Энергия, творчество, амбиции, действие"
    },
    "swords": {
        "name": "Мечи",
        "element": "Воздух",
        "theme": "Интеллект, конфликты, правда, мысли"
    },
    "pentacles": {
        "name": "Пентакли",
        "element": "Земля",
        "theme": "Материальное, деньги, здоровье, работа"
    }
}

# Значения для числовых карт младших арканов
MINOR_NUMBERS = {
    1: {
        "cups": {"name": "Туз Кубков", "meaning": "Новая любовь, эмоциональное пробуждение"},
        "wands": {"name": "Туз Жезлов", "meaning": "Творческое вдохновение, новая энергия"},
        "swords": {"name": "Туз Мечей", "meaning": "Ментальный прорыв, ясность мышления"},
        "pentacles": {"name": "Туз Пентаклей", "meaning": "Новые возможности, материальный старт"}
    },
    2: {
        "cups": {"name": "Двойка Кубков", "meaning": "Партнерство, взаимность в отношениях"},
        "wands": {"name": "Двойка Жезлов", "meaning": "Планирование, выбор направления"},
        "swords": {"name": "Двойка Мечей", "meaning": "Сложный выбор, баланс противоположностей"},
        "pentacles": {"name": "Двойка Пентаклей", "meaning": "Жонглирование ресурсами, адаптация"}
    }
}

TAROT_SPREADS = {
    "daily_card": {
        "name": "Карта дня",
        "description": "Простой расклад на одну карту для получения совета на день",
        "card_count": 1,
        "positions": ["Энергия дня"],
        "is_premium": False,
        "category": "daily"
    },
    "yes_no": {
        "name": "Да / Нет",
        "description": "Получите четкий ответ на конкретный вопрос",
        "card_count": 1,
        "positions": ["Ответ"],
        "is_premium": False,
        "category": "simple"
    },
    "three_cards": {
        "name": "Путь",
        "description": "Три карты: прошлое, настоящее, будущее",
        "card_count": 3,
        "positions": ["Прошлое", "Настоящее", "Будущее"],
        "is_premium": False,
        "category": "simple"
    },
    "love_spread": {
        "name": "Отношения",
        "description": "Расклад для понимания отношений",
        "card_count": 5,
        "positions": ["Ваши чувства", "Чувства партнера", "Связь между вами", "Препятствия", "Совет"],
        "is_premium": True,
        "category": "relationship"
    },
    "shadow_light": {
        "name": "Тень и Свет",
        "description": "Анализ сильных и слабых сторон",
        "card_count": 4,
        "positions": ["Ваша сила", "Скрытый потенциал", "Слабая сторона", "Совет для роста"],
        "is_premium": True,
        "category": "deep"
    },
    "celtic_cross": {
        "name": "Кельтский Крест",
        "description": "Глубокий анализ ситуации",
        "card_count": 10,
        "positions": ["Суть", "Помеха", "Основание", "Прошлое", "Корона", "Будущее", "Вы", "Окружение", "Страхи", "Итог"],
        "is_premium": True,
        "category": "complex"
    },
    "chakra_spread": {
        "name": "Чакровый расклад",
        "description": "Энергетический баланс",
        "card_count": 7,
        "positions": ["Муладхара", "Свадхистана", "Манипура", "Анахата", "Вишудха", "Аджна", "Сахасрара"],
        "is_premium": True,
        "category": "spiritual"
    }
}

ZODIAC_SIGNS = {
    "aries": {"name": "Овен", "dates": "21.03 - 19.04", "element": "Огонь"},
    "taurus": {"name": "Телец", "dates": "20.04 - 20.05", "element": "Земля"},
    "gemini": {"name": "Близнецы", "dates": "21.05 - 20.06", "element": "Воздух"},
    "cancer": {"name": "Рак", "dates": "21.06 - 22.07", "element": "Вода"},
    "leo": {"name": "Лев", "dates": "23.07 - 22.08", "element": "Огонь"},
    "virgo": {"name": "Дева", "dates": "23.08 - 22.09", "element": "Земля"},
    "libra": {"name": "Весы", "dates": "23.09 - 22.10", "element": "Воздух"},
    "scorpio": {"name": "Скорпион", "dates": "23.10 - 21.11", "element": "Вода"},
    "sagittarius": {"name": "Стрелец", "dates": "22.11 - 21.12", "element": "Огонь"},
    "capricorn": {"name": "Козерог", "dates": "22.12 - 19.01", "element": "Земля"},
    "aquarius": {"name": "Водолей", "dates": "20.01 - 18.02", "element": "Воздух"},
    "pisces": {"name": "Рыбы", "dates": "19.02 - 20.03", "element": "Вода"}
} 
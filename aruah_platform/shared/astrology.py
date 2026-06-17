"""
Модуль астрологии для платформы АРУАХ
"""

from datetime import date, time
from typing import Dict, Any, Optional
import random


class AstrologyCalculator:
    """Калькулятор астрологических данных"""
    
    @staticmethod
    def get_zodiac_sign(birth_date: date) -> str:
        """Определить знак зодиака по дате рождения"""
        month = birth_date.month
        day = birth_date.day
        
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "aquarius"
        else:
            return "pisces"
    
    @staticmethod
    def calculate_natal_chart(birth_date: date, birth_time: Optional[time] = None, 
                            birth_place: Optional[str] = None) -> Dict[str, Any]:
        """Расчёт натальной карты (упрощённая версия)"""
        # В реальной реализации здесь будет интеграция с swisseph
        # Пока используем упрощённые расчёты
        
        sun_sign = AstrologyCalculator.get_zodiac_sign(birth_date)
        
        # Упрощённые расчёты для других планет
        planets = {
            'sun': sun_sign,
            'moon': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']),
            'mercury': sun_sign,  # Меркурий обычно близко к Солнцу
            'venus': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                  'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']),
            'mars': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']),
            'jupiter': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']),
            'saturn': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                   'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']),
            'uranus': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                   'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']),
            'neptune': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']),
            'pluto': random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                  'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'])
        }
        
        return {
            'birth_date': birth_date,
            'birth_time': birth_time,
            'birth_place': birth_place,
            'planets': planets
        }
    
    @staticmethod
    def get_rising_sign(birth_time: Optional[time] = None) -> str:
        """Определить восходящий знак (упрощённо)"""
        if not birth_time:
            return random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'])
        
        # Упрощённый расчёт на основе времени рождения
        hour = birth_time.hour
        if 6 <= hour < 8:
            return 'aries'
        elif 8 <= hour < 10:
            return 'taurus'
        elif 10 <= hour < 12:
            return 'gemini'
        elif 12 <= hour < 14:
            return 'cancer'
        elif 14 <= hour < 16:
            return 'leo'
        elif 16 <= hour < 18:
            return 'virgo'
        elif 18 <= hour < 20:
            return 'libra'
        elif 20 <= hour < 22:
            return 'scorpio'
        elif 22 <= hour < 24 or 0 <= hour < 2:
            return 'sagittarius'
        elif 2 <= hour < 4:
            return 'capricorn'
        else:  # 4 <= hour < 6
            return 'aquarius'


class AstrologyInterpreter:
    """Интерпретатор астрологических данных"""
    
    ZODIAC_DESCRIPTIONS = {
        'aries': {
            'name': 'Овен',
            'name_kz': 'Қозы',
            'element': 'Огонь',
            'planet': 'Марс',
            'traits': 'Энергичный, инициативный, лидер, импульсивный',
            'strengths': 'Смелость, энтузиазм, честность, лидерство',
            'challenges': 'Нетерпеливость, агрессивность, эгоизм',
            'compatible': ['leo', 'sagittarius', 'gemini', 'aquarius'],
            'career': 'Лидерство, спорт, военное дело, предпринимательство',
            'love': 'Страстный, прямой, нуждается в независимости'
        },
        'taurus': {
            'name': 'Телец',
            'name_kz': 'Бұзау',
            'element': 'Земля',
            'planet': 'Венера',
            'traits': 'Стабильный, практичный, терпеливый, упрямый',
            'strengths': 'Надёжность, терпение, практичность, чувственность',
            'challenges': 'Упрямство, медлительность, материализм',
            'compatible': ['virgo', 'capricorn', 'cancer', 'pisces'],
            'career': 'Финансы, искусство, сельское хозяйство, дизайн',
            'love': 'Преданный, романтичный, ценит стабильность'
        },
        'gemini': {
            'name': 'Близнецы',
            'name_kz': 'Егіздер',
            'element': 'Воздух',
            'planet': 'Меркурий',
            'traits': 'Общительный, любознательный, изменчивый, интеллектуальный',
            'strengths': 'Коммуникабельность, адаптивность, интеллект, юмор',
            'challenges': 'Поверхностность, непостоянство, нервозность',
            'compatible': ['libra', 'aquarius', 'aries', 'leo'],
            'career': 'Журналистика, преподавание, торговля, IT',
            'love': 'Игривый, общительный, нуждается в интеллектуальной связи'
        },
        'cancer': {
            'name': 'Рак',
            'name_kz': 'Шаян',
            'element': 'Вода',
            'planet': 'Луна',
            'traits': 'Эмоциональный, заботливый, интуитивный, чувствительный',
            'strengths': 'Забота, интуиция, преданность, творчество',
            'challenges': 'Переменчивость настроения, обидчивость, зависимость',
            'compatible': ['scorpio', 'pisces', 'taurus', 'virgo'],
            'career': 'Медицина, психология, кулинария, недвижимость',
            'love': 'Заботливый, преданный, нуждается в эмоциональной безопасности'
        },
        'leo': {
            'name': 'Лев',
            'name_kz': 'Арыстан',
            'element': 'Огонь',
            'planet': 'Солнце',
            'traits': 'Гордый, творческий, щедрый, драматичный',
            'strengths': 'Лидерство, творчество, щедрость, уверенность',
            'challenges': 'Гордыня, эгоцентризм, драматизм',
            'compatible': ['aries', 'sagittarius', 'gemini', 'libra'],
            'career': 'Искусство, развлечения, политика, управление',
            'love': 'Романтичный, щедрый, нуждается в восхищении'
        },
        'virgo': {
            'name': 'Дева',
            'name_kz': 'Бикеш',
            'element': 'Земля',
            'planet': 'Меркурий',
            'traits': 'Аналитичный, практичный, перфекционист, скромный',
            'strengths': 'Аналитичность, практичность, забота, надёжность',
            'challenges': 'Критичность, перфекционизм, тревожность',
            'compatible': ['taurus', 'capricorn', 'cancer', 'scorpio'],
            'career': 'Медицина, аналитика, исследования, обслуживание',
            'love': 'Преданный, практичный, выражает любовь через заботу'
        },
        'libra': {
            'name': 'Весы',
            'name_kz': 'Таразы',
            'element': 'Воздух',
            'planet': 'Венера',
            'traits': 'Дипломатичный, справедливый, романтичный, нерешительный',
            'strengths': 'Дипломатия, справедливость, эстетика, обаяние',
            'challenges': 'Нерешительность, зависимость, избегание конфликтов',
            'compatible': ['gemini', 'aquarius', 'leo', 'sagittarius'],
            'career': 'Право, дизайн, дипломатия, консультирование',
            'love': 'Романтичный, справедливый, нуждается в гармонии'
        },
        'scorpio': {
            'name': 'Скорпион',
            'name_kz': 'Шаян',
            'element': 'Вода',
            'planet': 'Плутон',
            'traits': 'Интенсивный, страстный, трансформационный, скрытный',
            'strengths': 'Интенсивность, страсть, интуиция, сила',
            'challenges': 'Ревность, скрытность, манипулятивность',
            'compatible': ['cancer', 'pisces', 'virgo', 'capricorn'],
            'career': 'Психология, медицина, исследования, криминалистика',
            'love': 'Страстный, преданный, нуждается в глубокой связи'
        },
        'sagittarius': {
            'name': 'Стрелец',
            'name_kz': 'Жауынгер',
            'element': 'Огонь',
            'planet': 'Юпитер',
            'traits': 'Авантюрный, философский, оптимистичный, прямолинейный',
            'strengths': 'Оптимизм, философия, авантюризм, честность',
            'challenges': 'Нетерпеливость, прямолинейность, непостоянство',
            'compatible': ['aries', 'leo', 'libra', 'aquarius'],
            'career': 'Путешествия, преподавание, философия, спорт',
            'love': 'Авантюрный, честный, нуждается в свободе'
        },
        'capricorn': {
            'name': 'Козерог',
            'name_kz': 'Ешкі',
            'element': 'Земля',
            'planet': 'Сатурн',
            'traits': 'Амбициозный, дисциплинированный, практичный, консервативный',
            'strengths': 'Амбициозность, дисциплина, ответственность, практичность',
            'challenges': 'Пессимизм, консерватизм, эмоциональная закрытость',
            'compatible': ['taurus', 'virgo', 'scorpio', 'pisces'],
            'career': 'Управление, финансы, политика, строительство',
            'love': 'Преданный, ответственный, выражает любовь через заботу'
        },
        'aquarius': {
            'name': 'Водолей',
            'name_kz': 'Суқұйғыш',
            'element': 'Воздух',
            'planet': 'Уран',
            'traits': 'Инновационный, независимый, гуманистичный, эксцентричный',
            'strengths': 'Инновационность, независимость, гуманизм, оригинальность',
            'challenges': 'Непредсказуемость, отстранённость, упрямство',
            'compatible': ['gemini', 'libra', 'aries', 'sagittarius'],
            'career': 'Технологии, наука, гуманитарная работа, изобретения',
            'love': 'Независимый, дружелюбный, нуждается в интеллектуальной связи'
        },
        'pisces': {
            'name': 'Рыбы',
            'name_kz': 'Балықтар',
            'element': 'Вода',
            'planet': 'Нептун',
            'traits': 'Интуитивный, сострадательный, творческий, мечтательный',
            'strengths': 'Интуиция, сострадание, творчество, эмпатия',
            'challenges': 'Эскапизм, жертвенность, нерешительность',
            'compatible': ['cancer', 'scorpio', 'taurus', 'capricorn'],
            'career': 'Искусство, медицина, психология, духовность',
            'love': 'Романтичный, сострадательный, нуждается в духовной связи'
        }
    }
    
    @staticmethod
    def interpret_sun_sign(zodiac_sign: str) -> str:
        """Интерпретация солнечного знака"""
        sign_data = AstrologyInterpreter.ZODIAC_DESCRIPTIONS.get(zodiac_sign, {})
        if not sign_data:
            return "Неизвестный знак зодиака"
        
        return f"""
🌟 **{sign_data['name']} ({sign_data['name_kz']})**

**Элемент:** {sign_data['element']}
**Планета-управитель:** {sign_data['planet']}

**Основные черты:**
{sign_data['traits']}

**Сильные стороны:**
{sign_data['strengths']}

**На что обратить внимание:**
{sign_data['challenges']}

**Совместимость:**
Лучше всего с {', '.join(sign_data['compatible'])} знаками

**Карьера:**
{sign_data['career']}

**В любви:**
{sign_data['love']}
        """.strip()
    
    @staticmethod
    def generate_daily_forecast(zodiac_sign: str) -> str:
        """Генерация дневного прогноза"""
        sign_data = AstrologyInterpreter.ZODIAC_DESCRIPTIONS.get(zodiac_sign, {})
        sign_name = sign_data.get('name', 'Неизвестный знак')
        
        forecasts = [
            f"Сегодня {sign_name} ощутит прилив энергии и вдохновения. Время для новых начинаний!",
            f"День благоприятен для {sign_name} в вопросах творчества и самовыражения.",
            f"Звезды советуют {sign_name} обратить внимание на отношения и близких людей.",
            f"Прекрасный день для новых начинаний, дорогой {sign_name}. Доверьтесь интуиции!",
            f"Сегодня {sign_name} может получить важные новости или встретить интересного человека.",
            f"Энергия дня поможет {sign_name} решить давние проблемы и двигаться вперед.",
            f"Время для {sign_name} сосредоточиться на здоровье и внутренней гармонии."
        ]
        
        return f"🌟 **Прогноз для {sign_name}**\n\n{random.choice(forecasts)}"
    
    @staticmethod
    def generate_weekly_forecast(zodiac_sign: str) -> str:
        """Генерация недельного прогноза"""
        sign_data = AstrologyInterpreter.ZODIAC_DESCRIPTIONS.get(zodiac_sign, {})
        sign_name = sign_data.get('name', 'Неизвестный знак')
        
        return f"""
📅 **Недельный прогноз для {sign_name}**

**Понедельник-вторник:** Время для планирования и постановки целей
**Среда-четверг:** Благоприятный период для общения и новых знакомств
**Пятница-суббота:** Отличное время для творчества и самовыражения
**Воскресенье:** День отдыха и размышлений

**Общий совет недели:**
Доверьтесь своей интуиции и не бойтесь перемен. Звезды на вашей стороне!
        """.strip()
    
    @staticmethod
    def check_compatibility(sign1: str, sign2: str) -> str:
        """Проверка совместимости знаков зодиака"""
        sign1_data = AstrologyInterpreter.ZODIAC_DESCRIPTIONS.get(sign1, {})
        sign2_data = AstrologyInterpreter.ZODIAC_DESCRIPTIONS.get(sign2, {})
        
        if not sign1_data or not sign2_data:
            return "Недостаточно данных для анализа совместимости"
        
        compatible_signs = sign1_data.get('compatible', [])
        compatibility = "высокая" if sign2 in compatible_signs else "средняя"
        
        return f"""
💕 **Совместимость: {sign1_data['name']} и {sign2_data['name']}**

**Уровень совместимости:** {compatibility}

**Общие черты:**
Оба знака обладают {sign1_data['element']} энергией, что создает {compatibility} совместимость.

**Рекомендации:**
• Уважайте различия друг друга
• Ищите общие интересы
• Общайтесь открыто и честно
• Поддерживайте друг друга в развитии

**Совет:**
Совместимость в астрологии - это только отправная точка. Настоящая гармония строится на взаимном уважении и любви.
        """.strip()


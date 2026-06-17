"""
Модуль Human Design для платформы АРУАХ
"""

from datetime import date, time
from typing import Dict, Any, List, Optional
import random


class HumanDesignCalculator:
    """Калькулятор Human Design"""
    
    TYPES = {
        'generator': {
            'name': 'Генератор',
            'name_kz': 'Генератор',
            'percentage': 37,
            'strategy': 'Отвечать',
            'authority': 'Сакральная',
            'not_self_theme': 'Фрустрация',
            'description': 'Энергетический тип, создающий и поддерживающий жизнь'
        },
        'manifesting_generator': {
            'name': 'Манифестирующий Генератор',
            'name_kz': 'Манифестірующий Генератор',
            'percentage': 8,
            'strategy': 'Информировать, затем отвечать',
            'authority': 'Сакральная',
            'not_self_theme': 'Гнев',
            'description': 'Гибридный тип, сочетающий качества Манифестора и Генератора'
        },
        'projector': {
            'name': 'Проектор',
            'name_kz': 'Проектор',
            'percentage': 21,
            'strategy': 'Ждать приглашения',
            'authority': 'Эмоциональная, Сакральная, Селезеночная, G-центр',
            'not_self_theme': 'Горечь',
            'description': 'Неэнергетический тип, направляющий и управляющий'
        },
        'reflector': {
            'name': 'Рефлектор',
            'name_kz': 'Рефлектор',
            'percentage': 1,
            'strategy': 'Ждать 28 дней',
            'authority': 'Лунная',
            'not_self_theme': 'Разочарование',
            'description': 'Редкий тип, отражающий энергию окружающих'
        }
    }
    
    CENTERS = {
        'head': {'name': 'Голова', 'function': 'Вдохновение, давление'},
        'ajna': {'name': 'Аджна', 'function': 'Ментальная осознанность'},
        'throat': {'name': 'Горло', 'function': 'Коммуникация, действие'},
        'g_center': {'name': 'G-центр', 'function': 'Любовь, направление, идентичность'},
        'heart': {'name': 'Сердце', 'function': 'Воля, эго'},
        'solar_plexus': {'name': 'Солнечное сплетение', 'function': 'Эмоции, страсть'},
        'sacral': {'name': 'Сакральная', 'function': 'Жизненная сила, сексуальность'},
        'spleen': {'name': 'Селезенка', 'function': 'Интуиция, здоровье'},
        'root': {'name': 'Корень', 'function': 'Адреналин, давление'}
    }
    
    @staticmethod
    def calculate_human_design(birth_date: date, birth_time: Optional[time] = None, 
                             birth_place: Optional[str] = None) -> Dict[str, Any]:
        """Расчёт Human Design (упрощённая версия)"""
        # В реальной реализации здесь будет интеграция с библиотекой Human Design
        # Пока используем упрощённые расчёты на основе даты рождения
        
        day, month, year = birth_date.day, birth_date.month, birth_date.year
        
        # Определяем тип (упрощённо)
        type_value = (day + month + year) % 4
        type_keys = ['generator', 'manifesting_generator', 'projector', 'reflector']
        hd_type = type_keys[type_value]
        
        # Определяем определённые центры (упрощённо)
        defined_centers = []
        center_keys = list(HumanDesignCalculator.CENTERS.keys())
        
        for i, center in enumerate(center_keys):
            if (day + month + year + i) % 3 == 0:
                defined_centers.append(center)
        
        undefined_centers = [center for center in center_keys if center not in defined_centers]
        
        # Определяем профиль (1-6)
        profile = ((day + month) % 6) + 1
        
        # Определяем авторитет
        if hd_type in ['generator', 'manifesting_generator']:
            authority = 'Сакральная'
        elif hd_type == 'projector':
            authorities = ['Эмоциональная', 'Сакральная', 'Селезеночная', 'G-центр']
            authority = random.choice(authorities)
        elif hd_type == 'reflector':
            authority = 'Лунная'
        else:
            authority = 'Неопределённая'
        
        return {
            'type': hd_type,
            'profile': profile,
            'authority': authority,
            'defined_centers': defined_centers,
            'undefined_centers': undefined_centers,
            'strategy': HumanDesignCalculator.TYPES[hd_type]['strategy'],
            'not_self_theme': HumanDesignCalculator.TYPES[hd_type]['not_self_theme']
        }
    
    @staticmethod
    def calculate_gates(birth_date: date) -> List[int]:
        """Расчёт определённых ворот (упрощённо)"""
        day, month, year = birth_date.day, birth_date.month, birth_date.year
        
        # В реальной реализации здесь будет сложный расчёт на основе времени и места рождения
        # Пока используем упрощённый алгоритм
        gates = []
        
        for i in range(1, 65):  # 64 ворот в Human Design
            if (day + month + year + i) % 7 == 0:
                gates.append(i)
        
        return gates[:8]  # Ограничиваем количество ворот


class HumanDesignInterpreter:
    """Интерпретатор Human Design"""
    
    @staticmethod
    def interpret_human_design(hd_data: Dict[str, Any]) -> str:
        """Интерпретация Human Design"""
        type_info = HumanDesignCalculator.TYPES[hd_data['type']]
        
        interpretation = f"""
🧬 **HUMAN DESIGN**

**Тип:** {type_info['name']} ({type_info['name_kz']})
**Профиль:** {hd_data['profile']}/6
**Стратегия:** {hd_data['strategy']}
**Авторитет:** {hd_data['authority']}

**Описание:**
{type_info['description']}

**Определённые центры:**
"""
        
        for center in hd_data['defined_centers']:
            center_info = HumanDesignCalculator.CENTERS.get(center, {})
            interpretation += f"• {center_info.get('name', center)} - {center_info.get('function', '')}\n"
        
        interpretation += f"\n**Неопределённые центры:**\n"
        for center in hd_data['undefined_centers']:
            center_info = HumanDesignCalculator.CENTERS.get(center, {})
            interpretation += f"• {center_info.get('name', center)} - {center_info.get('function', '')}\n"
        
        interpretation += f"\n**Тема не-себя:** {hd_data['not_self_theme']}\n"
        
        return interpretation
    
    @staticmethod
    def get_type_advice(hd_data: Dict[str, Any]) -> str:
        """Получить советы для типа"""
        type_info = HumanDesignCalculator.TYPES[hd_data['type']]
        
        advice = f"**СОВЕТЫ ДЛЯ {type_info['name'].upper()}:**\n\n"
        
        if hd_data['type'] == 'generator':
            advice += """
• **Стратегия:** Отвечайте на вопросы и предложения
• **Авторитет:** Слушайте свой сакральный отклик (да/нет в животе)
• **Избегайте:** Инициировать действия самостоятельно
• **Практика:** Задавайте себе вопросы и ждите ответа от тела
• **Карьера:** Работа, которая приносит удовлетворение
            """
        elif hd_data['type'] == 'manifesting_generator':
            advice += """
• **Стратегия:** Информируйте о своих планах, затем отвечайте
• **Авторитет:** Слушайте сакральный отклик
• **Избегайте:** Действовать без информирования
• **Практика:** Сообщайте о своих намерениях
• **Карьера:** Разнообразная деятельность, приносящая удовлетворение
            """
        elif hd_data['type'] == 'projector':
            advice += """
• **Стратегия:** Ждите приглашения
• **Авторитет:** Следуйте своему внутреннему авторитету
• **Избегайте:** Предлагать себя без приглашения
• **Практика:** Развивайте мудрость и ждите признания
• **Карьера:** Направление и управление другими
            """
        elif hd_data['type'] == 'reflector':
            advice += """
• **Стратегия:** Ждите 28 дней перед принятием решений
• **Авторитет:** Лунная авторитет
• **Избегайте:** Принимать решения быстро
• **Практика:** Наблюдайте за лунным циклом
• **Карьера:** Работа, отражающая окружающую среду
            """
        
        return advice.strip()
    
    @staticmethod
    def get_center_advice(hd_data: Dict[str, Any]) -> str:
        """Получить советы по центрам"""
        advice = "**СОВЕТЫ ПО ЦЕНТРАМ:**\n\n"
        
        # Определённые центры
        advice += "**Определённые центры (ваши сильные стороны):**\n"
        for center in hd_data['defined_centers']:
            center_info = HumanDesignCalculator.CENTERS.get(center, {})
            advice += f"• {center_info.get('name', center)}: {center_info.get('function', '')}\n"
        
        advice += "\n**Неопределённые центры (области для развития):**\n"
        for center in hd_data['undefined_centers']:
            center_info = HumanDesignCalculator.CENTERS.get(center, {})
            advice += f"• {center_info.get('name', center)}: {center_info.get('function', '')}\n"
        
        advice += "\n**Общие рекомендации:**\n"
        advice += "• Развивайте свои определённые центры\n"
        advice += "• Будьте осторожны с неопределёнными центрами\n"
        advice += "• Не принимайте решения из неопределённых центров\n"
        
        return advice
    
    @staticmethod
    def get_profile_meaning(profile: int) -> str:
        """Получить значение профиля"""
        profiles = {
            1: {
                'name': 'Исследователь',
                'description': 'Глубокое изучение и исследование',
                'advice': 'Изучайте всё досконально, будьте экспертом'
            },
            2: {
                'name': 'Отшельник',
                'description': 'Естественная мудрость и таланты',
                'advice': 'Ждите, когда вас найдут, не предлагайте себя'
            },
            3: {
                'name': 'Мученик',
                'description': 'Обучение через опыт и ошибки',
                'advice': 'Экспериментируйте, учитесь на ошибках'
            },
            4: {
                'name': 'Оппортунист',
                'description': 'Естественные друзья и возможности',
                'advice': 'Используйте свои связи и дружбы'
            },
            5: {
                'name': 'Еретик',
                'description': 'Универсальное решение проблем',
                'advice': 'Предлагайте практические решения'
            },
            6: {
                'name': 'Роль Модели',
                'description': 'Три фазы жизни: исследование, эксперимент, вдохновение',
                'advice': 'Будьте примером для других'
            }
        }
        
        profile_info = profiles.get(profile, {})
        
        return f"""
**Профиль {profile}: {profile_info.get('name', 'Неизвестно')}**

**Описание:**
{profile_info.get('description', '')}

**Совет:**
{profile_info.get('advice', '')}
        """.strip()
    
    @staticmethod
    def get_authority_advice(authority: str) -> str:
        """Получить советы по авторитету"""
        authorities = {
            'Сакральная': {
                'description': 'Отклик в области живота (да/нет)',
                'practice': 'Задавайте себе вопросы и ждите ответа от тела'
            },
            'Эмоциональная': {
                'description': 'Эмоциональная волна, нужно время для ясности',
                'practice': 'Ждите эмоциональной ясности перед принятием решений'
            },
            'Селезеночная': {
                'description': 'Мгновенная интуиция и инстинкты',
                'practice': 'Доверяйте первому впечатлению'
            },
            'G-центр': {
                'description': 'Сердечный отклик и любовь',
                'practice': 'Слушайте сердце и чувства'
            },
            'Лунная': {
                'description': '28-дневный цикл для принятия решений',
                'practice': 'Ждите полного лунного цикла'
            }
        }
        
        auth_info = authorities.get(authority, {})
        
        return f"""
**Авторитет: {authority}**

**Описание:**
{auth_info.get('description', '')}

**Практика:**
{auth_info.get('practice', '')}
        """.strip()

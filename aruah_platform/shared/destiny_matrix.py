"""
Модуль матрицы судьбы для платформы АРУАХ
"""

from datetime import date
from typing import Dict, Any, List
import random


class DestinyMatrixCalculator:
    """Калькулятор матрицы судьбы"""
    
    ARCANA_MEANINGS = {
        0: {"name": "Дурак", "meaning": "Новые начинания, спонтанность, свобода"},
        1: {"name": "Маг", "meaning": "Сила воли, проявление, концентрация"},
        2: {"name": "Верховная Жрица", "meaning": "Интуиция, подсознание, мудрость"},
        3: {"name": "Императрица", "meaning": "Плодородие, женственность, красота"},
        4: {"name": "Император", "meaning": "Авторитет, структура, контроль"},
        5: {"name": "Иерофант", "meaning": "Традиции, духовность, обучение"},
        6: {"name": "Влюблённые", "meaning": "Любовь, выбор, гармония"},
        7: {"name": "Колесница", "meaning": "Победа, контроль, направление"},
        8: {"name": "Сила", "meaning": "Внутренняя сила, мужество, терпение"},
        9: {"name": "Отшельник", "meaning": "Поиск истины, мудрость, одиночество"},
        10: {"name": "Колесо Фортуны", "meaning": "Судьба, циклы, перемены"},
        11: {"name": "Справедливость", "meaning": "Баланс, справедливость, карма"},
        12: {"name": "Повешенный", "meaning": "Жертва, сдача, новый взгляд"},
        13: {"name": "Смерть", "meaning": "Трансформация, конец, новое начало"},
        14: {"name": "Умеренность", "meaning": "Баланс, терпение, исцеление"},
        15: {"name": "Дьявол", "meaning": "Искушения, ограничения, материализм"},
        16: {"name": "Башня", "meaning": "Разрушение, освобождение, пробуждение"},
        17: {"name": "Звезда", "meaning": "Надежда, вдохновение, духовность"},
        18: {"name": "Луна", "meaning": "Иллюзии, подсознание, интуиция"},
        19: {"name": "Солнце", "meaning": "Радость, успех, жизненная сила"},
        20: {"name": "Суд", "meaning": "Воскрешение, прощение, обновление"},
        21: {"name": "Мир", "meaning": "Завершение, достижение, гармония"}
    }
    
    @staticmethod
    def calculate_destiny_matrix(birth_date: date) -> Dict[str, Any]:
        """Расчёт полной матрицы судьбы (40+ точек)"""
        day, month, year = birth_date.day, birth_date.month, birth_date.year
        full_year = year
        short_year = year % 100
        
        matrix = {
            # Основные точки (22 аркана)
            'personal_destiny': (day + month + full_year) % 22,
            'social_destiny': (day + month + short_year) % 22,
            'spiritual_destiny': (month + full_year) % 22,
            'karma_mother': (day + month) % 22,
            'karma_father': (day + full_year) % 22,
            
            # Дополнительные точки
            'money_energy': (day * 2 + month) % 22,
            'health_energy': (month * 2 + full_year) % 22,
            'talents': (day + month * 2) % 22,
            'relationships': (month + full_year * 2) % 22,
            'career': (day * 3 + month) % 22,
            'family': (month * 3 + full_year) % 22,
            'children': (day + month * 3) % 22,
            'friends': (month + full_year * 3) % 22,
            'travel': (day * 4 + month) % 22,
            'home': (month * 4 + full_year) % 22,
            'creativity': (day + month * 4) % 22,
            'intuition': (month + full_year * 4) % 22,
            'wisdom': (day * 5 + month) % 22,
            'power': (month * 5 + full_year) % 22,
            'love': (day + month * 5) % 22,
            'sexuality': (month + full_year * 5) % 22,
            'communication': (day * 6 + month) % 22,
            'learning': (month * 6 + full_year) % 22,
            'teaching': (day + month * 6) % 22,
            'healing': (month + full_year * 6) % 22,
            'leadership': (day * 7 + month) % 22,
            'service': (month * 7 + full_year) % 22,
            'sacrifice': (day + month * 7) % 22,
            'transformation': (month + full_year * 7) % 22,
            'freedom': (day * 8 + month) % 22,
            'discipline': (month * 8 + full_year) % 22,
            'justice': (day + month * 8) % 22,
            'balance': (month + full_year * 8) % 22,
            'harmony': (day * 9 + month) % 22,
            'completion': (month * 9 + full_year) % 22,
            'new_beginning': (day + month * 9) % 22,
            'enlightenment': (month + full_year * 9) % 22,
            'mastery': (day * 10 + month) % 22,
            'perfection': (month * 10 + full_year) % 22,
            'transcendence': (day + month * 10) % 22,
            'cosmic_consciousness': (month + full_year * 10) % 22
        }
        
        return matrix
    
    @staticmethod
    def calculate_compatibility_matrix(birth_date1: date, birth_date2: date) -> Dict[str, Any]:
        """Расчёт совместимости двух матриц"""
        matrix1 = DestinyMatrixCalculator.calculate_destiny_matrix(birth_date1)
        matrix2 = DestinyMatrixCalculator.calculate_destiny_matrix(birth_date2)
        
        compatibility = {
            'personal_destiny': abs(matrix1['personal_destiny'] - matrix2['personal_destiny']),
            'social_destiny': abs(matrix1['social_destiny'] - matrix2['social_destiny']),
            'spiritual_destiny': abs(matrix1['spiritual_destiny'] - matrix2['spiritual_destiny']),
            'love': abs(matrix1['love'] - matrix2['love']),
            'relationships': abs(matrix1['relationships'] - matrix2['relationships']),
            'communication': abs(matrix1['communication'] - matrix2['communication'])
        }
        
        # Общий балл совместимости (чем меньше, тем лучше)
        total_compatibility = sum(compatibility.values())
        
        if total_compatibility <= 10:
            compatibility_level = "Очень высокая"
        elif total_compatibility <= 20:
            compatibility_level = "Высокая"
        elif total_compatibility <= 30:
            compatibility_level = "Средняя"
        else:
            compatibility_level = "Низкая"
        
        return {
            'compatibility_scores': compatibility,
            'total_score': total_compatibility,
            'compatibility_level': compatibility_level
        }


class DestinyMatrixInterpreter:
    """Интерпретатор матрицы судьбы"""
    
    POSITION_NAMES = {
        'personal_destiny': 'Личное предназначение',
        'social_destiny': 'Социальное предназначение',
        'spiritual_destiny': 'Духовное предназначение',
        'karma_mother': 'Карма матери',
        'karma_father': 'Карма отца',
        'money_energy': 'Энергия денег',
        'health_energy': 'Энергия здоровья',
        'talents': 'Таланты',
        'relationships': 'Отношения',
        'career': 'Карьера',
        'family': 'Семья',
        'children': 'Дети',
        'friends': 'Друзья',
        'travel': 'Путешествия',
        'home': 'Дом',
        'creativity': 'Творчество',
        'intuition': 'Интуиция',
        'wisdom': 'Мудрость',
        'power': 'Власть',
        'love': 'Любовь',
        'sexuality': 'Сексуальность',
        'communication': 'Коммуникация',
        'learning': 'Обучение',
        'teaching': 'Преподавание',
        'healing': 'Исцеление',
        'leadership': 'Лидерство',
        'service': 'Служение',
        'sacrifice': 'Жертвенность',
        'transformation': 'Трансформация',
        'freedom': 'Свобода',
        'discipline': 'Дисциплина',
        'justice': 'Справедливость',
        'balance': 'Баланс',
        'harmony': 'Гармония',
        'completion': 'Завершение',
        'new_beginning': 'Новое начало',
        'enlightenment': 'Просветление',
        'mastery': 'Мастерство',
        'perfection': 'Совершенство',
        'transcendence': 'Трансценденция',
        'cosmic_consciousness': 'Космическое сознание'
    }
    
    @staticmethod
    def interpret_destiny_matrix(matrix: Dict[str, int]) -> str:
        """Интерпретация матрицы судьбы"""
        interpretation = "🌟 **МАТРИЦА СУДЬБЫ** 🌟\n\n"
        
        # Основные точки
        interpretation += "**ОСНОВНЫЕ ТОЧКИ:**\n"
        main_points = ['personal_destiny', 'social_destiny', 'spiritual_destiny', 
                      'karma_mother', 'karma_father']
        
        for point in main_points:
            arcana_num = matrix[point]
            arcana = DestinyMatrixCalculator.ARCANA_MEANINGS.get(arcana_num, {})
            position_name = DestinyMatrixInterpreter.POSITION_NAMES.get(point, point)
            
            interpretation += f"**{position_name}:** {arcana.get('name', 'Неизвестно')}\n"
            interpretation += f"💫 {arcana.get('meaning', '')}\n\n"
        
        # Дополнительные точки
        interpretation += "**ДОПОЛНИТЕЛЬНЫЕ ТОЧКИ:**\n"
        additional_points = ['money_energy', 'health_energy', 'talents', 'relationships', 
                           'career', 'love', 'communication', 'creativity']
        
        for point in additional_points:
            arcana_num = matrix[point]
            arcana = DestinyMatrixCalculator.ARCANA_MEANINGS.get(arcana_num, {})
            position_name = DestinyMatrixInterpreter.POSITION_NAMES.get(point, point)
            
            interpretation += f"**{position_name}:** {arcana.get('name', 'Неизвестно')}\n"
        
        # Общий анализ
        interpretation += "\n**ОБЩИЙ АНАЛИЗ:**\n"
        
        # Анализ основных арканов
        main_arcanas = [matrix[point] for point in main_points]
        most_common = max(set(main_arcanas), key=main_arcanas.count)
        
        interpretation += f"• Доминирующий аркан: {DestinyMatrixCalculator.ARCANA_MEANINGS.get(most_common, {}).get('name', 'Неизвестно')}\n"
        
        # Анализ энергии
        energy_points = [matrix['money_energy'], matrix['health_energy'], matrix['power']]
        avg_energy = sum(energy_points) / len(energy_points)
        
        if avg_energy >= 15:
            interpretation += "• Высокая жизненная энергия и потенциал\n"
        elif avg_energy >= 10:
            interpretation += "• Умеренная жизненная энергия\n"
        else:
            interpretation += "• Нужно работать над повышением энергии\n"
        
        # Анализ отношений
        relationship_points = [matrix['love'], matrix['relationships'], matrix['communication']]
        avg_relationships = sum(relationship_points) / len(relationship_points)
        
        if avg_relationships >= 15:
            interpretation += "• Отличные способности к отношениям\n"
        elif avg_relationships >= 10:
            interpretation += "• Хорошие способности к отношениям\n"
        else:
            interpretation += "• Нужно развивать навыки общения\n"
        
        return interpretation
    
    @staticmethod
    def interpret_compatibility(compatibility_data: Dict[str, Any]) -> str:
        """Интерпретация совместимости матриц"""
        level = compatibility_data['compatibility_level']
        total_score = compatibility_data['total_score']
        
        interpretation = f"""
💕 **СОВМЕСТИМОСТЬ МАТРИЦ СУДЬБЫ**

**Общий уровень:** {level} ({total_score}/60)

**Детальный анализ:**
"""
        
        scores = compatibility_data['compatibility_scores']
        
        for aspect, score in scores.items():
            aspect_name = DestinyMatrixInterpreter.POSITION_NAMES.get(aspect, aspect)
            
            if score <= 2:
                level_text = "Отличная"
                emoji = "💚"
            elif score <= 5:
                level_text = "Хорошая"
                emoji = "💛"
            elif score <= 8:
                level_text = "Средняя"
                emoji = "🟡"
            else:
                level_text = "Низкая"
                emoji = "🔴"
            
            interpretation += f"{emoji} **{aspect_name}:** {level_text} совместимость\n"
        
        # Общие рекомендации
        interpretation += "\n**РЕКОМЕНДАЦИИ:**\n"
        
        if level == "Очень высокая":
            interpretation += "• У вас отличная совместимость! Развивайте отношения\n"
            interpretation += "• Поддерживайте друг друга в духовном росте\n"
        elif level == "Высокая":
            interpretation += "• Хорошая совместимость, есть потенциал для развития\n"
            interpretation += "• Работайте над слабыми аспектами\n"
        elif level == "Средняя":
            interpretation += "• Совместимость требует работы и понимания\n"
            interpretation += "• Фокусируйтесь на сильных сторонах\n"
        else:
            interpretation += "• Совместимость требует много усилий\n"
            interpretation += "• Рассмотрите возможность работы с тарологом\n"
        
        return interpretation
    
    @staticmethod
    def get_destiny_advice(matrix: Dict[str, int]) -> str:
        """Получить советы на основе матрицы судьбы"""
        advice = "**СОВЕТЫ НА ОСНОВЕ МАТРИЦЫ СУДЬБЫ:**\n\n"
        
        # Анализ основных арканов
        personal_destiny = matrix['personal_destiny']
        social_destiny = matrix['social_destiny']
        spiritual_destiny = matrix['spiritual_destiny']
        
        # Персональное предназначение
        personal_arcana = DestinyMatrixCalculator.ARCANA_MEANINGS.get(personal_destiny, {})
        advice += f"**Ваше предназначение:**\n"
        advice += f"• {personal_arcana.get('meaning', '')}\n"
        advice += f"• Развивайте качества аркана {personal_arcana.get('name', '')}\n\n"
        
        # Социальное предназначение
        social_arcana = DestinyMatrixCalculator.ARCANA_MEANINGS.get(social_destiny, {})
        advice += f"**Ваша роль в обществе:**\n"
        advice += f"• {social_arcana.get('meaning', '')}\n"
        advice += f"• Помогайте другим через {social_arcana.get('name', '')}\n\n"
        
        # Духовное развитие
        spiritual_arcana = DestinyMatrixCalculator.ARCANA_MEANINGS.get(spiritual_destiny, {})
        advice += f"**Духовный путь:**\n"
        advice += f"• {spiritual_arcana.get('meaning', '')}\n"
        advice += f"• Изучайте аспекты аркана {spiritual_arcana.get('name', '')}\n\n"
        
        # Практические советы
        advice += "**Практические рекомендации:**\n"
        
        if matrix['money_energy'] >= 15:
            advice += "• У вас сильная энергия денег - развивайте финансовые навыки\n"
        else:
            advice += "• Работайте над отношением к деньгам и материальному\n"
        
        if matrix['health_energy'] >= 15:
            advice += "• Отличная энергия здоровья - поддерживайте активный образ жизни\n"
        else:
            advice += "• Обратите внимание на здоровье и образ жизни\n"
        
        if matrix['creativity'] >= 15:
            advice += "• Высокий творческий потенциал - развивайте таланты\n"
        else:
            advice += "• Ищите способы выражения творчества\n"
        
        return advice


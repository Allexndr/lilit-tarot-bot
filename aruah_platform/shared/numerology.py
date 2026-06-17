"""
Модуль нумерологии для платформы АРУАХ
"""

from datetime import date
from typing import Dict, Any


class NumerologyCalculator:
    """Калькулятор нумерологических значений"""
    
    @staticmethod
    def calculate_life_path_number(birth_date: date) -> int:
        """Расчёт числа жизненного пути"""
        day, month, year = birth_date.day, birth_date.month, birth_date.year
        total = sum(int(d) for d in f"{day:02d}{month:02d}{year:04d}")
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(d) for d in str(total))
        return total
    
    @staticmethod
    def calculate_destiny_number(name: str) -> int:
        """Расчёт числа судьбы по имени"""
        letter_values = {
            'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9,
            'И': 1, 'Й': 2, 'К': 3, 'Л': 4, 'М': 5, 'Н': 6, 'О': 7, 'П': 8, 'Р': 9,
            'С': 1, 'Т': 2, 'У': 3, 'Ф': 4, 'Х': 5, 'Ц': 6, 'Ч': 7, 'Ш': 8, 'Щ': 9,
            'Ъ': 1, 'Ы': 2, 'Ь': 3, 'Э': 4, 'Ю': 5, 'Я': 6
        }
        total = sum(letter_values.get(char.upper(), 0) for char in name)
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(d) for d in str(total))
        return total
    
    @staticmethod
    def calculate_pythagorean_square(birth_date: date) -> Dict[str, int]:
        """Расчёт квадрата Пифагора"""
        day, month, year = birth_date.day, birth_date.month, birth_date.year
        
        # Основные числа
        character = sum(int(d) for d in f"{day:02d}")
        energy = sum(int(d) for d in f"{month:02d}")
        interest = sum(int(d) for d in f"{year:04d}")
        health = sum(int(d) for d in f"{day:02d}{month:02d}")
        logic = sum(int(d) for d in f"{month:02d}{year:04d}")
        labor = sum(int(d) for d in f"{day:02d}{year:04d}")
        luck = sum(int(d) for d in f"{day:02d}{month:02d}{year:04d}")
        duty = sum(int(d) for d in f"{day:02d}{month:02d}{year:04d}")
        memory = sum(int(d) for d in f"{day:02d}{month:02d}{year:04d}")
        
        return {
            'character': character,
            'energy': energy,
            'interest': interest,
            'health': health,
            'logic': logic,
            'labor': labor,
            'luck': luck,
            'duty': duty,
            'memory': memory
        }
    
    @staticmethod
    def calculate_personal_year(birth_date: date, current_year: int) -> int:
        """Расчёт персонального года"""
        day, month = birth_date.day, birth_date.month
        total = day + month + current_year
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(d) for d in str(total))
        return total
    
    @staticmethod
    def calculate_personal_month(birth_date: date, current_year: int, current_month: int) -> int:
        """Расчёт персонального месяца"""
        personal_year = NumerologyCalculator.calculate_personal_year(birth_date, current_year)
        total = personal_year + current_month
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(d) for d in str(total))
        return total
    
    @staticmethod
    def get_number_meaning(number: int) -> Dict[str, str]:
        """Получить значение числа"""
        meanings = {
            1: {
                "name": "Лидер",
                "traits": "Инициатива, независимость, лидерство, оригинальность",
                "challenges": "Эгоизм, упрямство, нетерпеливость"
            },
            2: {
                "name": "Дипломат",
                "traits": "Сотрудничество, дипломатия, терпение, интуиция",
                "challenges": "Зависимость, нерешительность, пассивность"
            },
            3: {
                "name": "Творец",
                "traits": "Творчество, оптимизм, общительность, самовыражение",
                "challenges": "Поверхностность, сплетни, расточительность"
            },
            4: {
                "name": "Строитель",
                "traits": "Стабильность, практичность, трудолюбие, надежность",
                "challenges": "Упрямство, консерватизм, медлительность"
            },
            5: {
                "name": "Авантюрист",
                "traits": "Свобода, приключения, перемены, прогресс",
                "challenges": "Беспокойство, непостоянство, импульсивность"
            },
            6: {
                "name": "Заботливый",
                "traits": "Ответственность, забота, гармония, семья",
                "challenges": "Вмешательство, жертвенность, тревожность"
            },
            7: {
                "name": "Искатель",
                "traits": "Духовность, анализ, интуиция, мудрость",
                "challenges": "Изоляция, скептицизм, пессимизм"
            },
            8: {
                "name": "Организатор",
                "traits": "Материальный успех, власть, амбиции, эффективность",
                "challenges": "Жадность, авторитаризм, стресс"
            },
            9: {
                "name": "Гуманист",
                "traits": "Завершение, мудрость, гуманизм, всеобщность",
                "challenges": "Идеализм, разочарование, отчуждение"
            },
            11: {
                "name": "Интуитивный",
                "traits": "Интуиция, вдохновение, духовность, просветление",
                "challenges": "Нервозность, перфекционизм, стресс"
            },
            22: {
                "name": "Мастер-строитель",
                "traits": "Практическая духовность, масштабные проекты, служение",
                "challenges": "Стресс, перфекционизм, перегрузка"
            },
            33: {
                "name": "Мастер-учитель",
                "traits": "Высшая духовность, исцеление, мудрость, служение",
                "challenges": "Перегрузка, перфекционизм, изоляция"
            }
        }
        return meanings.get(number, {"name": "Неизвестно", "traits": "", "challenges": ""})


class NumerologyInterpreter:
    """Интерпретатор нумерологических данных"""
    
    @staticmethod
    def interpret_life_path(life_path_number: int) -> str:
        """Интерпретация числа жизненного пути"""
        meaning = NumerologyCalculator.get_number_meaning(life_path_number)
        return f"""
🔢 **Число жизненного пути: {life_path_number}**

**{meaning['name']}**

**Ваши сильные стороны:**
{meaning['traits']}

**На что обратить внимание:**
{meaning['challenges']}

**Совет:**
Это число показывает ваш жизненный путь и основные уроки, которые вам предстоит изучить.
        """.strip()
    
    @staticmethod
    def interpret_destiny_number(destiny_number: int) -> str:
        """Интерпретация числа судьбы"""
        meaning = NumerologyCalculator.get_number_meaning(destiny_number)
        return f"""
⭐ **Число судьбы: {destiny_number}**

**{meaning['name']}**

**Ваше предназначение:**
{meaning['traits']}

**Потенциальные препятствия:**
{meaning['challenges']}

**Совет:**
Это число показывает ваше истинное предназначение и то, к чему вы должны стремиться.
        """.strip()
    
    @staticmethod
    def interpret_pythagorean_square(square: Dict[str, int]) -> str:
        """Интерпретация квадрата Пифагора"""
        interpretation = "📊 **Квадрат Пифагора**\n\n"
        
        # Анализ каждого числа
        for key, value in square.items():
            meaning = NumerologyCalculator.get_number_meaning(value)
            interpretation += f"**{key.title()}: {value}** - {meaning['name']}\n"
        
        interpretation += "\n**Общий анализ:**\n"
        
        # Анализ характера
        if square['character'] >= 5:
            interpretation += "• У вас сильный характер и лидерские качества\n"
        else:
            interpretation += "• Вы более мягкий и дипломатичный человек\n"
        
        # Анализ энергии
        if square['energy'] >= 5:
            interpretation += "• Вы обладаете высокой жизненной энергией\n"
        else:
            interpretation += "• Вам нужно больше отдыхать и восстанавливать силы\n"
        
        # Анализ здоровья
        if square['health'] >= 5:
            interpretation += "• У вас хорошее здоровье и выносливость\n"
        else:
            interpretation += "• Обратите внимание на здоровье и образ жизни\n"
        
        return interpretation
    
    @staticmethod
    def interpret_personal_year(personal_year: int) -> str:
        """Интерпретация персонального года"""
        meaning = NumerologyCalculator.get_number_meaning(personal_year)
        return f"""
🗓 **Персональный год: {personal_year}**

**{meaning['name']}**

**Что ждёт в этом году:**
{meaning['traits']}

**На что обратить внимание:**
{meaning['challenges']}

**Совет:**
Этот год принесёт вам возможности для развития в указанных направлениях.
        """.strip()


"""
Модуль диагностики чакр для платформы АРУАХ
"""

from datetime import date
from typing import Dict, Any, List
import random


class ChakraCalculator:
    """Калькулятор состояния чакр"""
    
    CHAKRAS = {
        'muladhara': {
            'name': 'Муладхара',
            'name_kz': 'Муладхара',
            'sanskrit': 'मूलाधार',
            'color': 'Красный',
            'element': 'Земля',
            'location': 'Основание позвоночника',
            'function': 'Выживание, безопасность, стабильность',
            'mantra': 'LAM',
            'crystals': ['Гранат', 'Красная яшма', 'Обсидиан', 'Красный агат']
        },
        'svadhisthana': {
            'name': 'Свадхистана',
            'name_kz': 'Свадхистана',
            'sanskrit': 'स्वाधिष्ठान',
            'color': 'Оранжевый',
            'element': 'Вода',
            'location': 'Нижняя часть живота',
            'function': 'Сексуальность, творчество, удовольствие',
            'mantra': 'VAM',
            'crystals': ['Оранжевый кальцит', 'Сердолик', 'Тигровый глаз', 'Оранжевый агат']
        },
        'manipura': {
            'name': 'Манипура',
            'name_kz': 'Манипура',
            'sanskrit': 'मणिपूर',
            'color': 'Жёлтый',
            'element': 'Огонь',
            'location': 'Солнечное сплетение',
            'function': 'Личная сила, воля, самооценка',
            'mantra': 'RAM',
            'crystals': ['Цитрин', 'Жёлтый топаз', 'Янтарь', 'Жёлтый кальцит']
        },
        'anahata': {
            'name': 'Анахата',
            'name_kz': 'Анахата',
            'sanskrit': 'अनाहत',
            'color': 'Зелёный',
            'element': 'Воздух',
            'location': 'Сердечный центр',
            'function': 'Любовь, сострадание, прощение',
            'mantra': 'YAM',
            'crystals': ['Розовый кварц', 'Зелёный авантюрин', 'Малахит', 'Зелёный турмалин']
        },
        'vishuddha': {
            'name': 'Вишудха',
            'name_kz': 'Вишудха',
            'sanskrit': 'विशुद्ध',
            'color': 'Голубой',
            'element': 'Эфир',
            'location': 'Горло',
            'function': 'Коммуникация, самовыражение, истина',
            'mantra': 'HAM',
            'crystals': ['Голубой агат', 'Аквамарин', 'Содалит', 'Голубой топаз']
        },
        'ajna': {
            'name': 'Аджна',
            'name_kz': 'Аджна',
            'sanskrit': 'आज्ञा',
            'color': 'Синий',
            'element': 'Свет',
            'location': 'Третий глаз',
            'function': 'Интуиция, мудрость, духовное видение',
            'mantra': 'OM',
            'crystals': ['Аметист', 'Лазурит', 'Флюорит', 'Синий сапфир']
        },
        'sahasrara': {
            'name': 'Сахасрара',
            'name_kz': 'Сахасрара',
            'sanskrit': 'सहस्रार',
            'color': 'Фиолетовый',
            'element': 'Мысль',
            'location': 'Макушка головы',
            'function': 'Духовность, просветление, связь с божественным',
            'mantra': 'OM',
            'crystals': ['Аметист', 'Горный хрусталь', 'Селенит', 'Фиолетовый флюорит']
        }
    }
    
    @staticmethod
    def calculate_chakra_analysis(birth_date: date) -> Dict[str, Any]:
        """Расчёт состояния чакр по дате рождения"""
        day, month, year = birth_date.day, birth_date.month, birth_date.year
        
        chakras = {}
        
        for chakra_id, chakra_info in ChakraCalculator.CHAKRAS.items():
            # Упрощённый алгоритм расчёта состояния чакры
            if chakra_id == 'muladhara':
                value = (day + month) % 7
            elif chakra_id == 'svadhisthana':
                value = (month + year) % 7
            elif chakra_id == 'manipura':
                value = (day + year) % 7
            elif chakra_id == 'anahata':
                value = (day + month + year) % 7
            elif chakra_id == 'vishuddha':
                value = (day * 2 + month) % 7
            elif chakra_id == 'ajna':
                value = (month * 2 + year) % 7
            else:  # sahasrara
                value = (day + month + year + 1) % 7
            
            # Определение уровня активности
            if value <= 1:
                level = 'Заблокирована'
                percentage = random.randint(0, 30)
                status = 'blocked'
            elif value <= 3:
                level = 'Слабая'
                percentage = random.randint(31, 60)
                status = 'weak'
            elif value <= 5:
                level = 'Нормальная'
                percentage = random.randint(61, 80)
                status = 'normal'
            else:
                level = 'Сильная'
                percentage = random.randint(81, 100)
                status = 'strong'
            
            chakras[chakra_id] = {
                **chakra_info,
                'value': value,
                'level': level,
                'percentage': percentage,
                'status': status
            }
        
        return chakras
    
    @staticmethod
    def get_chakra_balance_score(chakras: Dict[str, Any]) -> int:
        """Получить общий балл баланса чакр"""
        total_percentage = sum(chakra['percentage'] for chakra in chakras.values())
        return total_percentage // 7  # Средний процент


class ChakraInterpreter:
    """Интерпретатор состояния чакр"""
    
    @staticmethod
    def interpret_chakra_analysis(chakras: Dict[str, Any]) -> str:
        """Интерпретация анализа чакр"""
        balance_score = ChakraCalculator.get_chakra_balance_score(chakras)
        
        interpretation = f"""
🌈 **Диагностика чакр**

**Общий баланс:** {balance_score}%

"""
        
        # Анализ каждой чакры
        for chakra_id, chakra in chakras.items():
            status_emoji = {
                'blocked': '🔴',
                'weak': '🟡', 
                'normal': '🟢',
                'strong': '💚'
            }.get(chakra['status'], '⚪')
            
            interpretation += f"""
{status_emoji} **{chakra['name']}** ({chakra['color']}) - {chakra['level']} ({chakra['percentage']}%)
**Функция:** {chakra['function']}
**Мантра:** {chakra['mantra']}
**Кристаллы:** {', '.join(chakra['crystals'])}
"""
        
        # Общие рекомендации
        interpretation += "\n**Общие рекомендации:**\n"
        
        if balance_score < 50:
            interpretation += "• Ваши чакры нуждаются в активации и балансировке\n"
            interpretation += "• Рекомендуется медитация и работа с кристаллами\n"
            interpretation += "• Обратите внимание на физическое и эмоциональное здоровье\n"
        elif balance_score < 70:
            interpretation += "• Ваши чакры в хорошем состоянии, но есть потенциал для улучшения\n"
            interpretation += "• Продолжайте практики медитации и энергетической работы\n"
            interpretation += "• Сосредоточьтесь на слабых чакрах\n"
        else:
            interpretation += "• Отличный баланс чакр! Вы находитесь в гармонии с собой\n"
            interpretation += "• Продолжайте поддерживать этот уровень\n"
            interpretation += "• Рассмотрите возможность помощи другим в их духовном развитии\n"
        
        return interpretation
    
    @staticmethod
    def get_chakra_meditation_advice(chakras: Dict[str, Any]) -> str:
        """Получить советы по медитации для чакр"""
        weak_chakras = [chakra for chakra in chakras.values() if chakra['status'] in ['blocked', 'weak']]
        
        if not weak_chakras:
            return "Все ваши чакры в хорошем состоянии! Продолжайте поддерживать баланс."
        
        advice = "**Медитационные практики для слабых чакр:**\n\n"
        
        for chakra in weak_chakras:
            advice += f"""
**{chakra['name']} ({chakra['color']}):**
• Медитация: Сосредоточьтесь на области {chakra['location']}
• Мантра: {chakra['mantra']}
• Цвет: Визуализируйте {chakra['color'].lower()} свет
• Кристаллы: Используйте {chakra['crystals'][0]} или {chakra['crystals'][1]}
• Дыхание: Глубокое дыхание в течение 10-15 минут
"""
        
        return advice
    
    @staticmethod
    def get_chakra_healing_crystals(chakras: Dict[str, Any]) -> str:
        """Получить рекомендации по кристаллам для исцеления"""
        advice = "**Кристаллы для исцеления чакр:**\n\n"
        
        for chakra_id, chakra in chakras.items():
            if chakra['status'] in ['blocked', 'weak']:
                advice += f"""
**{chakra['name']} - {chakra['level']}:**
• Основной: {chakra['crystals'][0]}
• Дополнительный: {chakra['crystals'][1]}
• Использование: Носите как украшение или держите во время медитации
• Очистка: Промойте под проточной водой или оставьте на солнце
"""
        
        return advice
    
    @staticmethod
    def get_chakra_affirmations(chakras: Dict[str, Any]) -> str:
        """Получить аффирмации для чакр"""
        affirmations = {
            'muladhara': "Я в безопасности и защищён. Я заземлён и стабилен.",
            'svadhisthana': "Я творческий и чувственный. Я заслуживаю удовольствия и радости.",
            'manipura': "Я сильный и уверенный. Я контролирую свою жизнь.",
            'anahata': "Я люблю и принимаю себя. Моё сердце открыто для любви.",
            'vishuddha': "Я выражаю свою истину. Мои слова исходят из сердца.",
            'ajna': "Я доверяю своей интуиции. Я вижу ясно и мудро.",
            'sahasrara': "Я связан с божественным. Я нахожусь в потоке вселенной."
        }
        
        advice = "**Аффирмации для чакр:**\n\n"
        
        for chakra_id, chakra in chakras.items():
            if chakra['status'] in ['blocked', 'weak']:
                advice += f"""
**{chakra['name']}:**
"{affirmations[chakra_id]}"
Повторяйте 3-5 раз утром и вечером.
"""
        
        return advice


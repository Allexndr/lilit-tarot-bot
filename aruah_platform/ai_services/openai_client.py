"""
OpenAI клиент для платформы АРУАХ
"""

import asyncio
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from config import settings


class OpenAIClient:
    """Клиент для работы с OpenAI API"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4"
        self.max_tokens = 1000
        self.temperature = 0.8
    
    async def generate_tarot_interpretation(self, cards: List[Dict], question: str, 
                                          user_context: Dict[str, Any]) -> str:
        """Генерация интерпретации Таро"""
        prompt = f"""
Ты - опытный таролог Лилит с 15-летним стажем из Алматы.
Специализируешься на психологическом Таро и духовном развитии.

Вопрос клиента: {question}
Карты: {self._format_cards(cards)}
Контекст: {self._format_user_context(user_context)}

Дай интерпретацию (400-600 слов):
1. Общая энергия расклада
2. Детальный анализ каждой карты
3. Взаимосвязи и синергия
4. Практические советы
5. Что делать сегодня/на неделе
6. Медитация/аффирмация

Стиль: эмпатичный, поддерживающий, конкретный
Учитывай казахстанскую ментальность
        """.strip()
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Ты таролог Лилит, опытный специалист по Таро."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    async def generate_numerology_interpretation(self, calculations: Dict[str, Any], 
                                               user_data: Dict[str, Any]) -> str:
        """Генерация интерпретации нумерологии"""
        prompt = f"""
Ты - нумеролог Аруах, специалист по числам судьбы.
Работаешь с квадратом Пифагора и персональными годами.

Данные клиента: {self._format_user_context(user_data)}
Расчёты: {self._format_calculations(calculations)}

Дай анализ (300-500 слов):
1. Основные числа и их значение
2. Сильные и слабые стороны
3. Совместимость с партнёром
4. Персональный год
5. Рекомендации по развитию

Стиль: мудрый, аналитичный, практичный
        """.strip()
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Ты нумеролог Аруах, эксперт по числам судьбы."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    async def generate_astrology_interpretation(self, natal_chart: Dict[str, Any], 
                                             zodiac_sign: str, question: str) -> str:
        """Генерация интерпретации астрологии"""
        prompt = f"""
Ты - астролог Аруах, эксперт по натальным картам.
Знаешь особенности казахстанской астрологии.

Натальная карта: {self._format_natal_chart(natal_chart)}
Знак зодиака: {zodiac_sign}
Вопрос: {question}

Дай прогноз (400-600 слов):
1. Анализ планет
2. Аспекты и дома
3. Транзиты
4. Совместимость
5. Рекомендации

Стиль: мистический, но практичный
        """.strip()
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Ты астролог Аруах, специалист по натальным картам."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    async def generate_destiny_matrix_interpretation(self, matrix: Dict[str, int], 
                                                   user_data: Dict[str, Any]) -> str:
        """Генерация интерпретации матрицы судьбы"""
        prompt = f"""
Ты - специалист по матрице судьбы Аруах.
Работаешь с 22 арканами и их значениями.

Данные клиента: {self._format_user_context(user_data)}
Матрица: {self._format_matrix(matrix)}

Дай интерпретацию (500-700 слов):
1. Основные точки матрицы
2. Кармические задачи
3. Предназначение и миссия
4. Совместимость
5. Рекомендации по развитию

Стиль: мудрый, глубокий, практичный
        """.strip()
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Ты специалист по матрице судьбы Аруах."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    async def generate_chakra_interpretation(self, chakras: Dict[str, Any], 
                                           user_data: Dict[str, Any]) -> str:
        """Генерация интерпретации чакр"""
        prompt = f"""
Ты - специалист по чакрам Аруах.
Работаешь с энергетическими центрами и их балансировкой.

Данные клиента: {self._format_user_context(user_data)}
Состояние чакр: {self._format_chakras(chakras)}

Дай интерпретацию (400-600 слов):
1. Общий баланс чакр
2. Анализ каждой чакры
3. Рекомендации по медитации
4. Кристаллы для исцеления
5. Практические упражнения

Стиль: духовный, практичный, поддерживающий
        """.strip()
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Ты специалист по чакрам Аруах."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    async def generate_human_design_interpretation(self, hd_data: Dict[str, Any], 
                                                 user_data: Dict[str, Any]) -> str:
        """Генерация интерпретации Human Design"""
        prompt = f"""
Ты - специалист по Human Design Аруах.
Работаешь с типами, центрами и профилями.

Данные клиента: {self._format_user_context(user_data)}
Human Design: {self._format_human_design(hd_data)}

Дай интерпретацию (500-700 слов):
1. Анализ типа и стратегии
2. Определённые и неопределённые центры
3. Профиль и его значение
4. Авторитет и принятие решений
5. Практические рекомендации

Стиль: аналитичный, практичный, поддерживающий
        """.strip()
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Ты специалист по Human Design Аруах."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    def _format_cards(self, cards: List[Dict]) -> str:
        """Форматирование карт для промпта"""
        formatted = []
        for i, card in enumerate(cards):
            position = card.get('position', f'Позиция {i+1}')
            name = card.get('name', 'Неизвестная карта')
            is_reversed = card.get('is_reversed', False)
            status = "перевернутая" if is_reversed else "прямая"
            formatted.append(f"{position}: {name} ({status})")
        return "\n".join(formatted)
    
    def _format_user_context(self, user_data: Dict[str, Any]) -> str:
        """Форматирование контекста пользователя"""
        context = []
        if user_data.get('name'):
            context.append(f"Имя: {user_data['name']}")
        if user_data.get('birth_date'):
            context.append(f"Дата рождения: {user_data['birth_date']}")
        if user_data.get('gender'):
            context.append(f"Пол: {user_data['gender']}")
        if user_data.get('city'):
            context.append(f"Город: {user_data['city']}")
        return ", ".join(context)
    
    def _format_calculations(self, calculations: Dict[str, Any]) -> str:
        """Форматирование расчётов"""
        formatted = []
        for key, value in calculations.items():
            formatted.append(f"{key}: {value}")
        return ", ".join(formatted)
    
    def _format_natal_chart(self, natal_chart: Dict[str, Any]) -> str:
        """Форматирование натальной карты"""
        planets = natal_chart.get('planets', {})
        formatted = []
        for planet, sign in planets.items():
            formatted.append(f"{planet}: {sign}")
        return ", ".join(formatted)
    
    def _format_matrix(self, matrix: Dict[str, int]) -> str:
        """Форматирование матрицы судьбы"""
        formatted = []
        for key, value in matrix.items():
            formatted.append(f"{key}: {value}")
        return ", ".join(formatted)
    
    def _format_chakras(self, chakras: Dict[str, Any]) -> str:
        """Форматирование чакр"""
        formatted = []
        for chakra_id, chakra in chakras.items():
            name = chakra.get('name', chakra_id)
            level = chakra.get('level', 'Неизвестно')
            percentage = chakra.get('percentage', 0)
            formatted.append(f"{name}: {level} ({percentage}%)")
        return ", ".join(formatted)
    
    def _format_human_design(self, hd_data: Dict[str, Any]) -> str:
        """Форматирование Human Design"""
        formatted = []
        formatted.append(f"Тип: {hd_data.get('type', 'Неизвестно')}")
        formatted.append(f"Профиль: {hd_data.get('profile', 'Неизвестно')}")
        formatted.append(f"Авторитет: {hd_data.get('authority', 'Неизвестно')}")
        formatted.append(f"Стратегия: {hd_data.get('strategy', 'Неизвестно')}")
        return ", ".join(formatted)

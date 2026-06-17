"""
Сервисы для бизнес-логики Telegram бота АРУАХ
"""

import logging
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.database import DatabaseManager
from telegram_bot.models import User, Reading, TarotCard, Spread
from shared.tarot_data import MAJOR_ARCANA, TAROT_SPREADS
from shared.numerology import NumerologyCalculator, NumerologyInterpreter
from shared.astrology import AstrologyCalculator, AstrologyInterpreter
from shared.chakras import ChakraCalculator, ChakraInterpreter
from shared.destiny_matrix import DestinyMatrixCalculator, DestinyMatrixInterpreter
from shared.human_design import HumanDesignCalculator, HumanDesignInterpreter
from ai_services.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class UserService:
    """Сервис для работы с пользователями"""
    
    @staticmethod
    async def get_or_create_user(telegram_id: int, username: str = None,
                               first_name: str = None, last_name: str = None) -> User:
        """Получить или создать пользователя"""
        async with DatabaseManager.get_session() as session:
            try:
                result = await session.execute(
                    select(User).where(User.telegram_id == telegram_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    user = User(
                        telegram_id=telegram_id,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        registration_date=datetime.now(),
                        last_activity=datetime.now()
                    )
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                else:
                    # Обновить активность
                    user.last_activity = datetime.now()
                    await session.commit()
                
                return user
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка при создании/получении пользователя: {e}")
                raise e
    
    @staticmethod
    async def can_make_request(user: User) -> bool:
        """Проверить, может ли пользователь сделать запрос"""
        if user.subscription_type == "premium":
            return True
        
        if user.subscription_type == "vip":
            return True
        
        # Для free пользователей проверяем дневной лимит
        if user.daily_requests >= user.daily_limit:
            return False
        
        return True
    
    @staticmethod
    async def increment_daily_requests(user: User) -> None:
        """Увеличить счётчик дневных запросов"""
        async with DatabaseManager.get_session() as session:
            try:
                await session.execute(
                    update(User)
                    .where(User.id == user.id)
                    .values(
                        daily_requests=User.daily_requests + 1,
                        total_requests=User.total_requests + 1
                    )
                )
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка при обновлении счётчика запросов: {e}")
                raise e


class TarotService:
    """Сервис для работы с Таро"""
    
    @staticmethod
    async def get_random_card() -> Dict[str, Any]:
        """Получить случайную карту Таро"""
        import random
        
        # Выбираем случайную карту из старших арканов
        card_id = random.randint(0, 21)
        is_reversed = random.choice([True, False])
        
        card_data = MAJOR_ARCANA.get(card_id, {})
        
        return {
            'id': card_id,
            'name': card_data.get('name', 'Неизвестная карта'),
            'name_en': card_data.get('name_en', ''),
            'name_kz': card_data.get('name_kz', ''),
            'is_reversed': is_reversed,
            'upright_meaning': card_data.get('upright_meaning', ''),
            'reversed_meaning': card_data.get('reversed_meaning', ''),
            'upright_short': card_data.get('upright_short', ''),
            'reversed_short': card_data.get('reversed_short', ''),
            'arcana_personality': card_data.get('arcana_personality', ''),
            'arcana_voice_phrases': card_data.get('arcana_voice_phrases', [])
        }
    
    @staticmethod
    async def get_cards_for_spread(spread_name: str) -> List[Dict[str, Any]]:
        """Получить карты для конкретного расклада"""
        spread_info = TAROT_SPREADS.get(spread_name)
        if not spread_info:
            raise ValueError(f"Расклад {spread_name} не найден")
        
        cards = []
        used_cards = set()
        
        for i in range(spread_info['card_count']):
            while True:
                card = await TarotService.get_random_card()
                card_key = (card['id'], card['is_reversed'])
                if card_key not in used_cards:
                    used_cards.add(card_key)
                    break
            cards.append(card)
        
        return cards
    
    @staticmethod
    async def interpret_card(card: Dict[str, Any], context: str = "") -> str:
        """Интерпретировать карту"""
        name = card['name']
        is_reversed = card['is_reversed']
        
        if is_reversed:
            meaning = card['reversed_meaning']
            short = card['reversed_short']
        else:
            meaning = card['upright_meaning']
            short = card['upright_short']
        
        interpretation = f"""
🔮 **{name}** {'(перевернутая)' if is_reversed else '(прямая)'}

**Значение:**
{meaning}

**Краткий совет:**
{short}

**Контекст:** {context}
        """.strip()
        
        return interpretation
    
    @staticmethod
    async def create_reading(user_id: int, spread_type: str, question: str = None) -> Dict[str, Any]:
        """Создать расклад"""
        try:
            # Получить карты для расклада
            cards = await TarotService.get_cards_for_spread(spread_type)
            
            # Создать интерпретацию
            interpretation = await TarotService.interpret_spread(cards, spread_type, question)
            
            # Сохранить в базу данных
            async with DatabaseManager.get_session() as session:
                reading = Reading(
                    user_id=user_id,
                    spread_id=1,  # Временный ID
                    question=question,
                    cards_drawn=[{
                        'card_id': card['id'],
                        'position': f"Позиция {i+1}",
                        'is_reversed': card['is_reversed']
                    } for i, card in enumerate(cards)],
                    interpretation=interpretation
                )
                session.add(reading)
                await session.commit()
            
            return {
                'cards': cards,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Ошибка при создании расклада: {e}")
            raise e
    
    @staticmethod
    async def interpret_spread(cards: List[Dict[str, Any]], spread_type: str, question: str = None) -> str:
        """Интерпретировать расклад"""
        spread_info = TAROT_SPREADS.get(spread_type, {})
        positions = spread_info.get('positions', [])
        
        interpretation = f"🔮 **Расклад '{spread_info.get('name', spread_type)}'**\n\n"
        
        if question:
            interpretation += f"**Вопрос:** {question}\n\n"
        
        interpretation += "**Карты:**\n"
        
        for i, card in enumerate(cards):
            position = positions[i] if i < len(positions) else f"Позиция {i+1}"
            name = card['name']
            is_reversed = card['is_reversed']
            status = "перевернутая" if is_reversed else "прямая"
            
            interpretation += f"\n**{position}:** {name} ({status})\n"
            
            if is_reversed:
                meaning = card['reversed_meaning']
            else:
                meaning = card['upright_meaning']
            
            interpretation += f"{meaning}\n"
        
        # Общая интерпретация
        interpretation += "\n**Общая энергия расклада:**\n"
        interpretation += "Карты показывают, что в вашей жизни происходит важный переходный период. "
        interpretation += "Время прислушаться к интуиции и довериться внутренней мудрости.\n"
        
        interpretation += "\n**Совет:**\n"
        interpretation += "Будьте открыты к новым возможностям и не бойтесь перемен. "
        interpretation += "Ваша интуиция сейчас особенно сильна - доверьтесь ей.\n"
        
        return interpretation
    
    @staticmethod
    async def get_daily_card(user_id: int) -> Dict[str, Any]:
        """Получить карту дня"""
        card = await TarotService.get_random_card()
        return card


class NumerologyService:
    """Сервис для работы с нумерологией"""
    
    @staticmethod
    async def calculate_life_path(user_id: int, birth_date: date) -> Dict[str, Any]:
        """Рассчитать число жизненного пути"""
        try:
            life_path_number = NumerologyCalculator.calculate_life_path_number(birth_date)
            interpretation = NumerologyInterpreter.interpret_life_path(life_path_number)
            
            return {
                'life_path_number': life_path_number,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Ошибка при расчёте числа жизненного пути: {e}")
            raise e
    
    @staticmethod
    async def calculate_destiny_number(user_id: int, name: str) -> Dict[str, Any]:
        """Рассчитать число судьбы"""
        try:
            destiny_number = NumerologyCalculator.calculate_destiny_number(name)
            interpretation = NumerologyInterpreter.interpret_destiny_number(destiny_number)
            
            return {
                'destiny_number': destiny_number,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Ошибка при расчёте числа судьбы: {e}")
            raise e
    
    @staticmethod
    async def calculate_pythagorean_square(user_id: int, birth_date: date) -> Dict[str, Any]:
        """Рассчитать квадрат Пифагора"""
        try:
            square = NumerologyCalculator.calculate_pythagorean_square(birth_date)
            interpretation = NumerologyInterpreter.interpret_pythagorean_square(square)
            
            return {
                'square': square,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Ошибка при расчёте квадрата Пифагора: {e}")
            raise e


class AstrologyService:
    """Сервис для работы с астрологией"""
    
    @staticmethod
    async def get_zodiac_sign(birth_date: date) -> str:
        """Получить знак зодиака"""
        return AstrologyCalculator.get_zodiac_sign(birth_date)
    
    @staticmethod
    async def generate_daily_forecast(zodiac_sign: str) -> str:
        """Сгенерировать дневной прогноз"""
        return AstrologyInterpreter.generate_daily_forecast(zodiac_sign)
    
    @staticmethod
    async def generate_weekly_forecast(zodiac_sign: str) -> str:
        """Сгенерировать недельный прогноз"""
        return AstrologyInterpreter.generate_weekly_forecast(zodiac_sign)


class ChakraService:
    """Сервис для работы с чакрами"""
    
    @staticmethod
    async def calculate_chakra_analysis(birth_date: date) -> Dict[str, Any]:
        """Рассчитать анализ чакр"""
        try:
            chakras = ChakraCalculator.calculate_chakra_analysis(birth_date)
            interpretation = ChakraInterpreter.interpret_chakra_analysis(chakras)
            
            return {
                'chakras': chakras,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Ошибка при расчёте чакр: {e}")
            raise e


class DestinyMatrixService:
    """Сервис для работы с матрицей судьбы"""
    
    @staticmethod
    async def calculate_destiny_matrix(birth_date: date) -> Dict[str, Any]:
        """Рассчитать матрицу судьбы"""
        try:
            matrix = DestinyMatrixCalculator.calculate_destiny_matrix(birth_date)
            interpretation = DestinyMatrixInterpreter.interpret_destiny_matrix(matrix)
            
            return {
                'matrix': matrix,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Ошибка при расчёте матрицы судьбы: {e}")
            raise e


class HumanDesignService:
    """Сервис для работы с Human Design"""
    
    @staticmethod
    async def calculate_human_design(birth_date: date, birth_time: str = None, 
                                   birth_place: str = None) -> Dict[str, Any]:
        """Рассчитать Human Design"""
        try:
            hd_data = HumanDesignCalculator.calculate_human_design(birth_date, birth_time, birth_place)
            interpretation = HumanDesignInterpreter.interpret_human_design(hd_data)
            
            return {
                'hd_data': hd_data,
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Ошибка при расчёте Human Design: {e}")
            raise e


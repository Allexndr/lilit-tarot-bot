"""
Умная интеграция с Google Gemini API
С кэшированием и оптимизацией для лимита 1500 запросов/день
"""
import os
import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDztfeyNxLS2Z6RxKmTqio2-B3jbAKnCEg")

# Настраиваем Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Кэш для интерпретаций (в памяти)
# В продакшене лучше использовать Redis
INTERPRETATION_CACHE = {}
DAILY_REQUEST_COUNT = 0
LAST_RESET_DATE = datetime.now().date()
MAX_DAILY_REQUESTS = 1400  # Оставляем запас от 1500


class GeminiAI:
    """Сервис для работы с Google Gemini AI"""
    
    @staticmethod
    def _get_cache_key(card: Dict[str, Any], position: str = None, question: str = None) -> str:
        """Генерируем ключ кэша для интерпретации"""
        # Кэшируем по карте + позиция (вопрос игнорируем для большего переиспользования)
        cache_data = {
            'card_id': card.get('id'),
            'is_reversed': card.get('is_reversed'),
            'position': position
        }
        key = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(key.encode()).hexdigest()
    
    @staticmethod
    def _check_daily_limit() -> bool:
        """Проверяем не превышен ли дневной лимит"""
        global DAILY_REQUEST_COUNT, LAST_RESET_DATE
        
        # Сбрасываем счетчик в начале нового дня
        today = datetime.now().date()
        if today > LAST_RESET_DATE:
            DAILY_REQUEST_COUNT = 0
            LAST_RESET_DATE = today
        
        return DAILY_REQUEST_COUNT < MAX_DAILY_REQUESTS
    
    @staticmethod
    async def generate_interpretation(
        card: Dict[str, Any],
        position: str = None,
        question: str = None,
        context: Dict[str, Any] = None,
        force_ai: bool = False  # Для платных раскладов
    ) -> str:
        """
        Генерация интерпретации карты через Gemini AI
        
        Args:
            card: Данные карты
            position: Позиция карты в раскладе
            question: Вопрос пользователя
            context: Дополнительный контекст (луна, число дня)
            force_ai: Если True - обязательно использовать AI (для платных)
        """
        global DAILY_REQUEST_COUNT
        
        # 1. Проверяем кэш
        cache_key = GeminiAI._get_cache_key(card, position, question)
        if cache_key in INTERPRETATION_CACHE:
            print(f"✅ Кэш: используем сохраненную интерпретацию")
            return INTERPRETATION_CACHE[cache_key]
        
        # 2. Проверяем лимит
        if not force_ai and not GeminiAI._check_daily_limit():
            print(f"⚠️ Достигнут дневной лимит запросов ({MAX_DAILY_REQUESTS})")
            return _fallback_interpretation(card, position)
        
        # 3. Генерируем через AI
        try:
            # Формируем промпт
            system_prompt = """Ты - мистическая гадалка Лилит. 
Твой стиль: загадочный, мудрый, доброжелательный. Используй эмодзи ✨🌙🔮
Давай глубокие персонализированные трактовки Таро.
Отвечай КОРОТКО (максимум 100 слов), на русском языке."""
            
            card_desc = f"Карта: {card['name']}"
            if card.get('is_reversed'):
                card_desc += " (перевернутая)"
            
            user_prompt = f"{card_desc}\n"
            
            if position:
                user_prompt += f"Позиция: {position}\n"
            
            if question:
                user_prompt += f"Вопрос: {question}\n"
            
            if context:
                if context.get('moon_phase'):
                    user_prompt += f"Луна: {context['moon_phase']}\n"
                if context.get('day_number'):
                    user_prompt += f"Число дня: {context['day_number']}\n"
            
            user_prompt += "\nДай мистическую интерпретацию."
            
            # Используем Gemini Flash Latest (для обхода лимитов)
            model = genai.GenerativeModel('gemini-flash-latest')
            
            # Генерируем
            response = model.generate_content(
                f"{system_prompt}\n\n{user_prompt}",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=200
                )
            )
            
            interpretation = response.text.strip()
            
            # Увеличиваем счетчик
            DAILY_REQUEST_COUNT += 1
            print(f"📊 Gemini запросов сегодня: {DAILY_REQUEST_COUNT}/{MAX_DAILY_REQUESTS}")
            
            # Сохраняем в кэш
            INTERPRETATION_CACHE[cache_key] = interpretation
            
            return interpretation
            
        except Exception as e:
            print(f"❌ Ошибка Gemini API: {e}")
            return _fallback_interpretation(card, position)

    @staticmethod
    async def generate_general_interpretation(prompt: str) -> str:
        """Общая генерация текста для произвольных промптов"""
        global DAILY_REQUEST_COUNT
        
        if not GeminiAI._check_daily_limit():
            return "Извините, лимит мудрости на сегодня исчерпан. Попробуйте завтра. ✨"
            
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=500
                )
            )
            
            DAILY_REQUEST_COUNT += 1
            return response.text.strip()
        except Exception as e:
            print(f"❌ Ошибка General Gemini API: {e}")
            return "Звезды сегодня туманны... Попробуйте позже. 🌌"


def _fallback_interpretation(card: Dict[str, Any], position: str = None) -> str:
    """Статическая интерпретация как резервный вариант"""
    if card.get('is_reversed'):
        meaning = card.get('reversed_meaning', '')
        short = card.get('reversed_short', '')
    else:
        meaning = card.get('upright_meaning', '')
        short = card.get('upright_short', '')
    
    interpretation = f"🔮 <b>{card['name']}</b>"
    if card.get('is_reversed'):
        interpretation += " (перевернутая)"
    
    interpretation += f"\n\n💫 <i>{short}</i>\n\n📖 {meaning}"
    
    if position:
        interpretation = f"<b>{position}:</b>\n{interpretation}"
    
    return interpretation


def get_ai_stats() -> Dict[str, Any]:
    """Получить статистику использования AI"""
    return {
        'requests_today': DAILY_REQUEST_COUNT,
        'limit': MAX_DAILY_REQUESTS,
        'cache_size': len(INTERPRETATION_CACHE),
        'remaining': MAX_DAILY_REQUESTS - DAILY_REQUEST_COUNT
    }

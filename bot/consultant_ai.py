"""
24/7 AI Consultant using Ollama
Handles tarot-related questions with context awareness and off-topic detection
"""
import aiohttp
import json
from typing import List, Dict, Optional
from datetime import datetime

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

# In-memory conversation storage (should be moved to Redis/DB in production)
CONVERSATIONS: Dict[int, List[Dict]] = {}

SYSTEM_PROMPT = """Ты — Лилит, мистический консультант по Таро с 15-летним опытом.
Твоя задача — помогать людям с вопросами о картах Таро, их значениях, раскладах, астрологии, нумерологии и эзотерике.

ВАЖНЫЕ ПРАВИЛА:
1. Отвечай ТОЛЬКО на вопросы о Таро, астрологии, нумерологии, мистике, эзотерике
2. Если вопрос НЕ по теме (математика, программирование, политика, и т.д.), вежливо откажи:
   "🌙 Я консультант по мистическим практикам. Этот вопрос вне моей компетенции. Давайте поговорим о картах?"
3. Будь тёплой, мудрой, немного загадочной, но дружелюбной
4. Используй эмодзи для атмосферы: 🔮✨🌙💫🃏
5. Помни контекст предыдущих сообщений в беседе
6. Давай конкретные ответы, но не слишком длинные (максимум 150 слов)
7. Говори только на русском языке

Примеры хороших вопросов:
- "Что означает карта Маг?"
- "Как делать расклад на любовь?"
- "Расскажи о значении Луны в Таро"

Примеры плохих вопросов (отказывай):
- "Сколько будет 2+2?"
- "Напиши код на Python"
- "Кто выиграет выборы?"
"""

class ConsultantAI:
    """AI Consultant powered by Ollama"""
    
    @staticmethod
    async def is_on_topic(question: str) -> bool:
        """Check if question is related to tarot/mysticism"""
        check_prompt = f"""Вопрос пользователя: "{question}"

Это вопрос о Таро, астрологии, нумерологии, мистике или эзотерике?
Ответь ТОЛЬКО "ДА" или "НЕТ" без объяснений."""

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": MODEL_NAME,
                    "prompt": check_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Low temp for consistent classification
                        "num_predict": 10
                    }
                }
                
                async with session.post(OLLAMA_API_URL, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        response = data.get('response', '').strip().upper()
                        return 'ДА' in response or 'YES' in response
                    return True  # Default to allowing if check fails
        except Exception as e:
            print(f"Error in topic check: {e}")
            return True  # Fail open
    
    @staticmethod
    async def chat(user_id: int, message: str) -> str:
        """
        Process user message and return AI response
        
        Args:
            user_id: User ID for conversation context
            message: User's message
        
        Returns:
            AI response text
        """
        # Initialize conversation history if needed
        if user_id not in CONVERSATIONS:
            CONVERSATIONS[user_id] = []
        
        # Check if on-topic (skip for first few messages to be friendly)
        if len(CONVERSATIONS[user_id]) > 2:  # After 2 exchanges, start checking
            is_relevant = await ConsultantAI.is_on_topic(message)
            if not is_relevant:
                return "🌙 Прости, но я консультант по мистическим практикам. Этот вопрос вне моей компетенции. Давай лучше поговорим о картах Таро или астрологии? 🔮"
        
        # Build context from history
        context = SYSTEM_PROMPT + "\n\nИстория беседы:\n"
        for msg in CONVERSATIONS[user_id][-6:]:  # Last 3 exchanges
            context += f"Пользователь: {msg['user']}\nЛилит: {msg['assistant']}\n"
        
        context += f"\nПользователь: {message}\nЛилит:"
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": MODEL_NAME,
                    "prompt": context,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "num_predict": 300
                    }
                }
                
                async with session.post(OLLAMA_API_URL, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        response = data.get('response', '').strip()
                        
                        # Save to history
                        CONVERSATIONS[user_id].append({
                            'user': message,
                            'assistant': response,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Keep only last 10 exchanges
                        if len(CONVERSATIONS[user_id]) > 10:
                            CONVERSATIONS[user_id] = CONVERSATIONS[user_id][-10:]
                        
                        return response
                    else:
                        return "🌙 Извините, произошла ошибка. Попробуйте еще раз."
        
        except Exception as e:
            print(f"Error in chat: {e}")
            return "🌙 Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже."
    
    @staticmethod
    def clear_history(user_id: int):
        """Clear conversation history for user"""
        if user_id in CONVERSATIONS:
            CONVERSATIONS[user_id] = []
    
    @staticmethod
    def get_history(user_id: int) -> List[Dict]:
        """Get conversation history for user"""
        return CONVERSATIONS.get(user_id, [])

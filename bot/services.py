import random
import uuid
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import User, Reading, TarotCard, Spread, DestinyMatrix
from bot.tarot_data import MAJOR_ARCANA, TAROT_SPREADS, ZODIAC_SIGNS
from bot.database import DatabaseManager
from bot.ai_service import GeminiAI
from bot.external_data import MoonService, NumerologyService


class UserService:
    """Сервис для работы с пользователями"""
    
    @staticmethod
    async def get_or_create_user(telegram_id: int, username: str = None, 
                               first_name: str = None, last_name: str = None) -> User:
        """Получить или создать пользователя"""
        session = await DatabaseManager.get_session()
        try:
            # Попытаться найти существующего пользователя
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                # Создать нового пользователя
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
            else:
                # Обновить информацию пользователя
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.last_activity = datetime.now()
                await session.commit()
            
            return user
        finally:
            await session.close()

    @staticmethod
    async def check_energy(user_id: int) -> bool:
        """Check if user has energy and refill if needed"""
        session = await DatabaseManager.get_session()
        try:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            
            # Check for daily refill
            today = date.today()
            if user.last_energy_refill != today:
                user.energy = max(user.energy, 1)  # Refill to at least 1
                user.last_energy_refill = today
                await session.commit()
            
            return user.energy > 0
        finally:
            await session.close()

    @staticmethod
    async def consume_energy(user_id: int) -> bool:
        """Consume 1 energy point"""
        session = await DatabaseManager.get_session()
        try:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user or user.energy <= 0:
                return False
            
            user.energy -= 1
            await session.commit()
            return True
        finally:
            await session.close()

    @staticmethod
    async def add_stars(user_id: int, amount: int) -> bool:
        """Add stars to user balance"""
        session = await DatabaseManager.get_session()
        try:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            
            user.stars_balance += amount
            await session.commit()
            return True
        finally:
            await session.close()

    @staticmethod
    async def refill_energy(user_id: int, amount: int) -> bool:
        """Add energy pack"""
        session = await DatabaseManager.get_session()
        try:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            
            user.energy += amount
            await session.commit()
            return True
        finally:
            await session.close()

    @staticmethod
    async def update_birth_date(user_id: int, birth_date: date) -> bool:
        """Update user birth date"""
        session = await DatabaseManager.get_session()
        try:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            
            user.birth_date = birth_date
            await session.commit()
            return True
        finally:
            await session.close()

    @staticmethod
    async def update_birth_time(user_id: int, birth_time: str) -> bool:
        """Update user birth time (HH:MM)"""
        session = await DatabaseManager.get_session()
        try:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            
            user.birth_time = birth_time
            await session.commit()
            return True
        finally:
            await session.close()

    @staticmethod
    async def update_birth_place(user_id: int, birth_place: str) -> bool:
        """Update user birth place (city)"""
        session = await DatabaseManager.get_session()
        try:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            
            user.birth_place = birth_place
            # Also reset lat/lng to let engine recalculate them
            user.latitude = None
            user.longitude = None
            await session.commit()
            return True
        finally:
            await session.close()


class TarotService:
    """Сервис для работы с картами Таро"""
    
    @staticmethod
    def get_random_card() -> Dict[str, Any]:
        """Получить случайную карту Таро"""
        card_id = random.choice(list(MAJOR_ARCANA.keys()))
        card_data = MAJOR_ARCANA[card_id].copy()
        
        # Определить, перевернута ли карта
        is_reversed = random.choice([True, False])
        card_data['is_reversed'] = is_reversed
        card_data['id'] = card_id
        
        return card_data
    
    @staticmethod
    def get_cards_for_spread(spread_name: str) -> List[Dict[str, Any]]:
        """Получить карты для конкретного расклада"""
        spread_info = TAROT_SPREADS.get(spread_name)
        if not spread_info:
            raise ValueError(f"Расклад {spread_name} не найден")
        
        cards = []
        used_cards = set()
        
        for i in range(spread_info['card_count']):
            # Избегать повторения карт в одном раскладе
            while True:
                card = TarotService.get_random_card()
                card_key = (card['id'], card['is_reversed'])
                if card_key not in used_cards:
                    used_cards.add(card_key)
                    break
            
            cards.append(card)
        
        return cards
    
    @staticmethod
    async def interpret_card(
        card: Dict[str, Any], 
        position: str = None, 
        question: str = None,
        use_ai: bool = True  # Можно отключить AI для бесплатных раскладов
    ) -> str:
        """Интерпретировать карту с AI и внешними данными"""
        
        if not use_ai:
            # Статическая интерпретация
            from bot.ai_service import _fallback_interpretation
            return _fallback_interpretation(card, position)
        
        # Получаем контекст
        moon = MoonService.get_moon_phase()
        day_num = NumerologyService.get_day_number()
        
        context = {
            'moon_phase': f"{moon['emoji']} {moon['name']}",
            'day_number': f"{day_num['number']}"
        }
        
        # Используем AI для генерации
        interpretation = await GeminiAI.generate_interpretation(
            card=card,
            position=position,
            question=question,
            context=context
        )
        
        return interpretation

    @staticmethod
    async def _ensure_daily_spread_exists(session: AsyncSession) -> Spread:
        """Ensure daily card spread exists in database"""
        result = await session.execute(
            select(Spread).where(Spread.name == "Карта дня")
        )
        spread = result.scalar_one_or_none()
        
        if not spread:
            spread_data = TAROT_SPREADS["daily_card"]
            spread = Spread(
                name=spread_data["name"],
                description=spread_data["description"],
                card_count=spread_data["card_count"],
                positions=spread_data["positions"],
                is_premium=spread_data["is_premium"],
                category=spread_data["category"]
            )
            session.add(spread)
            await session.commit()
            await session.refresh(spread)
            
        return spread

    @staticmethod
    async def get_daily_card(user_id: int) -> Optional[Reading]:
        """Get user's card of the day for today"""
        session = await DatabaseManager.get_session()
        try:
            # Find daily spread
            spread = await TarotService._ensure_daily_spread_exists(session)
            
            # Check for existing reading today
            today = date.today()
            start_of_day = datetime.combine(today, datetime.min.time())
            
            result = await session.execute(
                select(Reading)
                .where(Reading.user_id == user_id)
                .where(Reading.spread_id == spread.id)
                .where(Reading.created_at >= start_of_day)
            )
            return result.scalar_one_or_none()
        finally:
            await session.close()

    @staticmethod
    async def save_reading(user_id: int, spread_id: int, cards: List[Dict[str, Any]], interpretation: str, question: str = None) -> Reading:
        """Save a general tarot reading"""
        session = await DatabaseManager.get_session()
        try:
            reading = Reading(
                user_id=user_id,
                spread_id=spread_id,
                cards_drawn=cards,
                interpretation=interpretation,
                question=question,
                created_at=datetime.now()
            )
            session.add(reading)
            await session.commit()
            await session.refresh(reading)
            return reading
        finally:
            await session.close()

    @staticmethod
    async def save_daily_card(user_id: int, card: Dict[str, Any], interpretation: str) -> Reading:
        """Save user's card of the day"""
        session = await DatabaseManager.get_session()
        try:
            spread = await TarotService._ensure_daily_spread_exists(session)
            
            reading = Reading(
                user_id=user_id,
                spread_id=spread.id,
                cards_drawn=[card],
                interpretation=interpretation,
                created_at=datetime.now()
            )
            session.add(reading)
            await session.commit()
            await session.refresh(reading)
            return reading
        finally:
            await session.close()


from bot.matrix_logic import MatrixService

class DestinyMatrixService:
    """Сервис для расчета Матрицы Судьбы"""
    
    @staticmethod
    def calculate_matrix(birth_date) -> dict:
        """Рассчитать полную Матрицу Судьбы по дате рождения"""
        return MatrixService.calculate_matrix(birth_date)
    
    @staticmethod
    def interpret_matrix(matrix: dict) -> str:
        """Интерпретировать сложную структуру Матрицы Судьбы"""
        interpretation = "🌟 <b>ПОЛНАЯ МАТРИЦА СУДЬБЫ</b> 🌟\n\n"
        
        main = matrix.get('main', {})
        destiny = matrix.get('destiny', {})
        channels = matrix.get('channels', {})
        
        # 1. Личные качества
        interpretation += "🎭 <b>ЛИЧНОСТЬ И СОЦИУМ</b>\n"
        interpretation += f"• Личность (А): {MAJOR_ARCANA.get(main['A'], {}).get('name', main['A'])}\n"
        interpretation += f"• Связь с небом (B): {MAJOR_ARCANA.get(main['B'], {}).get('name', main['B'])}\n"
        interpretation += f"• Зона комфорта (E): {MAJOR_ARCANA.get(main['E'], {}).get('name', main['E'])}\n\n"
        
        # 2. Предназначение
        interpretation += "🎯 <b>ПРЕДНАЗНАЧЕНИЕ</b>\n"
        interpretation += f"• Личное (до 40 лет): {destiny.get('personal')}\n"
        interpretation += f"• Социальное (40-60 лет): {destiny.get('social')}\n"
        interpretation += f"• Духовное (общее): {destiny.get('spiritual')}\n\n"
        
        # 3. Каналы
        interpretation += "💰 <b>КАНАЛЫ</b>\n"
        interpretation += f"• Деньги: {channels.get('money')}\n"
        interpretation += f"• Любовь: {channels.get('love')}\n\n"
        
        interpretation += "<i>Это краткая выжимка. Полный расчет включает 50+ параметров и родовые линии.</i>"
        
        return interpretation

    @staticmethod
    async def save_matrix(user_id: int, birth_date: date, matrix_data: dict, interpretation: str) -> DestinyMatrix:
        """Save calculated matrix to DB"""
        session = await DatabaseManager.get_session()
        try:
            matrix = DestinyMatrix(
                user_id=user_id,
                birth_date=birth_date,
                matrix_data=matrix_data,
                interpretation=interpretation,
                created_at=datetime.now()
            )
            session.add(matrix)
            await session.commit()
            await session.refresh(matrix)
            return matrix
        finally:
            await session.close()


from bot.astro_logic import AstroEngine

class AstroService:
    """Сервис для астрологических прогнозов и натальных карт"""
    
    @staticmethod
    def get_zodiac_sign(birth_date) -> str:
        """Определить знак зодиака по дате рождения (традиционный метод)"""
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
    def calculate_natal_chart(user_name, birth_date, birth_time="12:00", birth_place="Almaty"):
        """Рассчитать полную натальную карту пользователя"""
        try:
            # Parse time
            hour, minute = map(int, birth_time.split(':'))
            
            return AstroEngine.calculate_natal_chart(
                name=user_name,
                year=birth_date.year,
                month=birth_date.month,
                day=birth_date.day,
                hour=hour,
                minute=minute,
                city=birth_place
            )
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def interpret_natal_chart(chart: dict) -> str:
        """Интерпретировать натальную карту (кратко)"""
        if "error" in chart:
            return f"❌ Ошибка расчета: {chart['error']}"
            
        interpretation = f"🪐 <b>НАТАЛЬНАЯ КАРТА: {chart['info']['name']}</b>\n"
        interpretation += f"📍 {chart['info']['city']} | {chart['info']['date']} {chart['info']['time']}\n\n"
        
        # Основные точки
        for p in chart['planets'][:3]: # Sun, Moon, Mercury
            interpretation += f"• <b>{p['name']}:</b> {p['sign']} (дом {p['house']})\n"
        
        # Асцендент
        asc = chart['houses'][0]
        interpretation += f"• <b>Асцендент (ASC):</b> {asc['sign']}\n\n"
        
        interpretation += f"💡 <i>Найдено аспектов: {len(chart['aspects'])}</i>\n\n"
        interpretation += "Полная расшифровка доступна в веб-версии или через AI-консультанта."
        
        return interpretation

    @staticmethod
    async def save_astro_chart(user_id: int, birth_date: date, birth_time: str, birth_place: str, chart_data: dict, interpretation: str) -> Any:
        """Save natal chart to DB"""
        from bot.models import AstroChart
        session = await DatabaseManager.get_session()
        try:
            chart = AstroChart(
                user_id=user_id,
                birth_date=birth_date,
                birth_time=birth_time,
                birth_place=birth_place,
                chart_data=chart_data,
                interpretation=interpretation,
                created_at=datetime.now()
            )
            session.add(chart)
            await session.commit()
            await session.refresh(chart)
            return chart
        finally:
            await session.close()


class RuneService:
    """Сервис для работы с рунами"""
    @staticmethod
    def cast_runes(count: int = 1) -> list:
        from bot.divination_data import RUNE_DATA
        rune_keys = list(RUNE_DATA.keys())
        selected_keys = random.sample(rune_keys, count)
        
        results = []
        for key in selected_keys:
            rune = RUNE_DATA[key].copy()
            rune["key"] = key
            rune["is_reversed"] = random.random() < 0.25
            results.append(rune)
        return results

    @staticmethod
    async def interpret_runes(selected_runes: list, spread_name: str, question: str = None) -> str:
        from bot.ai_service import GeminiAI
        
        runes_str = ", ".join([f"{r['name']} ({'перевернутая' if r['is_reversed'] else 'прямая'})" for r in selected_runes])
        
        prompt = f"""
        Выступай в роли опытного эриля (мастера рун). 
        Расклад: {spread_name}
        Выпавшие руны: {runes_str}
        Вопрос: {question or 'Общий прогноз'}
        
        Дай мистическую и глубокую трактовку. Учти значения каждой руны и их сочетание.
        Пиши в стиле скандинавских саг, но понятно для современного человека.
        Объем: 2-4 абзаца.
        """
        
        return await GeminiAI.generate_interpretation(prompt)

    @staticmethod
    async def save_rune_reading(user_id: int, spread_type: str, runes: list, interpretation: str, question: str = None) -> Any:
        """Save rune reading to DB"""
        from bot.models import RuneReading
        session = await DatabaseManager.get_session()
        try:
            reading = RuneReading(
                user_id=user_id,
                spread_type=spread_type,
                question=question,
                runes_drawn=runes,
                interpretation=interpretation,
                created_at=datetime.now()
            )
            session.add(reading)
            await session.commit()
            await session.refresh(reading)
            return reading
        finally:
            await session.close()


class PsychomatrixService:
    """Сервис для расчета Квадрата Пифагора (Психоматрицы)"""
    @staticmethod
    def calculate(birth_date) -> dict:
        day = f"{birth_date.day:02d}"
        month = f"{birth_date.month:02d}"
        year = f"{birth_date.year}"
        
        digits = [int(d) for d in day + month + year]
        
        # 1-е число: сумма всех цифр даты рождения
        n1 = sum(digits)
        # 2-е число: сумма цифр 1-го числа
        n2 = sum(int(d) for d in str(n1))
        # 3-е число: 1-е число минус (первая отличная от нуля цифра дня рождения * 2)
        first_digit = int(day[0]) if day[0] != '0' else int(day[1])
        n3 = n1 - (first_digit * 2)
        # 4-е число: сумма цифр 3-го числа
        n4 = sum(int(d) for d in str(n3))
        
        all_digits_str = "".join(map(str, digits)) + str(n1) + str(n2) + str(n3) + str(n4)
        
        matrix = {str(i): all_digits_str.count(str(i)) for i in range(1, 10)}
        
        return {
            "matrix": matrix,
            "numbers": [n1, n2, n3, n4],
            "total_digits": all_digits_str
        }

    @staticmethod
    def interpret(matrix_data: dict) -> str:
        m = matrix_data["matrix"]
        
        interpretation = "📜 <b>ПСИХОМАТРИЦА (Квадрат Пифагора)</b>\n\n"
        
        traits = {
            "1": "Характер/Воля",
            "2": "Энергия",
            "3": "Интерес/Наука",
            "4": "Здоровье",
            "5": "Логика/Интуиция",
            "6": "Труд/Мастерство",
            "7": "Удача",
            "8": "Долг/Ответственность",
            "9": "Память/Ум"
        }
        
        for key, name in traits.items():
            count = m[key]
            val = "нет" if count == 0 else "I" * count
            interpretation += f"• <b>{name}:</b> {val}\n"
            
        interpretation += "\n<i>Это базовые черты вашей личности по классической нумерологии.</i>"
        return interpretation

    @staticmethod
    async def save_psychomatrix_result(user_id: int, birth_date: date, matrix_data: dict, interpretation: str) -> Any:
        """Save psychomatrix result to DB"""
        from bot.models import PsychomatrixResult
        session = await DatabaseManager.get_session()
        try:
            result = PsychomatrixResult(
                user_id=user_id,
                birth_date=birth_date,
                matrix_data=matrix_data,
                interpretation=interpretation,
                created_at=datetime.now()
            )
            session.add(result)
            await session.commit()
            await session.refresh(result)
            return result
        finally:
            await session.close()


class DreamService:
    """Сервис толкования снов"""
    @staticmethod
    async def interpret_dream(description: str) -> str:
        from bot.ai_service import GeminiAI
        
        prompt = f"""
        Ты — мудрый толкователь снов, эксперт в глубинной психологии (по Юнгу) и эзотерических символах.
        Пользователь описал свой сон: "{description}"
        
        Проанализируй этот сон:
        1. Ключевые символы и их значение.
        2. Психологический подтекст (что хочет сказать подсознание).
        3. Эзотерическое послание или совет.
        
        Пиши мягко, но глубоко. Объем: 3-5 абзацев.
        """
        
        return await GeminiAI.generate_general_interpretation(prompt)


class MoonService:
    """Сервис лунного календаря"""
    @staticmethod
    def get_todays_advice() -> dict:
        today = date.today()
        # Simple algorithm to estimate lunar day (very approximate)
        lunar_day = (today.day % 30) + 1
        
        advice = {
            "lunar_day": lunar_day,
            "phase": "Растущая" if lunar_day < 15 else "Убывающая",
            "advice": "Сегодня благоприятный день для новых начинаний и творчества." if lunar_day < 15 else "Хорошее время для очищения, завершения дел и отдыха."
        }
        return advice

    @staticmethod
    def get_moon_phase() -> dict:
        """Get current moon phase"""
        today = date.today()
        day_num = (today.day % 30) + 1
        
        phase_name = "Растущая" if day_num < 15 else "Убывающая"
        emoji = "🌑" if day_num == 1 else "🌓" if day_num < 8 else "🌕" if day_num == 15 else "🌗"
        
        return {
            "name": phase_name,
            "emoji": emoji,
            "day": day_num
        }


class IChingService:
    """Сервис И-Цзин (Книга Перемен)"""
    @staticmethod
    def throw_coins() -> list:
        # 3 coins throw, 6 times
        hexagram = []
        for _ in range(6):
            # 2 = yin, 3 = yang
            throw = sum(random.choice([2, 3]) for _ in range(3))
            hexagram.append(throw)
        return hexagram

    @staticmethod
    async def interpret_hexagram(hexagram: list, question: str = None) -> str:
        from bot.ai_service import GeminiAI
        
        hex_str = "-".join(map(str, hexagram))
        
        prompt = f"""
        Выступай в роли мастера И-Цзин. 
        Гексаграмма (код бросков): {hex_str}
        Вопрос: {question or 'Общий прогноз'}
        
        Дай философскую и глубокую трактовку согласно «Книге Перемен». 
        Объясни значение полученной гексаграммы и дай совет.
        Объем: 3-4 абзаца.
        """
        
        return await GeminiAI.generate_general_interpretation(prompt)


class CompatibilityService:
    """Сервис совместимости по Матрице Судьбы"""
    @staticmethod
    def calculate_compatibility(date1: str, date2: str) -> dict:
        from bot.services import DestinyMatrixService
        from datetime import datetime
        
        # Parse dates
        d1 = datetime.strptime(date1, "%d.%m.%Y").date()
        d2 = datetime.strptime(date2, "%d.%m.%Y").date()
        
        m1 = DestinyMatrixService.calculate_matrix(d1)
        m2 = DestinyMatrixService.calculate_matrix(d2)
        
        # Central energy of compatibility is sum of central energies
        def calc_arcana(a, b):
            res = (a + b) % 22
            return res if res != 22 else 22
            
        compatibility = {
            "center": calc_arcana(m1["center"], m2["center"]),
            "purpose": calc_arcana(m1["purpose_personal"], m2["purpose_personal"]),
            "karma": calc_arcana(m1["karma"][0], m2["karma"][0])
        }
        return compatibility

    @staticmethod
    async def interpret_compatibility(comp_data: dict) -> str:
        from bot.ai_service import GeminiAI
        prompt = f"""
        Ты — эксперт по совместимости и Матрице Судьбы. 
        Рассчитана совместимость пары:
        Центральная энергия пары: {comp_data['center']} - это "Лицо пары" и их общая задача.
        Общее предназначение: {comp_data['purpose']}
        Кармическая задача: {comp_data['karma']}
        
        Дай глубокий анализ этих отношений:
        1. В чем сила этой пары?
        2. Какие могут быть конфликты?
        3. Совет для гармонизации отношений.
        
        Пиши вдохновляюще. 3-4 абзаца.
        """
        return await GeminiAI.generate_general_interpretation(prompt)

    @staticmethod
    async def save_compatibility_result(user_id: int, partner_name: str, partner_birth_date: date, compatibility_data: dict, interpretation: str) -> Any:
        """Save compatibility result to DB"""
        from bot.models import CompatibilityResult
        session = await DatabaseManager.get_session()
        try:
            result = CompatibilityResult(
                user_id=user_id,
                partner_name=partner_name,
                partner_birth_date=partner_birth_date,
                compatibility_data=compatibility_data,
                interpretation=interpretation,
                created_at=datetime.now()
            )
            session.add(result)
            await session.commit()
            await session.refresh(result)
            return result
        finally:
            await session.close()
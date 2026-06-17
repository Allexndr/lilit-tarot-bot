"""
Обработчики команд для Telegram бота АРУАХ
"""

import logging
from datetime import datetime
from aiogram import types, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from telegram_bot.services import UserService, TarotService, NumerologyService, AstrologyService
from telegram_bot.services import ChakraService, DestinyMatrixService, HumanDesignService
from telegram_bot.subscription_service import SubscriptionService
from shared.tarot_data import TAROT_SPREADS, ZODIAC_SIGNS

logger = logging.getLogger(__name__)

# Router для обработчиков
router = Router()

# Состояния для FSM
class UserStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_birth_date = State()
    waiting_for_birth_time = State()
    waiting_for_birth_place = State()


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура"""
    buttons = [
        [InlineKeyboardButton(text="🔮 Таро", callback_data="tarot_menu")],
        [InlineKeyboardButton(text="🔢 Нумерология", callback_data="numerology_menu")],
        [InlineKeyboardButton(text="⭐ Астрология", callback_data="astrology_menu")],
        [InlineKeyboardButton(text="🌈 Чакры", callback_data="chakras_menu")],
        [InlineKeyboardButton(text="🌟 Матрица Судьбы", callback_data="matrix_menu")],
        [InlineKeyboardButton(text="🧬 Human Design", callback_data="human_design_menu")],
        [InlineKeyboardButton(text="📊 Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="💎 Подписка", callback_data="subscription")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_tarot_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура Таро"""
    buttons = [
        [InlineKeyboardButton(text="🔮 Карта дня", callback_data="daily_card")],
        [InlineKeyboardButton(text="🎯 Да/Нет", callback_data="yes_no")],
        [InlineKeyboardButton(text="🛤 Путь (3 карты)", callback_data="three_cards")],
        [InlineKeyboardButton(text="💖 Отношения", callback_data="love_spread")],
        [InlineKeyboardButton(text="🎭 Диалог с Арканом", callback_data="arcana_dialogue")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_numerology_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура нумерологии"""
    buttons = [
        [InlineKeyboardButton(text="🔢 Число жизненного пути", callback_data="life_path")],
        [InlineKeyboardButton(text="⭐ Число судьбы", callback_data="destiny_number")],
        [InlineKeyboardButton(text="📊 Квадрат Пифагора", callback_data="pythagorean_square")],
        [InlineKeyboardButton(text="🗓 Персональный год", callback_data="personal_year")],
        [InlineKeyboardButton(text="💕 Совместимость", callback_data="compatibility")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    # Создать или получить пользователя
    user = await UserService.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    welcome_text = f"""
🌙 Добро пожаловать в АРУАХ, {user.first_name or 'Путник'}!

Я - ваш духовный проводник в мире эзотерических знаний. Я помогу вам:

✨ Получить расклады Таро на любые вопросы
🔮 Узнать свою Матрицу Судьбы
🌟 Получить астрологические прогнозы
💫 Поговорить с Арканами напрямую
🌈 Диагностировать состояние чакр
🧬 Узнать свой Human Design

Выберите, что вас интересует:
"""
    
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик возврата в главное меню"""
    await state.clear()
    
    welcome_text = """
🌙 **АРУАХ - Ваш духовный проводник**

Выберите, что вас интересует:
"""
    
    await callback.message.edit_text(welcome_text, reply_markup=get_main_keyboard())


# === ТАРО ОБРАБОТЧИКИ ===

@router.callback_query(F.data == "tarot_menu")
async def tarot_menu_handler(callback: CallbackQuery):
    """Обработчик меню Таро"""
    text = """
🔮 **ТАРО**

Выберите тип расклада:

• **Карта дня** - ежедневный совет
• **Да/Нет** - ответ на вопрос
• **Путь** - прошлое, настоящее, будущее
• **Отношения** - анализ любовных связей
• **Диалог с Арканом** - поговорить с картой
"""
    
    await callback.message.edit_text(text, reply_markup=get_tarot_keyboard())


@router.callback_query(F.data == "daily_card")
async def daily_card_handler(callback: CallbackQuery):
    """Обработчик карты дня"""
    try:
        # Проверить лимиты пользователя
        user_id = callback.from_user.id
        can_request = await SubscriptionService.can_make_request(user_id)
        
        if not can_request["can_request"]:
            if can_request["reason"] == "daily_limit_exceeded":
                await callback.answer("Лимит запросов исчерпан. Обновите подписку.")
            else:
                await callback.answer("Ошибка при проверке лимитов.")
            return
        
        # Получить карту дня
        card = await TarotService.get_daily_card(user_id)
        
        # Интерпретировать карту
        interpretation = await TarotService.interpret_card(card, "Энергия дня")
        
        # Увеличить счётчик запросов
        await SubscriptionService.increment_request_count(user_id)
        
        await callback.message.edit_text(
            interpretation,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔮 Ещё карта", callback_data="daily_card")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ]),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при создании карты дня: {e}")
        await callback.answer("Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data == "yes_no")
async def yes_no_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик расклада Да/Нет"""
    await callback.message.edit_text(
        "🎯 **Расклад 'Да/Нет'**\n\n"
        "Задайте ваш вопрос, на который можно ответить 'да' или 'нет'.\n\n"
        "Например: 'Стоит ли мне сменить работу?'",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="tarot_menu")]
        ])
    )
    await state.set_state(UserStates.waiting_for_question)
    await state.update_data(spread_type="yes_no")


@router.callback_query(F.data == "three_cards")
async def three_cards_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик расклада на 3 карты"""
    await callback.message.edit_text(
        "🛤 **Расклад 'Путь'**\n\n"
        "Этот расклад покажет связь прошлого, настоящего и будущего.\n\n"
        "Задайте ваш вопрос или нажмите 'Без вопроса' для общего расклада:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Без вопроса", callback_data="three_cards_no_question")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="tarot_menu")]
        ])
    )
    await state.set_state(UserStates.waiting_for_question)
    await state.update_data(spread_type="three_cards")


@router.callback_query(F.data == "three_cards_no_question")
async def three_cards_no_question_handler(callback: CallbackQuery):
    """Обработчик расклада на 3 карты без вопроса"""
    try:
        user = await UserService.get_or_create_user(callback.from_user.id)
        if not await UserService.can_make_request(user):
            await callback.answer("Лимит запросов исчерпан. Обновите подписку.")
            return
        
        # Создать расклад
        reading = await TarotService.create_reading(
            user_id=user.id,
            spread_type="three_cards",
            question=None
        )
        
        await callback.message.edit_text(
            reading['interpretation'],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔮 Ещё расклад", callback_data="three_cards")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ]),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при создании расклада: {e}")
        await callback.answer("Произошла ошибка. Попробуйте позже.")


# === НУМЕРОЛОГИЯ ОБРАБОТЧИКИ ===

@router.callback_query(F.data == "numerology_menu")
async def numerology_menu_handler(callback: CallbackQuery):
    """Обработчик меню нумерологии"""
    text = """
🔢 **НУМЕРОЛОГИЯ**

Выберите тип расчёта:

• **Число жизненного пути** - ваше предназначение
• **Число судьбы** - по имени
• **Квадрат Пифагора** - полный анализ
• **Персональный год** - влияние года
• **Совместимость** - с партнёром
"""
    
    await callback.message.edit_text(text, reply_markup=get_numerology_keyboard())


@router.callback_query(F.data == "life_path")
async def life_path_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик числа жизненного пути"""
    await callback.message.edit_text(
        "🔢 **Число жизненного пути**\n\n"
        "Введите дату рождения в формате ДД.ММ.ГГГГ\n\n"
        "Например: 15.05.1990",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="numerology_menu")]
        ])
    )
    await state.set_state(UserStates.waiting_for_birth_date)
    await state.update_data(calculation_type="life_path")


@router.callback_query(F.data == "destiny_number")
async def destiny_number_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик числа судьбы"""
    await callback.message.edit_text(
        "⭐ **Число судьбы**\n\n"
        "Введите ваше полное имя (как в паспорте)\n\n"
        "Например: Александр Иванович Петров",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="numerology_menu")]
        ])
    )
    await state.set_state(UserStates.waiting_for_question)
    await state.update_data(calculation_type="destiny_number")


# === ОБРАБОТЧИКИ СООБЩЕНИЙ ===

@router.message(StateFilter(UserStates.waiting_for_question))
async def process_question(message: types.Message, state: FSMContext):
    """Обработчик вопроса пользователя"""
    data = await state.get_data()
    spread_type = data.get('spread_type')
    calculation_type = data.get('calculation_type')
    question = message.text
    
    try:
        user = await UserService.get_or_create_user(message.from_user.id)
        
        if spread_type == "yes_no":
            # Расклад Да/Нет
            if not await UserService.can_make_request(user):
                await message.answer("Лимит запросов исчерпан. Обновите подписку.")
                return
            
            reading = await TarotService.create_reading(
                user_id=user.id,
                spread_type="yes_no",
                question=question
            )
            
            await message.answer(
                reading['interpretation'],
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔮 Ещё расклад", callback_data="yes_no")],
                    [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
                ]),
                parse_mode="Markdown"
            )
            
        elif spread_type == "three_cards":
            # Расклад на 3 карты
            if not await UserService.can_make_request(user):
                await message.answer("Лимит запросов исчерпан. Обновите подписку.")
                return
            
            reading = await TarotService.create_reading(
                user_id=user.id,
                spread_type="three_cards",
                question=question
            )
            
            await message.answer(
                reading['interpretation'],
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔮 Ещё расклад", callback_data="three_cards")],
                    [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
                ]),
                parse_mode="Markdown"
            )
            
        elif calculation_type == "destiny_number":
            # Число судьбы
            if not await UserService.can_make_request(user):
                await message.answer("Лимит запросов исчерпан. Обновите подписку.")
                return
            
            result = await NumerologyService.calculate_destiny_number(user.id, question)
            
            await message.answer(
                result['interpretation'],
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔢 Ещё расчёт", callback_data="destiny_number")],
                    [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
                ]),
                parse_mode="Markdown"
            )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка при обработке вопроса: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(StateFilter(UserStates.waiting_for_birth_date))
async def process_birth_date(message: types.Message, state: FSMContext):
    """Обработчик даты рождения"""
    data = await state.get_data()
    calculation_type = data.get('calculation_type')
    birth_date_str = message.text
    
    try:
        # Парсинг даты
        from datetime import datetime
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").date()
        
        user = await UserService.get_or_create_user(message.from_user.id)
        
        if calculation_type == "life_path":
            # Число жизненного пути
            if not await UserService.can_make_request(user):
                await message.answer("Лимит запросов исчерпан. Обновите подписку.")
                return
            
            result = await NumerologyService.calculate_life_path(user.id, birth_date)
            
            await message.answer(
                result['interpretation'],
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔢 Ещё расчёт", callback_data="life_path")],
                    [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
                ]),
                parse_mode="Markdown"
            )
        
        await state.clear()
        
    except ValueError:
        await message.answer("Неверный формат даты. Используйте ДД.ММ.ГГГГ")
    except Exception as e:
        logger.error(f"Ошибка при обработке даты рождения: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# === ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ===

@router.callback_query(F.data == "profile")
async def profile_handler(callback: CallbackQuery):
    """Обработчик профиля пользователя"""
    user = await UserService.get_or_create_user(callback.from_user.id)
    
    profile_text = f"""
👤 **Ваш профиль**

🆔 ID: {user.telegram_id}
👤 Имя: {user.first_name or 'Не указано'}
📊 Всего запросов: {user.total_requests}
📅 Дата регистрации: {user.registration_date.strftime('%d.%m.%Y')}
💎 Подписка: {user.subscription_type}
🔢 Запросов сегодня: {user.daily_requests}/{user.daily_limit}
💰 Потрачено: {user.total_spent} тиын
"""
    
    await callback.message.edit_text(
        profile_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📅 Указать дату рождения", callback_data="set_birth_date")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ])
    )


# === ПОДПИСКА ===

@router.callback_query(F.data == "subscription")
async def subscription_handler(callback: CallbackQuery):
    """Обработчик подписки"""
    user = await UserService.get_or_create_user(callback.from_user.id)
    
    subscription_text = f"""
💎 **Подписка**

**Текущий тариф:** {user.subscription_type}

**Доступные тарифы:**

🆓 **FREE** (0₸/мес)
• 3 запроса в день
• Базовые функции

💎 **PREMIUM** (2,500₸/мес)
• Безлимит запросов
• Все функции
• PDF-отчёты

🌟 **VIP** (15,000₸/консультация)
• Живая консультация
• Персональный прогноз
• Закрытое комьюнити
"""
    
    await callback.message.edit_text(
        subscription_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Оформить Premium", callback_data="buy_premium")],
            [InlineKeyboardButton(text="🌟 VIP консультация", callback_data="buy_vip")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ])
    )

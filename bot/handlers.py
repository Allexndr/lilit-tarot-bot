import logging
from datetime import datetime
from aiogram import types, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.services import (
    UserService, TarotService, DestinyMatrixService, AstroService, 
    RuneService, PsychomatrixService, DreamService, IChingService, CompatibilityService
)
from bot.tarot_data import TAROT_SPREADS, MAJOR_ARCANA
from bot.consultant_ai import ConsultantAI

logger = logging.getLogger(__name__)

# Router для обработчиков
router = Router()

# Состояния для FSM
class TarotStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_birth_date = State()
    waiting_for_birth_time = State()  # New
    waiting_for_birth_place = State()  # New
    waiting_for_arcana_question = State()
    waiting_for_rune_question = State() # New
    waiting_for_dream_description = State() # New
    waiting_for_iching_question = State() # New
    waiting_for_partner_date = State() # New
    consulting = State()  # New state for AI consultant chat


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура"""
    buttons = [
        [InlineKeyboardButton(text="🔮 Карта дня", callback_data="daily_card")],
        [InlineKeyboardButton(text="🎯 Да/Нет", callback_data="yes_no")],
        [InlineKeyboardButton(text="🛤 Путь (3 карты)", callback_data="three_cards")],
        [InlineKeyboardButton(text="💖 Отношения", callback_data="love_spread")],
        [InlineKeyboardButton(text="🔥 Секс и Страсть", callback_data="sex_spread")],
        [InlineKeyboardButton(text="⭐️ Матрица Судьбы", callback_data="destiny_matrix")],
        [InlineKeyboardButton(text="🪐 Астрология", callback_data="astrology")],
        [InlineKeyboardButton(text="ᚠ Руны", callback_data="runes_menu")],
        [InlineKeyboardButton(text="🔢 Психоматрица", callback_data="psychomatrix")],
        [InlineKeyboardButton(text="🌙 Толкование снов", callback_data="dream_start")],
        [InlineKeyboardButton(text="🏮 И-Цзин", callback_data="iching_start")],
        [InlineKeyboardButton(text="❤️ Совместимость", callback_data="compatibility_start")],
        [InlineKeyboardButton(text="🔗 Диалог с Арканом", callback_data="arcana_dialogue")],
        [InlineKeyboardButton(text="💬 Консультант 24/7", callback_data="consultant")],
        [InlineKeyboardButton(text="👩‍🔮 Живые тарологи", callback_data="tarologists_0")],
        [InlineKeyboardButton(text="📊 Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="💎 Подписка", callback_data="subscription")]
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
🌙 Добро пожаловать в мир Таро, {user.first_name or 'Путник'}!

Я - ЛИЛИТ, ваш проводник в мире эзотерических знаний. Я помогу вам:

✨ Получить расклады Таро на любые вопросы
🔮 Узнать свою Матрицу Судьбы
🌟 Получить астрологические прогнозы
💫 Поговорить с Арканами напрямую

Выберите, что вас интересует:
"""
    
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "daily_card")
async def daily_card_handler(callback: CallbackQuery):
    """Обработчик карты дня"""
    try:
        # Получить пользователя
        user = await UserService.get_or_create_user(callback.from_user.id)
        
        # Проверить, есть ли уже карта на сегодня
        existing_reading = await TarotService.get_daily_card(user.id)
        
        if existing_reading:
            # Если карта уже есть, показать её
            interpretation = existing_reading.interpretation
            # Добавить пометку, что это уже вытянутая карта
            interpretation = f"📅 <b>Ваша карта дня на сегодня:</b>\n\n{interpretation}"
        else:
            # Если карты нет, вытянуть новую
            card = TarotService.get_random_card()
            
            # Интерпретировать карту БЕЗ AI (бесплатная фича, экономим запросы)
            interpretation = await TarotService.interpret_card(card, "Энергия дня", use_ai=False)
            
            # Добавить специальный совет для карты дня
            interpretation += f"\n\n🌅 <b>Совет на день:</b>\n"
            interpretation += f"Позвольте энергии {card['name']} направлять вас сегодня."
            
            # Сохранить карту
            await TarotService.save_daily_card(user.id, card, interpretation)
        
        await callback.message.edit_text(
            interpretation, 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при создании карты дня: {e}")
        await callback.answer("Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data == "yes_no")
async def yes_no_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик расклада Да/Нет"""
    # Check energy
    if not await UserService.check_energy(callback.from_user.id):
        return await show_paywall(callback)

    await callback.message.edit_text(
        "🎯 <b>Расклад 'Да/Нет'</b>\n\n"
        "Задайте ваш вопрос, на который можно ответить 'да' или 'нет'.\n\n"
        "Например: 'Стоит ли мне сменить работу?'",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ])
    )
    await state.set_state(TarotStates.waiting_for_question)
    await state.update_data(spread_type="yes_no")


@router.callback_query(F.data == "three_cards")
async def three_cards_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик расклада на 3 карты"""
    # Check energy
    if not await UserService.check_energy(callback.from_user.id):
        return await show_paywall(callback)

    await callback.message.edit_text(
        "🛤 <b>Расклад 'Путь'</b>\n\n"
        "Этот расклад покажет связь прошлого, настоящего и будущего.\n\n"
        "Задайте ваш вопрос или нажмите 'Без вопроса' для общего расклада:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Без вопроса", callback_data="three_cards_no_question")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ])
    )
    await state.set_state(TarotStates.waiting_for_question)
    await state.update_data(spread_type="three_cards")


@router.callback_query(F.data == "love_spread")
async def love_spread_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик расклада на отношения"""
    # Check energy
    if not await UserService.check_energy(callback.from_user.id):
        return await show_paywall(callback)

    await callback.message.edit_text(
        "💖 <b>Расклад 'Отношения'</b>\n\n"
        "Этот расклад поможет понять чувства партнера и перспективы отношений.\n\n"
        "Задайте ваш вопрос (например, 'Что он чувствует ко мне?') или нажмите 'Без вопроса':",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Без вопроса", callback_data="love_spread_no_question")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ])
    )
    await state.set_state(TarotStates.waiting_for_question)
    await state.update_data(spread_type="love_spread")


@router.callback_query(F.data == "sex_spread")
async def sex_spread_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик расклада Секс и Страсть"""
    # Check energy
    if not await UserService.check_energy(callback.from_user.id):
        return await show_paywall(callback)

    await callback.message.edit_text(
        "🔥 <b>Расклад 'Секс и Страсть'</b>\n\n"
        "Раскройте тайные желания и сексуальную совместимость.\n\n"
        "Задайте вопрос или нажмите 'Без вопроса':",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Без вопроса", callback_data="sex_spread_no_question")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ])
    )
    await state.set_state(TarotStates.waiting_for_question)
    await state.update_data(spread_type="sex_spread")


@router.callback_query(F.data == "destiny_matrix")
async def destiny_matrix_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик Матрицы Судьбы"""
    # Получить пользователя
    user = await UserService.get_or_create_user(callback.from_user.id)
    
    # Проверить наличие даты рождения
    if not user.birth_date:
        await callback.message.edit_text(
            "📍 <b>Для расчета Матрицы Судьбы необходимо указать вашу дату рождения.</b>\n\n"
            "Пожалуйста, введите дату в формате: ДД.ММ.ГГГГ\n"
            "(Например: 15.03.1994)",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        await state.set_state(TarotStates.waiting_for_birth_date)
        return

    # Check energy
    if not await UserService.check_energy(callback.from_user.id):
        return await show_paywall(callback)
        
    # Real Matrix calculation
    matrix_data = DestinyMatrixService.calculate_matrix(user.birth_date)
    interpretation = DestinyMatrixService.interpret_matrix(matrix_data)
    
    await callback.message.edit_text(
        interpretation,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    # Consume energy
    await UserService.consume_energy(callback.from_user.id)

@router.callback_query(F.data == "astrology")
async def astrology_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик Астрологии"""
    user = await UserService.get_or_create_user(callback.from_user.id)
    
    # Check birth date first
    if not user.birth_date:
        await callback.message.edit_text(
            "📅 <b>Для астрологического прогноза нужна ваша дата рождения.</b>\n\n"
            "Пожалуйста, введите её в формате: ДД.ММ.ГГГГ",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        await state.set_state(TarotStates.waiting_for_birth_date)
        return

    # Check birth time
    if not user.birth_time:
        await callback.message.edit_text(
            "⏰ <b>Теперь укажите время вашего рождения.</b>\n\n"
            "Это нужно для точного расчета домов и Асцендента.\n"
            "Формат: ЧЧ:ММ (например, 14:30). Если не знаете — введите 12:00.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🤷‍♂️ Не знаю (12:00)", callback_data="set_time_12:00")],
                [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        await state.set_state(TarotStates.waiting_for_birth_time)
        return

    # Check birth place
    if not user.birth_place:
        await callback.message.edit_text(
            "🏙 <b>И последнее: ваш город рождения.</b>\n\n"
            "Напишите название города (например: Москва или Алматы).",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        await state.set_state(TarotStates.waiting_for_birth_place)
        return

    # All data present, perform calculation
    if not await UserService.check_energy(callback.from_user.id):
        return await show_paywall(callback)

    chart = AstroService.calculate_natal_chart(
        user_name=user.first_name or "Путник",
        birth_date=user.birth_date,
        birth_time=user.birth_time,
        birth_place=user.birth_place
    )
    
    interpretation = AstroService.interpret_natal_chart(chart)
    
    await callback.message.edit_text(
        interpretation,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await UserService.consume_energy(callback.from_user.id)

@router.callback_query(F.data.startswith("set_time_"))
async def set_time_callback(callback: CallbackQuery, state: FSMContext):
    """Быстрая установка времени 12:00"""
    time_str = callback.data.split("_")[-1]
    user = await UserService.get_or_create_user(callback.from_user.id)
    await UserService.update_birth_time(user.id, time_str)
    await astrology_handler(callback, state)

@router.message(StateFilter(TarotStates.waiting_for_birth_time))
async def process_birth_time(message: types.Message, state: FSMContext):
    """Обработчик ввода времени рождения"""
    try:
        time_str = message.text.strip()
        # Валидация
        hour, minute = map(int, time_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
            
        user = await UserService.get_or_create_user(message.from_user.id)
        await UserService.update_birth_time(user.id, f"{hour:02d}:{minute:02d}")
        
        # Переходим к следующему шагу
        await state.clear()
        
        # Вызываем основной обработчик для проверки следующего шага
        # (AIogram doesn't allow calling callback handlers with messages easily, so we just prompt)
        await message.answer(
            f"✅ <b>Время {time_str} сохранено!</b>\n\n"
            "Нажмите кнопку ниже, чтобы продолжить.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Дальше", callback_data="astrology")]
            ]),
            parse_mode="HTML"
        )
    except Exception:
        await message.answer("❌ <b>Неверный формат времени.</b>\nВведите время как ЧЧ:ММ (напр. 15:45)")

@router.message(StateFilter(TarotStates.waiting_for_birth_place))
async def process_birth_place(message: types.Message, state: FSMContext):
    """Обработчик ввода города"""
    city = message.text.strip()
    user = await UserService.get_or_create_user(message.from_user.id)
    await UserService.update_birth_place(user.id, city)
    
    await state.clear()
    await message.answer(
        f"✅ <b>Город {city} сохранен!</b>\n\n"
        "Теперь всё готово для расчета натальной карты.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🪐 Рассчитать карту", callback_data="astrology")]
        ]),
        parse_mode="HTML"
    )

# ===== Runes Handlers =====

@router.callback_query(F.data == "runes_menu")
async def runes_menu_handler(callback: CallbackQuery):
    """Меню рун"""
    text = "ᚠ <b>ДРЕВНИЕ РУНЫ</b> ᚠ\n\nВыберите тип расклада:"
    buttons = [
        [InlineKeyboardButton(text="Одна руна (Совет)", callback_data="runes_cast_single_rune")],
        [InlineKeyboardButton(text="Три Норны (Прошлое-Наст-Буд)", callback_data="runes_cast_norns")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="HTML")

@router.callback_query(F.data.startswith("runes_cast_"))
async def rune_cast_handler(callback: CallbackQuery, state: FSMContext):
    """Начало броска рун"""
    spread_type = callback.data.replace("runes_cast_", "")
    await state.update_data(spread_type=spread_type)
    
    await callback.message.edit_text(
        "🔮 <b>О чем вы хотите спросить руны?</b>\n\n"
        "Введите ваш вопрос или нажмите кнопку ниже для общего прогноза.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Общий прогноз", callback_data="runes_final_cast")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="runes_menu")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(TarotStates.waiting_for_rune_question)

@router.message(StateFilter(TarotStates.waiting_for_rune_question))
async def process_rune_question(message: types.Message, state: FSMContext):
    """Обработка вопроса для рун"""
    await state.update_data(question=message.text)
    await perform_final_rune_cast(message, state)

@router.callback_query(F.data == "runes_final_cast")
async def rune_final_cast_callback(callback: CallbackQuery, state: FSMContext):
    """Конечный бросок через кнопку"""
    await perform_final_rune_cast(callback.message, state)

async def perform_final_rune_cast(message, state: FSMContext):
    """Выполнение броска рун и AI трактовка"""
    data = await state.get_data()
    spread_type = data.get("spread_type", "single_rune")
    question = data.get("question")
    
    # Check energy
    user = await UserService.get_or_create_user(message.chat.id if hasattr(message, 'chat') else message.from_user.id)
    if not await UserService.check_energy(user.id):
        # We need a callback to show paywall, or just a message
        await message.answer("⚡️ Недостаточно энергии для гадания.")
        await state.clear()
        return

    from bot.divination_data import RUNE_SPREADS
    spread = RUNE_SPREADS.get(spread_type)
    
    # Show status
    status_msg = await message.answer("ᚠ <i>Бросаю руны на полотно судьбы...</i>", parse_mode="HTML")
    
    runes = RuneService.cast_runes(spread["rune_count"])
    interpretation = await RuneService.interpret_runes(runes, spread["name"], question)
    
    # Format message
    res_text = f"ᚠ <b>РАСКЛАД: {spread['name']}</b> ᚠ\n"
    if question:
        res_text += f"❓ Вопрос: {question}\n\n"
    
    for i, r in enumerate(runes):
        pos = spread["positions"][i]
        orient = " (перевернутая)" if r["is_reversed"] else " (прямая)"
        res_text += f"• <b>{pos}:</b> {r['name']}{orient}\n"
        
    res_text += f"\n✨ <b>ТРАКТОВКА:</b>\n{interpretation}"
    
    await status_msg.edit_text(
        res_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await UserService.consume_energy(user.id)
    await state.clear()

# ===== Psychomatrix Handler =====

@router.callback_query(F.data == "psychomatrix")
async def psychomatrix_handler(callback: CallbackQuery, state: FSMContext):
    """Квадрат Пифагора"""
    user = await UserService.get_or_create_user(callback.from_user.id)
    
    if not user.birth_date:
        await callback.message.edit_text(
            "🔢 <b>Для расчета Психоматрицы нужна дата рождения.</b>\n\n"
            "Пожалуйста, введите её в формате: ДД.ММ.ГГГГ",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        await state.set_state(TarotStates.waiting_for_birth_date)
        return

    # Check energy
    if not await UserService.check_energy(user.id):
        return await show_paywall(callback)

    data = PsychomatrixService.calculate(user.birth_date)
    interpretation = PsychomatrixService.interpret(data)
    
    await callback.message.edit_text(
        interpretation,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await UserService.consume_energy(user.id)


# ===== Dream Interpreter Handlers =====

@router.callback_query(F.data == "dream_start")
async def dream_start_handler(callback: CallbackQuery, state: FSMContext):
    """Начало толкования сна"""
    await callback.message.edit_text(
        "🌙 <b>ТОЛКОВАНИЕ СНОВ</b> 🌙\n\n"
        "Опишите ваш сон как можно подробнее. Что вы видели? Какие чувства испытывали?\n\n"
        "<i>AI проанализирует символы и даст глубокую трактовку.</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(TarotStates.waiting_for_dream_description)

@router.message(TarotStates.waiting_for_dream_description)
async def process_dream_description(message: types.Message, state: FSMContext):
    """Процесс толкования сна"""
    user = await UserService.get_or_create_user(message.from_user.id)
    if not await UserService.check_energy(user.id):
        await message.answer("⚡️ Недостаточно энергии.")
        await state.clear()
        return

    status_msg = await message.answer("🌙 <i>Погружаюсь в мир ваших снов...</i>", parse_mode="HTML")
    interpretation = await DreamService.interpret_dream(message.text)
    
    await status_msg.edit_text(
        f"🌙 <b>ВАШ СОН:</b>\n\n{interpretation}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await UserService.consume_energy(user.id)
    await state.clear()

# ===== I-Ching Handlers =====

@router.callback_query(F.data == "iching_start")
async def iching_start_handler(callback: CallbackQuery, state: FSMContext):
    """Начало И-Цзин"""
    await callback.message.edit_text(
        "🏮 <b>И-ЦЗИН (КНИГА ПЕРЕМЕН)</b> 🏮\n\n"
        "Сформулируйте ваш вопрос к древней мудрости или просто нажмите кнопку для общего прогноза.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Общий прогноз", callback_data="iching_final")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(TarotStates.waiting_for_iching_question)

@router.message(TarotStates.waiting_for_iching_question)
async def process_iching_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await perform_final_iching(message, state)

@router.callback_query(F.data == "iching_final")
async def iching_final_callback(callback: CallbackQuery, state: FSMContext):
    await perform_final_iching(callback.message, state)

async def perform_final_iching(message, state: FSMContext):
    user_id = message.chat.id if hasattr(message, 'chat') else message.from_user.id
    user = await UserService.get_or_create_user(user_id)
    if not await UserService.check_energy(user.id):
        await message.answer("⚡️ Недостаточно энергии.")
        return

    data = await state.get_data()
    question = data.get("question")
    
    status_msg = await message.answer("🏮 <i>Бросаю монеты...</i>", parse_mode="HTML")
    hexagram = IChingService.throw_coins()
    interpretation = await IChingService.interpret_hexagram(hexagram, question)
    
    # Simple hexagram visualization
    hex_viz = ""
    for line in reversed(hexagram):
        hex_viz += "——  ——\n" if line % 2 == 0 else "——————\n"
        
    res_text = f"🏮 <b>ВАША ГЕКСАГРАММА:</b>\n\n<code>{hex_viz}</code>\n"
    res_text += f"✨ <b>МУДРОСТЬ:</b>\n{interpretation}"
    
    await status_msg.answer(
        res_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await UserService.consume_energy(user.id)
    await state.clear()

# ===== Compatibility Handlers =====

@router.callback_query(F.data == "compatibility_start")
async def compatibility_start_handler(callback: CallbackQuery, state: FSMContext):
    """Начало анализа совместимости"""
    await callback.message.edit_text(
        "❤️ <b>АНАЛИЗ СОВМЕСТИМОСТИ</b> ❤️\n\n"
        "Я проанализирую ваши Матрицы Судьбы и найду точки соприкосновения.\n\n"
        "Введите дату рождения вашего партнера (ДД.ММ.ГГГГ):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(TarotStates.waiting_for_partner_date)

@router.message(TarotStates.waiting_for_partner_date)
async def process_partner_date(message: types.Message, state: FSMContext):
    from datetime import datetime
    user = await UserService.get_or_create_user(message.from_user.id)
    if not user.birth_date:
        await message.answer("⚠️ Сначала укажите свою дату рождения в профиле.")
        await state.clear()
        return

    partner_date = message.text
    # Basic validation
    try:
        datetime.strptime(partner_date, "%d.%m.%Y")
    except:
        await message.answer("❌ Неверный формат. Используйте ДД.ММ.ГГГГ")
        return

    if not await UserService.check_energy(user.id):
        await message.answer("⚡️ Недостаточно энергии.")
        return

    status_msg = await message.answer("❤️ <i>Сонастраиваю ваши судьбы...</i>", parse_mode="HTML")
    data = CompatibilityService.calculate_compatibility(user.birth_date, partner_date)
    interpretation = await CompatibilityService.interpret_compatibility(data)
    
    res_text = f"❤️ <b>СОВМЕСТИМОСТЬ</b> ❤️\n"
    res_text += f"Центральная энергия пары: <b>{data['center']}</b>\n\n"
    res_text += f"✨ <b>АНАЛИЗ:</b>\n{interpretation}"
    
    await status_msg.answer(
        res_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await UserService.consume_energy(user.id)
    await state.clear()


@router.callback_query(F.data == "subscription")
async def subscription_handler(callback: CallbackQuery):
    """Обработчик подписки"""
    text = """
💎 <b>Премиум Подписка</b>

Получите доступ к эксклюзивным раскладам и безлимитной энергии!

✨ Безлимитные гадания
✨ Приоритетная поддержка
✨ Доступ к закрытому клубу

Стоимость: 500 ⭐️ / месяц
"""
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Купить за 500 ⭐️", callback_data="buy_subscription")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "three_cards_no_question")
async def three_cards_no_question_handler(callback: CallbackQuery):
    """Обработчик расклада на 3 карты без вопроса"""
    try:
        cards = []
        positions = ["Прошлое", "Настоящее", "Будущее"]
        
        # Получить 3 карты
        for i in range(3):
            card = TarotService.get_random_card()
            cards.append(card)
        
        # Создать интерпретацию
        interpretation = "🛤 <b>РАСКЛАД 'ПУТЬ'</b> 🛤\n\n"
        
        for i, (card, position) in enumerate(zip(cards, positions)):
            interpretation += TarotService.interpret_card(card, position)
            if i < len(cards) - 1:
                interpretation += "\n\n" + "="*30 + "\n\n"
        
        interpretation += "\n\n✨ <b>ОБЩИЙ СОВЕТ:</b>\n"
        interpretation += "Помните: прошлое дало вам опыт, настоящее — возможности, будущее — надежды."
        
        await callback.message.edit_text(
            interpretation,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        
    except Exception as e:
        await callback.answer("Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data.in_({"love_spread_no_question", "sex_spread_no_question"}))
async def love_sex_no_question_handler(callback: CallbackQuery):
    """Обработчик раскладов без вопроса"""
    try:
        spread_type = "love_spread" if "love" in callback.data else "sex_spread"
        cards = []
        
        if spread_type == "love_spread":
            positions = ["Ваши чувства", "Чувства партнера", "Будущее отношений"]
            title = "ОТНОШЕНИЯ"
            emoji = "💖"
        else:
            positions = ["Ваши желания", "Желания партнера", "Сексуальная совместимость"]
            title = "СЕКС И СТРАСТЬ"
            emoji = "🔥"
        
        # Получить 3 карты
        for i in range(3):
            card = TarotService.get_random_card()
            cards.append(card)
        
        # Создать интерпретацию
        interpretation = f"{emoji} <b>РАСКЛАД '{title}'</b> {emoji}\n\n"
        
        for i, (card, position) in enumerate(zip(cards, positions)):
            interpretation += TarotService.interpret_card(card, position)
            if i < len(cards) - 1:
                interpretation += "\n\n" + "="*30 + "\n\n"
        
        interpretation += "\n\n✨ <b>ОБЩИЙ СОВЕТ:</b>\n"
        interpretation += "Любовь - это энергия, которая движет миром."
        
        await callback.message.edit_text(
            interpretation,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        
        # Consume energy
        await UserService.consume_energy(callback.from_user.id)
        
    except Exception as e:
        logger.error(f"Ошибка при создании расклада: {e}")
        await callback.answer("Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data == "arcana_dialogue")
async def arcana_dialogue_handler(callback: CallbackQuery):
    """Обработчик диалога с Арканом"""
    # Выбрать случайный Аркан для диалога
    from bot.tarot_data import MAJOR_ARCANA
    arcana_id = random.choice(list(MAJOR_ARCANA.keys()))
    arcana = MAJOR_ARCANA[arcana_id]
    
    text = f"🎭 <b>Диалог с Арканом: {arcana['name']}</b>\n\n"
    text += f"<i>{arcana['arcana_personality']}</i>\n\n"
    text += "Задайте свой вопрос Аркану, и он ответит вам:"
    
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Случайный совет", callback_data=f"arcana_advice_{arcana_id}")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
        ])
    )


@router.callback_query(F.data.startswith("arcana_advice_"))
async def arcana_advice_handler(callback: CallbackQuery):
    """Обработчик совета от Аркана"""
    arcana_id = int(callback.data.split("_")[-1])
    
    from bot.tarot_data import MAJOR_ARCANA
    import random
    
    user = await UserService.get_or_create_user(callback.from_user.id)

    # Check energy
    if not await UserService.check_energy(user.id):
        return await show_paywall(callback)

    arcana = MAJOR_ARCANA[arcana_id]
    advice = random.choice(arcana['arcana_voice_phrases'])
    
    # Answer with card image
    image_url = arcana.get("image")
    
    caption = f"🎭 <b>{arcana['name']} говорит:</b>\n\n"
    caption += f"💬 {advice}\n\n"
    caption += f"✨ {arcana['upright_short']}"
    
    if image_url:
        await callback.message.answer_photo(
            photo=image_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Еще совет", callback_data=f"arcana_advice_{arcana_id}")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ])
        )
    else:
        await callback.message.answer(
            caption,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Еще совет", callback_data=f"arcana_advice_{arcana_id}")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ])
        )
    
    await UserService.consume_energy(user.id)


@router.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик возврата в главное меню"""
    await state.clear()
    
    welcome_text = """
🌙 <b>ЛИЛИТ - Ваш проводник в мире Таро</b>

Выберите, что вас интересует:
"""
    
    await callback.message.edit_text(welcome_text, reply_markup=get_main_keyboard())


@router.message(StateFilter(TarotStates.waiting_for_question))
async def process_question(message: types.Message, state: FSMContext):
    """Обработчик вопроса пользователя"""
    data = await state.get_data()
    spread_type = data.get('spread_type')
    question = message.text
    
    try:
        if spread_type == "yes_no":
            # Для расклада Да/Нет
            card = TarotService.get_random_card()
            
            # Определить ответ на основе карты
            if card['is_reversed']:
                answer = "❌ <b>НЕТ</b>"
                interpretation = f"Карта {card['name']} в перевернутом положении говорит 'Нет'."
            else:
                answer = "✅ <b>ДА</b>"
                interpretation = f"Карта {card['name']} в прямом положении говорит 'Да'."
            
            full_interpretation = f"🎯 <b>РАСКЛАД 'ДА/НЕТ'</b>\n\n"
            full_interpretation += f"❓ <b>Ваш вопрос:</b> {question}\n\n"
            full_interpretation += f"{answer}\n\n"
            full_interpretation += await TarotService.interpret_card(card, question=question)
            full_interpretation += f"\n\n💭 <b>Интерпретация:</b> {interpretation}"
            
        elif spread_type == "three_cards":
            # Для расклада на 3 карты с вопросом
            cards = []
            positions = ["Прошлое", "Настоящее", "Будущее"]
            
            for i in range(3):
                card = TarotService.get_random_card()
                cards.append(card)
            
            full_interpretation = f"🛤 <b>РАСКЛАД 'ПУТЬ'</b>\n\n"
            full_interpretation += f"❓ <b>Ваш вопрос:</b> {question}\n\n"
            
            for i, (card, position) in enumerate(zip(cards, positions)):
                full_interpretation += await TarotService.interpret_card(card, position, question=question)
                if i < len(cards) - 1:
                    full_interpretation += "\n\n" + "="*30 + "\n\n"
            
            full_interpretation += "\n\n✨ <b>ОБЩИЙ СОВЕТ:</b>\n"
            full_interpretation += "Учитывайте уроки прошлого, действуйте в настоящем, доверяйте будущему."
            
        elif spread_type in ["love_spread", "sex_spread"]:
            # Расклады на отношения и секс
            cards = []
            if spread_type == "love_spread":
                positions = ["Ваши чувства", "Чувства партнера", "Будущее отношений"]
                title = "ОТНОШЕНИЯ"
            else:
                positions = ["Ваши желания", "Желания партнера", "Сексуальная совместимость"]
                title = "СЕКС И СТРАСТЬ"
                
            for i in range(3):
                card = TarotService.get_random_card()
                cards.append(card)
            
            full_interpretation = f"💖 <b>РАСКЛАД '{title}'</b>\n\n"
            full_interpretation += f"❓ <b>Ваш вопрос:</b> {question}\n\n"
            
            for i, (card, position) in enumerate(zip(cards, positions)):
                full_interpretation += await TarotService.interpret_card(card, position, question=question)
                if i < len(cards) - 1:
                    full_interpretation += "\n\n" + "="*30 + "\n\n"
            
            full_interpretation += "\n\n✨ <b>СОВЕТ КАРТ:</b>\n"
            full_interpretation += "Слушайте свое сердце и будьте честны с собой."
        
        await message.answer(
            full_interpretation,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        
        # Consume energy
        await UserService.consume_energy(message.from_user.id)
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка при обработке вопроса: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(StateFilter(TarotStates.waiting_for_birth_date))
async def process_birth_date(message: types.Message, state: FSMContext):
    """Обработчик ввода даты рождения"""
    try:
        # Парсим дату
        birth_date_str = message.text.strip()
        day, month, year = map(int, birth_date_str.split('.'))
        birth_date = date(year, month, day)
        
        # Получаем пользователя
        user = await UserService.get_or_create_user(message.from_user.id)
        
        # Сохраняем дату
        await UserService.update_birth_date(user.id, birth_date)
        
        await message.answer(
            f"✅ <b>Дата рождения {birth_date_str} успешно сохранена!</b>\n\n"
            "Теперь я могу рассчитать вашу Матрицу Судьбы.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⭐️ Рассчитать Матрицу", callback_data="destiny_matrix")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
        await state.clear()
        
    except (ValueError, TypeError):
        await message.answer(
            "❌ <b>Некорректный формат даты.</b>\n\n"
            "Пожалуйста, введите дату в формате ДД.ММ.ГГГГ\n"
            "Например: 15.03.1994",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )


@router.callback_query(F.data == "profile")
async def profile_handler(callback: CallbackQuery):
    """Обработчик профиля пользователя"""
    user = await UserService.get_or_create_user(callback.from_user.id)
    
    profile_text = f"""
👤 <b>Ваш профиль</b>

🆔 ID: {user.telegram_id}
👤 Имя: {user.first_name or 'Не указано'}
📊 Всего раскладов: {user.total_readings}
📅 Дата регистрации: {user.registration_date.strftime('%d.%m.%Y')}
💎 Подписка: {user.subscription_type}
🔢 Раскладов сегодня: {user.daily_readings_count}/{user.daily_readings_limit}
"""
    
    await callback.message.edit_text(
        profile_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📅 Указать дату рождения", callback_data="set_birth_date")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ])
    )


# Импорт random для использования в обработчиках
import random

async def show_paywall(callback: CallbackQuery):
    """Показать сообщение о нехватке энергии"""
    text = """
⚡️ <b>Недостаточно энергии</b>

Ваша энергия исчерпана. Чтобы продолжить гадание, вам нужно восстановить связь с космосом.

Вы можете подождать до завтра (бесплатное восстановление) или приобрести энергию прямо сейчас.
"""
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✨ 5 Энергии (50 ⭐️)", callback_data="buy_energy_5")],
            [InlineKeyboardButton(text="✨ 10 Энергии (90 ⭐️)", callback_data="buy_energy_10")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ])
    )

@router.callback_query(F.data.startswith("buy_energy_"))
async def buy_energy_handler(callback: CallbackQuery):
    """Обработчик покупки энергии"""
    amount = int(callback.data.split("_")[-1])
    price = 50 if amount == 5 else 90
    
    await callback.message.answer_invoice(
        title=f"Пакет {amount} Энергии",
        description=f"Восстановление {amount} единиц энергии для гаданий",
        payload=f"energy_{amount}",
        provider_token="",  # Empty for Telegram Stars
        currency="XTR",
        prices=[types.LabeledPrice(label=f"{amount} Энергии", amount=price)],
        start_parameter="energy-pack"
    )
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    """Обработчик проверки перед оплатой"""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    """Обработчик успешной оплаты"""
    payment_info = message.successful_payment
    payload = payment_info.invoice_payload
    
    if payload.startswith("energy_"):
        amount = int(payload.split("_")[1])
        await UserService.refill_energy(message.from_user.id, amount)
        
        await message.answer(
            f"✨ <b>Оплата прошла успешно!</b>\n\n"
            f"Вам начислено {amount} единиц энергии. Теперь вы можете продолжить гадание.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ])
        )


@router.callback_query(F.data.startswith("tarologists_"))
async def tarologists_handler(callback: CallbackQuery):
    """Обработчик просмотра тарологов"""
    try:
        index = int(callback.data.split("_")[-1])
        
        # Импорт данных (в реальном проекте лучше через сервис/БД)
        from bot.tarologists_data import TAROLOGISTS_DATA
        
        # Циклическая навигация
        if index < 0:
            index = len(TAROLOGISTS_DATA) - 1
        elif index >= len(TAROLOGISTS_DATA):
            index = 0
            
        tarologist = TAROLOGISTS_DATA[index]
        
        text = f"👩‍🔮 <b>{tarologist['name']}</b>\n\n"
        text += f"📝 {tarologist['description']}\n\n"
        text += f"✨ Специализация: {tarologist['specialization']}\n"
        text += f"⏳ Опыт: {tarologist['experience']}\n"
        text += f"⭐️ Рейтинг: {tarologist['rating']} ({tarologist['review_count']} отзывов)\n"
        text += f"💰 Стоимость: {tarologist['price']} ⭐️"
        
        buttons = [
            [
                InlineKeyboardButton(text="⬅️", callback_data=f"tarologists_{index-1}"),
                InlineKeyboardButton(text="➡️", callback_data=f"tarologists_{index+1}")
            ],
            [InlineKeyboardButton(text="💬 Отзывы", callback_data=f"reviews_{index}")],
            [InlineKeyboardButton(text="📝 Обратиться", callback_data=f"contact_tarologist_{index}")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]
        
        # Если есть фото, отправляем/обновляем фото
        if tarologist.get('photo_url'):
            # В реальном боте лучше использовать InputMediaPhoto для обновления
            # Но для простоты здесь удалим старое и пришлем новое, если это не первое сообщение
            # Или просто отправим новое сообщение
            
            # Попробуем отредактировать медиа, если это возможно
            try:
                await callback.message.edit_media(
                    media=types.InputMediaPhoto(
                        media=tarologist['photo_url'],
                        caption=text,
                        parse_mode="HTML"
                    ),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
                )
            except Exception:
                # Если нельзя отредактировать (например, было текстовое сообщение), удаляем и шлем новое
                await callback.message.delete()
                await callback.message.answer_photo(
                    photo=tarologist['photo_url'],
                    caption=text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
                    parse_mode="HTML"
                )
        else:
            await callback.message.edit_text(
                text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
                parse_mode="HTML"
            )
            
    except Exception as e:
        logger.error(f"Ошибка при просмотре тарологов: {e}")
        await callback.answer("Ошибка загрузки профиля")


@router.callback_query(F.data.startswith("reviews_"))
async def reviews_handler(callback: CallbackQuery):
    """Обработчик просмотра отзывов"""
    index = int(callback.data.split("_")[-1])
    from bot.tarologists_data import TAROLOGISTS_DATA
    tarologist = TAROLOGISTS_DATA[index]
    
    # Фейковые отзывы для демонстрации
    reviews = [
        "Очень помогла разобраться в себе! Спасибо!",
        "Все четко и по делу. Рекомендую.",
        "Сначала сомневалась, но результат удивил.",
        "Приятная в общении, дала дельные советы."
    ]
    
    text = f"💬 <b>Отзывы о {tarologist['name']}</b>\n\n"
    for review in random.sample(reviews, 3):
        text += f"👤 <i>Пользователь</i>: {review}\n\n"
        
    await callback.message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Оставить отзыв", callback_data=f"leave_review_{index}")],
            [InlineKeyboardButton(text="🔙 К анкете", callback_data=f"tarologists_{index}")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("contact_tarologist_"))
async def contact_tarologist_handler(callback: CallbackQuery):
    """Обработчик обращения к тарологу"""
    index = int(callback.data.split("_")[-1])
    from bot.tarologists_data import TAROLOGISTS_DATA
    tarologist = TAROLOGISTS_DATA[index]
    
    text = f"📝 <b>Обращение к {tarologist['name']}</b>\n\n"
    text += "Опишите вашу ситуацию и вопрос. Таролог ответит вам в течение 24 часов.\n\n"
    text += f"Стоимость консультации: {tarologist['price']} ⭐️"
    
    await callback.message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"Оплатить {tarologist['price']} ⭐️", callback_data=f"pay_consultation_{index}")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"tarologists_{index}")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer() 


# ===== AI Consultant Handlers =====

@router.callback_query(F.data == "consultant")
async def consultant_handler(callback: CallbackQuery, state: FSMContext):
    """Start AI consultant conversation"""
    await callback.message.edit_text(
        "💬 <b>Консультант 24/7</b>\n\n"
        "🔮 Я — Лилит, ваш личный консультант по Таро.\n\n"
        "Задавайте любые вопросы о картах, раскладах, значениях. "
        "Я помню контекст нашей беседы!\n\n"
        "💡 <i>Напишите ваш вопрос...</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clear_consultant")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(TarotStates.consulting)


@router.callback_query(F.data == "clear_consultant")
async def clear_consultant_handler(callback: CallbackQuery):
    """Clear consultant conversation history"""
    ConsultantAI.clear_history(callback.from_user.id)
    await callback.answer("✅ История беседы очищена", show_alert=True)


@router.message(StateFilter(TarotStates.consulting))
async def consultant_message_handler(message: types.Message, state: FSMContext):
    """Handle messages in consultant mode"""
    try:
        # Show typing indicator
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Get AI response
        response = await ConsultantAI.chat(message.from_user.id, message.text)
        
        # Send response
        await message.answer(
            f"🔮 <b>Лилит:</b>\n\n{response}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clear_consultant")],
                [InlineKeyboardButton(text="🏠 Выйти из чата", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error in consultant: {e}")
        await message.answer(
            "😔 Произошла ошибка. Попробуйте еще раз или вернитесь в главное меню.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
            ])
        )
 
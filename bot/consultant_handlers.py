"""
Consultant handlers - add to handlers.py
"""

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

"""
Обработчики для системы подписок
"""

import logging
from aiogram import types, F, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram_bot.subscription_service import SubscriptionService
from payment_systems.robokassa import PaymentService

logger = logging.getLogger(__name__)

# Router для обработчиков подписок
subscription_router = Router()


def get_subscription_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора подписки"""
    buttons = [
        [InlineKeyboardButton(text="🆓 FREE", callback_data="subscription_free")],
        [InlineKeyboardButton(text="💎 PREMIUM - 2,500₸/мес", callback_data="subscription_premium")],
        [InlineKeyboardButton(text="🌟 VIP - 15,000₸/консультация", callback_data="subscription_vip")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_payment_keyboard(plan_type: str) -> InlineKeyboardMarkup:
    """Клавиатура для выбора способа оплаты"""
    buttons = [
        [InlineKeyboardButton(text="💳 Robokassa", callback_data=f"payment_robokassa_{plan_type}")],
        [InlineKeyboardButton(text="⭐ Telegram Stars", callback_data=f"payment_stars_{plan_type}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="subscription_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@subscription_router.callback_query(F.data == "subscription")
async def subscription_menu_handler(callback: CallbackQuery):
    """Обработчик меню подписок"""
    user_id = callback.from_user.id
    
    # Получить информацию о текущей подписке
    subscription_info = await SubscriptionService.get_user_subscription(user_id)
    
    if "error" in subscription_info:
        await callback.answer("Ошибка при получении информации о подписке")
        return
    
    # Создать текст с информацией о подписке
    text = f"""
💎 **Ваша подписка**

**Текущий план:** {subscription_info['plan_name']} ({subscription_info['plan_name_kz']})
**Запросов сегодня:** {subscription_info['daily_requests']}/{subscription_info['daily_limit'] if subscription_info['daily_limit'] != -1 else '∞'}
**Всего запросов:** {subscription_info['total_requests']}

**Доступные тарифы:**
"""
    
    # Добавить информацию о тарифах
    for plan_type, plan_info in SubscriptionService.SUBSCRIPTION_PLANS.items():
        text += f"\n**{plan_info['name']}** - {plan_info['price']}₸/мес"
        if plan_type == subscription_info['plan_type']:
            text += " ✅"
        text += f"\n• {', '.join(plan_info['features'])}\n"
    
    await callback.message.edit_text(text, reply_markup=get_subscription_keyboard())


@subscription_router.callback_query(F.data == "subscription_free")
async def subscription_free_handler(callback: CallbackQuery):
    """Обработчик выбора FREE подписки"""
    user_id = callback.from_user.id
    
    # FREE подписка уже активна по умолчанию
    subscription_info = await SubscriptionService.get_user_subscription(user_id)
    
    if subscription_info['plan_type'] == 'free':
        await callback.answer("У вас уже активна FREE подписка!")
        return
    
    # Переключить на FREE
    result = await SubscriptionService.cancel_subscription(user_id)
    
    if "error" in result:
        await callback.answer("Ошибка при переключении на FREE подписку")
        return
    
    await callback.answer("Переключено на FREE подписку!")
    await subscription_menu_handler(callback)


@subscription_router.callback_query(F.data == "subscription_premium")
async def subscription_premium_handler(callback: CallbackQuery):
    """Обработчик выбора PREMIUM подписки"""
    user_id = callback.from_user.id
    
    # Проверить текущую подписку
    subscription_info = await SubscriptionService.get_user_subscription(user_id)
    
    if subscription_info['plan_type'] == 'premium':
        await callback.answer("У вас уже активна PREMIUM подписка!")
        return
    
    # Показать способы оплаты
    text = """
💎 **PREMIUM подписка - 2,500₸/мес**

**Включает:**
• Безлимит запросов
• Все функции платформы
• PDF-отчёты
• Приоритетная поддержка

**Выберите способ оплаты:**
"""
    
    await callback.message.edit_text(text, reply_markup=get_payment_keyboard("premium"))


@subscription_router.callback_query(F.data == "subscription_vip")
async def subscription_vip_handler(callback: CallbackQuery):
    """Обработчик выбора VIP подписки"""
    user_id = callback.from_user.id
    
    # Проверить текущую подписку
    subscription_info = await SubscriptionService.get_user_subscription(user_id)
    
    if subscription_info['plan_type'] == 'vip':
        await callback.answer("У вас уже активна VIP подписка!")
        return
    
    # Показать способы оплаты
    text = """
🌟 **VIP консультация - 15,000₸**

**Включает:**
• Живая консультация с тарологом
• Персональный прогноз
• Доступ к закрытому комьюнити
• Эксклюзивные материалы

**Выберите способ оплаты:**
"""
    
    await callback.message.edit_text(text, reply_markup=get_payment_keyboard("vip"))


@subscription_router.callback_query(F.data.startswith("payment_robokassa_"))
async def payment_robokassa_handler(callback: CallbackQuery):
    """Обработчик оплаты через Robokassa"""
    user_id = callback.from_user.id
    plan_type = callback.data.split("_")[2]
    
    # Создать платеж
    payment_service = PaymentService()
    
    if plan_type == "vip":
        result = await payment_service.create_consultation_payment(user_id, "robokassa")
    else:
        result = await payment_service.create_subscription_payment(user_id, plan_type, "robokassa")
    
    if "error" in result:
        await callback.answer("Ошибка при создании платежа")
        return
    
    # Отправить ссылку на оплату
    text = f"""
💳 **Оплата через Robokassa**

**Сумма:** {result['amount']}₸
**Описание:** {result['description']}

Нажмите на кнопку ниже для перехода к оплате:
"""
    
    buttons = [
        [InlineKeyboardButton(text="💳 Оплатить", url=result['payment_url'])],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="subscription_menu")]
    ]
    
    await callback.message.edit_text(
        text, 
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@subscription_router.callback_query(F.data.startswith("payment_stars_"))
async def payment_stars_handler(callback: CallbackQuery):
    """Обработчик оплаты через Telegram Stars"""
    user_id = callback.from_user.id
    plan_type = callback.data.split("_")[2]
    
    # Создать платеж
    payment_service = PaymentService()
    
    if plan_type == "vip":
        result = await payment_service.create_consultation_payment(user_id, "telegram_stars")
    else:
        result = await payment_service.create_subscription_payment(user_id, plan_type, "telegram_stars")
    
    if "error" in result:
        await callback.answer("Ошибка при создании платежа")
        return
    
    # Отправить информацию о платеже
    text = f"""
⭐ **Оплата через Telegram Stars**

**Сумма:** {result['amount']}₸
**Описание:** {result['description']}
**ID платежа:** {result['payment_id']}

Платеж создан! Ожидайте подтверждения.
"""
    
    buttons = [
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ]
    
    await callback.message.edit_text(
        text, 
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@subscription_router.callback_query(F.data == "subscription_menu")
async def subscription_menu_back_handler(callback: CallbackQuery):
    """Возврат в меню подписок"""
    await subscription_menu_handler(callback)


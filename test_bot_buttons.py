"""
Автоматический тестер всех кнопок бота
"""
from telethon import TelegramClient
from telethon.tl.functions.messages import StartBotRequest
import asyncio

api_id = 26958540
api_hash = "fac9df28263703149d3654c415b0dd66"
bot_username = "lilit_tarologue_bot"

async def test_all_buttons():
    """Тестируем все кнопки бота"""
    client = TelegramClient('test_session', api_id, api_hash)
    await client.start()
    
    print("✅ Подключились к Telegram")
    
    # Найти бота
    bot = await client.get_entity(bot_username)
    print(f"✅ Нашли бота: {bot.username}")
    
    # Отправить /start
    await client.send_message(bot, '/start')
    await asyncio.sleep(2)
    
    # Получить последнее сообщение
    messages = await client.get_messages(bot, limit=1)
    last_msg = messages[0]
    
    print(f"\n📩 Ответ на /start получен: {len(last_msg.text)} символов")
    
    if last_msg.reply_markup:
        buttons = []
        for row in last_msg.reply_markup.rows:
            for button in row.buttons:
                buttons.append(button.text)
        
        print(f"\n🔘 Найдено кнопок: {len(buttons)}")
        print("Список кнопок:")
        for i, btn in enumerate(buttons, 1):
            print(f"  {i}. {btn}")
        
        # Тестируем каждую кнопку
        print("\n🧪 Начинаем тестирование кнопок...\n")
        
        for i, button_row in enumerate(last_msg.reply_markup.rows):
            for button in button_row.buttons:
                btn_text = button.text
                print(f"⏳ Тестирую: {btn_text}")
                
                try:
                    # Нажать кнопку
                    await last_msg.click(data=button.data)
                    await asyncio.sleep(2)
                    
                    # Проверить ответ
                    new_messages = await client.get_messages(bot, limit=1)
                    response = new_messages[0]
                    
                    if response.id != last_msg.id:
                        print(f"  ✅ {btn_text}: РАБОТАЕТ (получен ответ)")
                    else:
                        print(f"  ❌ {btn_text}: НЕТ ОТВЕТА")
                    
                    # Вернуться в главное меню
                    if response.reply_markup:
                        for row in response.reply_markup.rows:
                            for btn in row.buttons:
                                if "меню" in btn.text.lower() or "menu" in btn.text.lower():
                                    await response.click(data=btn.data)
                                    await asyncio.sleep(1)
                                    break
                    
                except Exception as e:
                    print(f"  ❌ {btn_text}: ОШИБКА - {str(e)[:50]}")
                
                await asyncio.sleep(1)
        
        print("\n✅ Тестирование завершено!")
    else:
        print("❌ Нет кнопок в ответе!")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_all_buttons())

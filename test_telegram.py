import asyncio
import os
import config
from telegram import Bot

async def test_telegram_connection():
    """Тестирует подключение к Telegram и каналу"""
    print("🔍 Тестирование подключения к Telegram...")
    print("=" * 50)
    
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не установлен")
        return False
    
    if not CHANNEL_ID:
        print("❌ TELEGRAM_CHANNEL_ID не установлен")
        return False
    
    print(f"🔑 Токен бота: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")
    print(f"📢 ID канала: {CHANNEL_ID}")
    
    try:
        bot = Bot(token=BOT_TOKEN)
        
        # Тест 1: Проверка бота
        print("\n🤖 Тест 1: Проверка бота...")
        me = await bot.get_me()
        print(f"✅ Бот подключен: @{me.username} ({me.first_name})")
        
        # Тест 2: Проверка канала
        print(f"\n📢 Тест 2: Проверка доступа к каналу {CHANNEL_ID}...")
        try:
            chat = await bot.get_chat(CHANNEL_ID)
            print(f"✅ Канал найден: {chat.title}")
            print(f"📊 Тип: {chat.type}")
            if hasattr(chat, 'username') and chat.username:
                print(f"🔗 Username: @{chat.username}")
        except Exception as e:
            print(f"❌ Ошибка доступа к каналу: {e}")
            print("\n🔧 Возможные решения:")
            print("1. Проверьте правильность TELEGRAM_CHANNEL_ID")
            print("2. Убедитесь что бот добавлен в канал")
            print("3. Дайте боту права администратора")
            print("4. Для приватных каналов используйте числовой ID (начинается с -100)")
            return False
        
        # Тест 3: Отправка тестового сообщения
        print(f"\n📤 Тест 3: Отправка тестового сообщения...")
        try:
            test_message = f"🧪 **ТЕСТ ПОДКЛЮЧЕНИЯ**\n\n✅ Бот работает корректно!\n🕐 Время: {asyncio.get_event_loop().time()}"
            result = await bot.send_message(
                chat_id=CHANNEL_ID,
                text=test_message,
                parse_mode='Markdown'
            )
            print(f"✅ Сообщение отправлено! ID: {result.message_id}")
            
        except Exception as e:
            print(f"❌ Ошибка отправки сообщения: {e}")
            print("\n🔧 Проверьте права бота в канале:")
            print("- Бот должен быть администратором")
            print("- Должно быть право 'Отправка сообщений'")
            return False
        
        print(f"\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("✅ Telegram бот настроен правильно")
        return True
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        return False

async def suggest_channel_id_format():
    """Подсказывает правильный формат ID канала"""
    print("\n💡 ПОДСКАЗКИ ПО НАСТРОЙКЕ CHANNEL_ID:")
    print("=" * 50)
    print("📋 Для публичных каналов:")
    print("   @your_channel_name")
    print("   Пример: @sportspredictions")
    print()
    print("📋 Для приватных каналов:")
    print("   -1001234567890 (числовой ID)")
    print("   Получить можно через @userinfobot")
    print()
    print("📋 Как получить ID приватного канала:")
    print("   1. Добавьте @userinfobot в канал")
    print("   2. Отправьте любое сообщение")
    print("   3. Бот покажет ID канала")
    print("   4. Удалите @userinfobot из канала")

if __name__ == "__main__":
    asyncio.run(test_telegram_connection())
    asyncio.run(suggest_channel_id_format())

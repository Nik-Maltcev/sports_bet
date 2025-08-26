import asyncio
import sys
import os
import config
from sports_bot import TelegramSportsBot

async def test_bot():
    """Тестирует работу бота"""
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ Ошибка: Не установлены переменные окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID")
        print("Отредактируйте файл .env и укажите ваши данные")
        return
    
    print("🤖 Создание экземпляра бота...")
    sports_bot = TelegramSportsBot(BOT_TOKEN, CHANNEL_ID)
    
    try:
        print("📊 Генерация тестовых прогнозов...")
        await sports_bot.test_send()
        print("✅ Тестовые прогнозы отправлены успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        print("\nВозможные причины:")
        print("1. Неверный токен бота")
        print("2. Неверный ID канала")
        print("3. Бот не является администратором канала")
        print("4. Отсутствует подключение к интернету")

if __name__ == "__main__":
    print("🔧 Запуск тестирования Telegram бота...")
    print("=" * 50)
    asyncio.run(test_bot())

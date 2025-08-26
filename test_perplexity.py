import asyncio
import os
import sys
import config
from perplexity_analyzer import EnhancedSportsAnalyzer

async def test_perplexity():
    """Тестирует интеграцию с Perplexity API"""
    print("🔬 Тестирование Perplexity API интеграции...")
    print("=" * 50)
    
    perplexity_key = os.getenv('PERPLEXITY_API_KEY')
    
    if not perplexity_key:
        print("❌ PERPLEXITY_API_KEY не установлен")
        print("Добавьте ключ в файл .env:")
        print("PERPLEXITY_API_KEY=pplx-ваш-ключ")
        print("\nПолучить ключ можно на: https://perplexity.ai/account/api")
        return False
    
    print(f"🔑 API ключ найден: {perplexity_key[:10]}...")
    
    try:
        analyzer = EnhancedSportsAnalyzer(perplexity_key)
        
        print("\n🏈 Тестирование получения футбольных данных...")
        football_prediction = await analyzer.generate_real_prediction("football")
        
        if football_prediction:
            print("✅ Футбольный прогноз получен!")
            print(f"⚽ Матч: {football_prediction['match']}")
            print(f"🏆 Лига: {football_prediction['league']}")
            print(f"📈 Прогноз: {football_prediction['prediction']}")
            print(f"💰 Коэффициент: {football_prediction['odds']}")
            print(f"🎯 Уверенность: {football_prediction['confidence']}%")
            print(f"📊 Источник: {football_prediction['source']}")
        else:
            print("❌ Не удалось получить футбольный прогноз")
        
        print("\n🏀 Тестирование получения баскетбольных данных...")
        basketball_prediction = await analyzer.generate_real_prediction("basketball")
        
        if basketball_prediction:
            print("✅ Баскетбольный прогноз получен!")
            print(f"🏀 Матч: {basketball_prediction['match']}")
            print(f"🏆 Лига: {basketball_prediction['league']}")
        else:
            print("❌ Не удалось получить баскетбольный прогноз")
        
        await analyzer.close()
        
        print("\n✅ Тестирование завершено успешно!")
        print("🚀 Perplexity API работает корректно")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        print("\nВозможные причины:")
        print("1. Неверный API ключ")
        print("2. Превышен лимит запросов")
        print("3. Проблемы с подключением к интернету")
        print("4. Проблемы с Perplexity API")
        return False

async def test_full_bot_integration():
    """Тестирует полную интеграцию бота с Perplexity"""
    print("\n🤖 Тестирование полной интеграции бота...")
    print("=" * 50)
    
    from main_bot import HybridSportsBot
    
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID') 
    PERPLEXITY_KEY = os.getenv('PERPLEXITY_API_KEY')
    
    if not all([BOT_TOKEN, CHANNEL_ID]):
        print("❌ Не все переменные окружения настроены")
        print("Необходимы: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID")
        return False
    
    try:
        bot = HybridSportsBot(BOT_TOKEN, CHANNEL_ID, PERPLEXITY_KEY)
        
        print("📊 Генерация прогнозов с Perplexity...")
        predictions = await bot.generate_hybrid_predictions(2)
        
        print(f"✅ Сгенерировано {len(predictions)} прогнозов")
        
        for i, pred in enumerate(predictions, 1):
            print(f"\n🏆 Прогноз #{i}:")
            print(f"   Спорт: {pred.sport}")
            print(f"   Матч: {pred.match}")
            print(f"   Уверенность: {pred.confidence}%")
        
        await bot.cleanup()
        
        print("\n✅ Интеграция работает!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка интеграции: {e}")
        return False

async def main():
    """Основная функция тестирования"""
    print("🧪 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ SPORTS PREDICTION BOT")
    print("=" * 60)
    
    # Тест 1: Perplexity API
    perplexity_ok = await test_perplexity()
    
    if perplexity_ok:
        # Тест 2: Полная интеграция
        integration_ok = await test_full_bot_integration()
        
        if integration_ok:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            print("🚀 Бот готов к развертыванию на Railway")
        else:
            print("\n⚠️ Частичный успех - Perplexity работает, но есть проблемы с интеграцией")
    else:
        print("\n❌ Тесты не пройдены")
        print("Проверьте настройки и попробуйте снова")

if __name__ == "__main__":
    asyncio.run(main())

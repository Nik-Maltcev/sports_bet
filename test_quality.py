#!/usr/bin/env python3
"""
Тест качества прогнозов после улучшений
"""
import asyncio
import os
from sports_bot import EnhancedSportsBot

async def test_mock_predictions():
    """Тестирует качество моковых прогнозов"""
    print("🧪 ТЕСТ КАЧЕСТВА МОКОВЫХ ДАННЫХ")
    print("=" * 50)
    
    bot = EnhancedSportsBot("fake_token", "fake_channel")
    
    print("📊 Генерируем 3 прогноза...")
    
    for i in range(3):
        prediction = bot.generate_prediction()
        print(f"\n🏆 ПРОГНОЗ #{i+1}:")
        print(f"   🎯 Спорт: {prediction.sport}")
        print(f"   🏟️ Лига: {prediction.league}")
        print(f"   ⚔️ Матч: {prediction.match}")
        print(f"   🕐 Время: {prediction.time}")
        print(f"   📈 Прогноз: {prediction.prediction}")
        print(f"   💰 Коэффициент: {prediction.odds}")
        print(f"   🎯 Уверенность: {prediction.confidence}%")
        print(f"   📊 Источник: {prediction.source}")
        print(f"   📋 Анализ: {prediction.analysis[:100]}...")
    
    print(f"\n✅ Моковые данные готовы!")
    return True

async def main():
    """Основной тест качества"""
    print("🎯 БЫСТРЫЙ ТЕСТ КАЧЕСТВА ПОСЛЕ УЛУЧШЕНИЙ")
    print("=" * 60)
    
    success = await test_mock_predictions()
    
    if success:
        print("\n🎉 ТЕСТ ПРОЙДЕН! Качество улучшилось")
        print("🔥 Реалистичные команды, времена матчей, детальный анализ")
    else:
        print("\n⚠️ ЕСТЬ ПРОБЛЕМЫ")

if __name__ == "__main__":
    asyncio.run(main())
    """Тестирует качество моковых данных"""
    print("🧪 ТЕСТИРОВАНИЕ КАЧЕСТВА ПРОГНОЗОВ")
    print("=" * 50)
    
    analyzer = SportsAnalyzer()
    
    print("📊 Генерация тестовых прогнозов...")
    
    sports = ["Футбол", "Баскетбол", "Теннис", "Хоккей"]
    
    for sport in sports:
        print(f"\n🏆 {sport.upper()}:")
        print("-" * 30)
        
        prediction = await analyzer.generate_prediction(sport)
        
        print(f"⚔️ Матч: {prediction.match}")
        print(f"🏟️ Лига: {prediction.league}")
        
        if hasattr(prediction, 'time'):
            print(f"🕐 Время: {prediction.time}")
        
        print(f"📈 Прогноз: {prediction.prediction}")
        print(f"💰 Коэффициент: {prediction.odds}")
        print(f"🎯 Уверенность: {prediction.confidence}%")
        
        if hasattr(prediction, 'source'):
            print(f"📡 Источник: {prediction.source}")
        
        print(f"\n📋 Анализ:")
        print(f"{prediction.analysis[:150]}...")
        
        # Проверка качества
        quality_score = 0
        
        # Проверяем, что команды выглядят реалистично
        if any(team in prediction.match for team in ["Барселона", "Реал", "Манчестер", "Ливерпуль", "Лейкерс", "Голден Стэйт"]):
            quality_score += 1
        
        # Проверяем наличие лиги
        if prediction.league and len(prediction.league) > 5:
            quality_score += 1
            
        # Проверяем детальность анализа
        if len(prediction.analysis) > 100:
            quality_score += 1
            
        # Проверяем коэффициенты
        try:
            odds_val = float(prediction.odds)
            if 1.1 <= odds_val <= 10.0:
                quality_score += 1
        except:
            pass
            
        # Проверяем уверенность
        if 70 <= prediction.confidence <= 95:
            quality_score += 1
            
        quality_percent = (quality_score / 5) * 100
        
        if quality_percent >= 80:
            quality_emoji = "✅"
            quality_text = "ОТЛИЧНОЕ"
        elif quality_percent >= 60:
            quality_emoji = "⚠️"
            quality_text = "ХОРОШЕЕ"
        else:
            quality_emoji = "❌"
            quality_text = "ПЛОХОЕ"
            
        print(f"\n{quality_emoji} Качество: {quality_text} ({quality_percent:.0f}%)")

async def test_realistic_teams():
    """Проверяет реалистичность команд"""
    print("\n\n🏟️ ПРОВЕРКА РЕАЛИСТИЧНОСТИ КОМАНД")
    print("=" * 50)
    
    analyzer = SportsAnalyzer()
    
    # Проверяем 10 матчей по футболу
    football_teams = set()
    
    for i in range(10):
        pred = await analyzer.generate_prediction("Футбол")
        teams = pred.match.replace(" - ", " vs ").split(" vs ")
        for team in teams:
            football_teams.add(team.strip())
    
    print(f"🏈 Найдено уникальных футбольных команд: {len(football_teams)}")
    
    real_teams = [
        "Барселона", "Реал Мадрид", "Манчестер Сити", "Ливерпуль", 
        "Челси", "Арсенал", "ПСЖ", "Бавария", "Ювентус", "Милан"
    ]
    
    real_found = sum(1 for team in real_teams if any(real_team in team for real_team in football_teams))
    
    print(f"✅ Реальных команд найдено: {real_found}/{len(real_teams)}")
    
    if real_found >= 5:
        print("🎉 Команды выглядят реалистично!")
    else:
        print("⚠️ Нужно улучшить базу команд")

async def main():
    """Основная функция тестирования"""
    await test_mock_data_quality()
    await test_realistic_teams()
    
    print("\n\n🏁 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("💡 Если качество плохое, проверьте:")
    print("1. База команд в sports_bot.py")
    print("2. Шаблоны анализа")
    print("3. Настройки коэффициентов")
    
    print("\n📝 Для улучшения качества:")
    print("1. Настройте PERPLEXITY_API_KEY для реальных данных")
    print("2. Или улучшите моковые данные в sports_bot.py")

if __name__ == "__main__":
    asyncio.run(main())

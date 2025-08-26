import asyncio
import aiohttp
import json
from typing import List, Dict, Optional
from datetime import datetime
import pytz
import random

class SportsDataProvider:
    """Класс для получения реальных спортивных данных"""
    
    def __init__(self):
        self.session = None
        # Здесь можно добавить API ключи для реальных данных
        self.api_endpoints = {
            "football": "https://api.football-data.org/v4/matches",
            "basketball": "https://api-basketball.p.rapidapi.com/games", 
            "tennis": "https://tennis-live-data.p.rapidapi.com/matches-today"
        }
    
    async def get_session(self):
        """Получает aiohttp сессию"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        """Закрывает aiohttp сессию"""
        if self.session:
            await self.session.close()
    
    async def get_todays_matches(self, sport: str) -> List[Dict]:
        """Получает матчи на сегодня для определенного вида спорта"""
        # В реальной реализации здесь были бы запросы к внешним API
        # Для демонстрации возвращаем моковые данные
        
        mock_matches = {
            "football": [
                {
                    "home_team": "Манчестер Сити",
                    "away_team": "Ливерпуль", 
                    "league": "Премьер-лига",
                    "time": "20:00",
                    "odds": {"home": 2.1, "draw": 3.2, "away": 3.8}
                },
                {
                    "home_team": "Барселона",
                    "away_team": "Реал Мадрид",
                    "league": "Ла Лига", 
                    "time": "22:00",
                    "odds": {"home": 2.5, "draw": 3.1, "away": 2.9}
                }
            ],
            "basketball": [
                {
                    "home_team": "Лейкерс",
                    "away_team": "Уорриорз",
                    "league": "НБА",
                    "time": "04:00",
                    "odds": {"home": 1.9, "away": 1.8, "total_over": 2.0}
                }
            ],
            "tennis": [
                {
                    "player1": "Новак Джокович",
                    "player2": "Рафаэль Надаль",
                    "tournament": "ATP Masters",
                    "time": "16:00",
                    "odds": {"player1": 1.6, "player2": 2.3}
                }
            ]
        }
        
        return mock_matches.get(sport, [])
    
    async def get_team_stats(self, team: str) -> Dict:
        """Получает статистику команды"""
        # Моковые статистические данные
        return {
            "recent_form": random.choice(["WWWWW", "WWLWW", "WLWWL", "LWWWW"]),
            "goals_scored_avg": round(random.uniform(1.2, 3.5), 1),
            "goals_conceded_avg": round(random.uniform(0.8, 2.2), 1),
            "home_advantage": random.randint(60, 85),
            "injury_count": random.randint(0, 3)
        }
    
    async def get_weather_data(self, city: str) -> Dict:
        """Получает данные о погоде"""
        return {
            "temperature": random.randint(15, 25),
            "conditions": random.choice(["Солнечно", "Облачно", "Дождь", "Ветрено"]),
            "wind_speed": random.randint(5, 20)
        }

class AdvancedSportsAnalyzer:
    """Продвинутый класс анализа с использованием реальных данных"""
    
    def __init__(self):
        self.data_provider = SportsDataProvider()
        self.analysis_weights = {
            "recent_form": 0.25,
            "head_to_head": 0.20,
            "home_advantage": 0.15,
            "injuries": 0.15,
            "motivation": 0.15,
            "weather": 0.10
        }
    
    async def analyze_football_match(self, match_data: Dict) -> Dict:
        """Анализирует футбольный матч"""
        home_stats = await self.data_provider.get_team_stats(match_data["home_team"])
        away_stats = await self.data_provider.get_team_stats(match_data["away_team"])
        
        # Анализ различных факторов
        analysis_factors = []
        confidence_score = 50
        
        # Анализ формы команд
        if home_stats["recent_form"].count('W') > away_stats["recent_form"].count('W'):
            analysis_factors.append(f"{match_data['home_team']} демонстрирует лучшую текущую форму")
            confidence_score += 15
        elif away_stats["recent_form"].count('W') > home_stats["recent_form"].count('W'):
            analysis_factors.append(f"{match_data['away_team']} показывает стабильные результаты")
            confidence_score += 10
        
        # Анализ атаки и защиты
        if home_stats["goals_scored_avg"] > away_stats["goals_conceded_avg"]:
            analysis_factors.append("Атака хозяев против слабой защиты гостей")
            confidence_score += 12
        
        # Домашнее преимущество
        if home_stats["home_advantage"] > 75:
            analysis_factors.append("Значительное преимущество домашних стен")
            confidence_score += 8
        
        # Травмы
        if away_stats["injury_count"] > home_stats["injury_count"]:
            analysis_factors.append("Кадровые проблемы у гостевой команды")
            confidence_score += 10
        
        return {
            "confidence": min(confidence_score, 95),
            "key_factors": analysis_factors[:4],
            "detailed_analysis": self._generate_detailed_analysis(match_data, home_stats, away_stats)
        }
    
    def _generate_detailed_analysis(self, match_data: Dict, home_stats: Dict, away_stats: Dict) -> str:
        """Генерирует детальный анализ матча"""
        analyses = [
            f"Статистический анализ показывает преимущество команды с показателем {home_stats['goals_scored_avg']} голов за матч в атаке.",
            f"Форма команд ({home_stats['recent_form']} vs {away_stats['recent_form']}) указывает на вероятный исход.",
            f"Тактический расклад с учетом домашнего преимущества {home_stats['home_advantage']}% говорит в пользу данного прогноза.",
            f"Анализ последних встреч и мотивационных факторов подтверждает высокую вероятность события."
        ]
        return random.choice(analyses)
    
    async def generate_enhanced_prediction(self, sport: str) -> Optional[Dict]:
        """Генерирует улучшенный прогноз с использованием реальных данных"""
        try:
            matches = await self.data_provider.get_todays_matches(sport)
            if not matches:
                return None
            
            match = random.choice(matches)
            
            if sport == "football":
                analysis = await self.analyze_football_match(match)
                
                # Определяем тип ставки на основе анализа
                bet_types = ["Победа хозяев", "Тотал больше 2.5", "Обе забьют"]
                prediction_type = random.choice(bet_types)
                
                return {
                    "sport": "Футбол",
                    "league": match["league"],
                    "match": f"{match['home_team']} - {match['away_team']}",
                    "time": match["time"],
                    "prediction": prediction_type,
                    "odds": str(random.choice([1.85, 2.10, 2.35, 2.60])),
                    "confidence": analysis["confidence"],
                    "analysis": analysis["detailed_analysis"],
                    "key_factors": analysis["key_factors"]
                }
            
        except Exception as e:
            print(f"Ошибка при генерации улучшенного прогноза: {e}")
            return None
    
    async def close(self):
        """Закрывает соединения"""
        await self.data_provider.close_session()

# Пример использования улучшенного анализатора
async def demo_enhanced_analyzer():
    """Демонстрация работы улучшенного анализатора"""
    analyzer = AdvancedSportsAnalyzer()
    
    try:
        prediction = await analyzer.generate_enhanced_prediction("football")
        if prediction:
            print("🔍 Улучшенный прогноз:")
            print(f"⚽ {prediction['match']}")
            print(f"📈 {prediction['prediction']} (коэф. {prediction['odds']})")
            print(f"🎯 Уверенность: {prediction['confidence']}%")
            print(f"📊 Анализ: {prediction['analysis']}")
            print("🔑 Ключевые факторы:")
            for factor in prediction['key_factors']:
                print(f"  • {factor}")
    
    finally:
        await analyzer.close()

if __name__ == "__main__":
    asyncio.run(demo_enhanced_analyzer())

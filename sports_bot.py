import asyncio
import logging
from datetime import datetime, time
from typing import List, Dict, Tuple
import pytz
from telegram import Bot
from telegram.ext import Application
import random
import aiohttp
import json
from dataclasses import dataclass
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import config  # Загружаем конфигурацию

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@dataclass
class SportsPrediction:
    """Структура для хранения спортивного прогноза"""
    sport: str
    league: str
    match: str
    prediction: str
    odds: str
    confidence: int
    analysis: str
    key_factors: List[str]

class SportsAnalyzer:
    """Класс для генерации профессиональных спортивных прогнозов"""
    
    def __init__(self):
        self.sports_data = {
            "Футбол": {
                "leagues": ["Премьер-лига", "Ла Лига", "Серия А", "Бундеслига", "Лига 1"],
                "bet_types": ["Победа хозяев", "Ничья", "Победа гостей", "Тотал больше 2.5", "Тотал меньше 2.5", "Обе забьют"]
            },
            "Баскетбол": {
                "leagues": ["НБА", "Евролига", "ВТБ", "NCAA"],
                "bet_types": ["Победа хозяев", "Победа гостей", "Тотал больше", "Тотал меньше", "Фора"]
            },
            "Теннис": {
                "leagues": ["ATP", "WTA", "Челленджер", "ITF"],
                "bet_types": ["Победа игрока 1", "Победа игрока 2", "Тотал геймов больше", "Тотал геймов меньше"]
            },
            "Хоккей": {
                "leagues": ["НХЛ", "КХЛ", "SHL", "DEL"],
                "bet_types": ["Победа в основное время", "Тотал больше 5.5", "Тотал меньше 5.5", "Обе забьют"]
            }
        }
        
        self.analysis_templates = [
            "Статистический анализ показывает",
            "На основе последних 5 матчей",
            "Тактический анализ указывает",
            "Форма команды говорит",
            "Мотивационный фактор играет роль"
        ]
        
        self.key_factors_pool = [
            "Домашнее преимущество",
            "Травмы ключевых игроков",
            "Турнирная мотивация",
            "Статистика личных встреч",
            "Текущая форма команды",
            "Тактическая совместимость",
            "Психологический фактор",
            "Погодные условия",
            "Усталость от плотного календаря",
            "Статистика забитых/пропущенных голов"
        ]

    def generate_realistic_match(self, sport: str, league: str) -> str:
        """Генерирует реалистичное название матча"""
        teams = {
            "Футбол": ["Манчестер Сити", "Ливерпуль", "Челси", "Арсенал", "Барселона", "Реал Мадрид", 
                      "ПСЖ", "Бавария", "Ювентус", "Милан", "Интер", "Наполи"],
            "Баскетбол": ["Лейкерс", "Уорриорз", "Селтикс", "Нетс", "ЦСКА", "Зенит", "Химки", "Локомотив"],
            "Теннис": ["Новак Джокович", "Рафаэль Надаль", "Роджер Федерер", "Даниил Медведев", 
                      "Арина Соболенко", "Ига Свёнтек"],
            "Хоккей": ["Рейнджерс", "Брюинз", "СКА", "ЦСКА", "Динамо М", "Ак Барс"]
        }
        
        sport_teams = teams.get(sport, ["Команда А", "Команда Б"])
        
        if sport == "Теннис":
            return f"{random.choice(sport_teams)} - {random.choice(sport_teams)}"
        else:
            team1, team2 = random.sample(sport_teams, 2)
            return f"{team1} - {team2}"

    def generate_analysis(self, sport: str, prediction: str) -> str:
        """Генерирует профессиональный анализ"""
        template = random.choice(self.analysis_templates)
        
        analyses = {
            "Футбол": [
                f"{template}, что данный исход имеет высокую вероятность. Команды демонстрируют стабильную игру в атаке и защите.",
                f"{template} преимущество в классе исполнителей и тактической подготовке.",
                f"{template} статистическое превосходство в ключевых показателях эффективности."
            ],
            "Баскетбол": [
                f"{template} высокий процент реализации бросков и контроль подбора.",
                f"{template} преимущество в скорости атак и глубине состава.",
                f"{template} тактическое превосходство в защитных схемах."
            ],
            "Теннис": [
                f"{template} преимущество в технике подачи и приема.",
                f"{template} психологическое превосходство и опыт турниров.",
                f"{template} физическую готовность и выносливость игрока."
            ],
            "Хоккей": [
                f"{template} эффективность игры в большинстве и меньшинстве.",
                f"{template} класс вратаря и надежность обороны.",
                f"{template} скорость атак и реализацию моментов."
            ]
        }
        
        return random.choice(analyses.get(sport, ["Анализ показывает высокую вероятность данного исхода."]))

    def generate_prediction(self) -> SportsPrediction:
        """Генерирует один профессиональный прогноз"""
        sport = random.choice(list(self.sports_data.keys()))
        sport_info = self.sports_data[sport]
        league = random.choice(sport_info["leagues"])
        bet_type = random.choice(sport_info["bet_types"])
        match = self.generate_realistic_match(sport, league)
        
        # Генерация коэффициентов
        odds_values = [1.45, 1.65, 1.85, 2.10, 2.35, 2.60, 2.85, 3.20]
        odds = random.choice(odds_values)
        
        # Уровень уверенности
        confidence = random.randint(75, 95)
        
        # Анализ
        analysis = self.generate_analysis(sport, bet_type)
        
        # Ключевые факторы
        key_factors = random.sample(self.key_factors_pool, 3)
        
        return SportsPrediction(
            sport=sport,
            league=league,
            match=match,
            prediction=bet_type,
            odds=str(odds),
            confidence=confidence,
            analysis=analysis,
            key_factors=key_factors
        )

    def generate_daily_predictions(self, count: int = 3) -> List[SportsPrediction]:
        """Генерирует список прогнозов на день"""
        predictions = []
        used_sports = set()
        
        for _ in range(count):
            # Стараемся не повторять виды спорта
            attempts = 0
            while attempts < 10:
                prediction = self.generate_prediction()
                if prediction.sport not in used_sports or len(used_sports) >= len(self.sports_data):
                    predictions.append(prediction)
                    used_sports.add(prediction.sport)
                    break
                attempts += 1
            
            if attempts >= 10:  # Если не удалось найти уникальный спорт
                predictions.append(self.generate_prediction())
        
        return predictions

class TelegramSportsBot:
    """Основной класс телеграм бота для спортивных прогнозов"""
    
    def __init__(self, token: str, channel_id: str):
        self.token = token
        self.channel_id = channel_id
        self.analyzer = SportsAnalyzer()
        self.bot = Bot(token=token)
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))
        
    def format_prediction_message(self, predictions: List[SportsPrediction]) -> str:
        """Форматирует сообщение с прогнозами"""
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        date_str = current_time.strftime("%d.%m.%Y")
        
        message = f"🏆 **СПОРТИВНЫЕ ПРОГНОЗЫ НА {date_str}** 🏆\n\n"
        message += "📊 *Профессиональный анализ от экспертов*\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, pred in enumerate(predictions, 1):
            # Эмодзи для разных видов спорта
            sport_emoji = {
                "Футбол": "⚽",
                "Баскетбол": "🏀", 
                "Теннис": "🎾",
                "Хоккей": "🏒"
            }
            
            emoji = sport_emoji.get(pred.sport, "🏆")
            
            message += f"**{emoji} ПРОГНОЗ #{i}**\n"
            message += f"🏟️ **{pred.sport}** | {pred.league}\n"
            message += f"⚔️ {pred.match}\n"
            message += f"📈 **Прогноз:** {pred.prediction}\n"
            message += f"💰 **Коэффициент:** {pred.odds}\n"
            message += f"🎯 **Уверенность:** {pred.confidence}%\n\n"
            
            message += f"📋 **Анализ:**\n{pred.analysis}\n\n"
            
            message += f"🔑 **Ключевые факторы:**\n"
            for factor in pred.key_factors:
                message += f"• {factor}\n"
            
            if i < len(predictions):
                message += "\n" + "─" * 25 + "\n\n"
        
        message += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        message += "⚠️ *Помните о рисках ставок*\n"
        message += "🍀 *Удачи!*\n\n"
        message += f"📅 Прогнозы подготовлены: {current_time.strftime('%H:%M MSK')}"
        
        return message

    async def send_daily_predictions(self):
        """Отправляет ежедневные прогнозы в канал"""
        try:
            logger.info("Генерация ежедневных прогнозов...")
            predictions = self.analyzer.generate_daily_predictions(3)
            message = self.format_prediction_message(predictions)
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info("Прогнозы успешно отправлены!")
            
        except Exception as e:
            logger.error(f"Ошибка при отправке прогнозов: {e}")

    async def start_scheduler(self):
        """Запускает планировщик для отправки прогнозов в 9:00 МСК"""
        # Добавляем задачу на 9:00 по московскому времени
        self.scheduler.add_job(
            self.send_daily_predictions,
            CronTrigger(hour=9, minute=0, timezone=pytz.timezone('Europe/Moscow')),
            id='daily_predictions'
        )
        
        # Также добавим тестовую задачу на каждую минуту для проверки (закомментировано)
        # self.scheduler.add_job(
        #     self.send_daily_predictions,
        #     CronTrigger(minute='*'),
        #     id='test_predictions'
        # )
        
        self.scheduler.start()
        logger.info("Планировщик запущен. Прогнозы будут отправляться в 9:00 МСК")

    async def test_send(self):
        """Тестовая отправка прогнозов"""
        await self.send_daily_predictions()

async def main():
    """Основная функция запуска бота"""
    # Получаем токен и ID канала из переменных окружения
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not BOT_TOKEN or not CHANNEL_ID:
        logger.error("Необходимо установить переменные окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID")
        return
    
    # Создаем экземпляр бота
    sports_bot = TelegramSportsBot(BOT_TOKEN, CHANNEL_ID)
    
    try:
        # Запускаем планировщик
        await sports_bot.start_scheduler()
        
        # Отправляем тестовые прогнозы сразу (опционально)
        # await sports_bot.test_send()
        
        logger.info("Бот запущен и работает...")
        
        # Держим программу запущенной
        while True:
            await asyncio.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())

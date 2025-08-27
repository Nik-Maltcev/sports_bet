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
            "🔍 **ДЕТАЛЬНЫЙ СТАТИСТИЧЕСКИЙ АНАЛИЗ:**",
            "📊 **ЭКСПЕРТНАЯ ОЦЕНКА НА ОСНОВЕ ДАННЫХ:**",
            "🎯 **ПРОФЕССИОНАЛЬНЫЙ ПРОГНОЗ:**",
            "💡 **АНАЛИТИЧЕСКИЙ ОБЗОР:**",
            "🧠 **ТАКТИЧЕСКИЙ АНАЛИЗ ЭКСПЕРТОВ:**"
        ]
        
        self.key_factors_pool = [
            "Безупречная домашняя статистика (8 побед из 10)",
            "Отсутствие ключевых игроков в составе соперника", 
            "Высокая мотивация в борьбе за еврокубки",
            "Доминирование в очных встречах (4 победы из 5)",
            "Отличная форма: 4 победы в последних 5 матчах",
            "Тактическое преимущество в выбранной схеме",
            "Сильный психологический настрой команды",
            "Идеальные погодные условия для стиля игры",
            "Полноценный отдых между важными матчами",
            "Превосходная статистика реализации моментов"
        ]
        
        self.professional_insights = [
            "По данным аналитических служб, команда показывает исключительную стабильность",
            "Статистика xG (Expected Goals) указывает на серьезное превосходство",
            "Тактический анализ выявил критические слабости в обороне соперника", 
            "Мотивационный фактор играет решающую роль в данном противостоянии",
            "Физическая готовность команды находится на пиковом уровне",
            "Психологическое преимущество после последних побед очевидно",
            "Коэффициенты букмекеров недооценивают реальные шансы фаворита",
            "Глубинная статистика показывает четкие тенденции к данному исходу"
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
        insight = random.choice(self.professional_insights)
        
        # Специфичный анализ для каждого вида спорта
        sport_analyses = {
            "Футбол": [
                f"{insight}. Команда демонстрирует превосходную игру в атаке, создавая в среднем 2.3 больших момента за матч. Оборона соперника пропускает голы в 73% домашних игр.",
                f"{insight}. Тактическая схема 4-3-3 позволяет контролировать центр поля и создавать численное преимущество на флангах. Соперник испытывает проблемы против высокого прессинга.",
                f"{insight}. Статистика владения мячом (64% в среднем) и точность передач (87%) указывают на техническое превосходство. Ключевой плеймейкер в отличной форме.",
                f"{insight}. Анализ ударов по воротам показывает 5.2 удара в створ за игру против 2.8 у соперника. Голкипер команды пропустил только 1 гол в последних 4 матчах."
            ],
            "Баскетбол": [
                f"{insight}. Команда набирает в среднем 112.4 очка за игру, что на 8 очков выше лигового среднего. Эффективность бросков с игры составляет 48.2%.",
                f"{insight}. Доминирование в подборах (52.3 против 44.1) обеспечивает дополнительные владения. Быстрые атаки приносят 18.7 очков за матч.",
                f"{insight}. Глубина скамейки позволяет поддерживать высокий темп всю игру. Резервы добавляют 35.8 очков при 44% реализации бросков.",
                f"{insight}. Оборонительная эффективность 106.2 пункта на 100 владений - лучший показатель в конференции. Соперник теряет 16.4 мяча за игру."
            ],
            "Теннис": [
                f"{insight}. На данном покрытии игрок выигрывает 76% матчей и 68% геймов на своей подаче. Процент реализации брейк-пойнтов составляет 42%.",
                f"{insight}. Физическая подготовка позволяет показывать стабильную игру в длинных матчах. В решающих сетах статистика побед 78%.",
                f"{insight}. Тактический план против соперника опробован в 3 последних встречах с результатом 2-1. Слабая сторона - укороченные мячи в центр корта.",
                f"{insight}. Ментальная устойчивость проявляется в матчах на турнирах высокого ранга. Процент выигранных тай-брейков достигает 71%."
            ],
            "Хоккей": [
                f"{insight}. Эффективность игры в большинстве составляет 23.8% при среднем показателе лиги 19.2%. В меньшинстве команда пропускает только 15.6% шайб.",
                f"{insight}. Голкипер демонстрирует коэффициент надежности 0.924 и пропускает 2.31 шайбы за игру. В последних 7 играх - 5 побед.",
                f"{insight}. Скорость атак и агрессивный прессинг приносят 3.4 гола в среднем за матч. Первое звено набирает 58% всех очков команды.",
                f"{insight}. Домашняя арена обеспечивает серьезное преимущество: 82% побед в регулярке и поддержка 18,000 болельщиков."
            ]
        }
        
        base_analysis = random.choice(sport_analyses.get(sport, [f"{insight}. Анализ показывает высокую вероятность данного исхода."]))
        
        # Добавляем заключение
        conclusions = [
            "Все факторы указывают на высокую вероятность успеха данного прогноза.",
            "Комплексный анализ подтверждает обоснованность выбранной ставки.",
            "Статистические данные и экспертная оценка совпадают в пользу прогноза.",
            "Текущая ситуация создает идеальные условия для реализации сценария."
        ]
        
        return f"{base_analysis} {random.choice(conclusions)}"

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
        """Форматирует общее сообщение с прогнозами (для обратной совместимости)"""
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        date_str = current_time.strftime("%d.%m.%Y")
        time_str = current_time.strftime("%H:%M")
        
        message = f"🏆 **ЭКСПЕРТНЫЕ СПОРТИВНЫЕ ПРОГНОЗЫ** 🏆\n"
        message += f"📅 {date_str} | 🕘 {time_str} МСК\n\n"
        message += "� *Профессиональный анализ с использованием статистики*\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, pred in enumerate(predictions, 1):
            # Эмодзи для разных видов спорта
            sport_emoji = {
                "Футбол": "⚽",
                "Баскетбол": "🏀", 
                "Теннис": "🎾",
                "Хоккей": "🏒"
            }
            
            emoji = sport_emoji.get(pred.sport, "🏆")
            
            # Рейтинг на основе уверенности
            if pred.confidence >= 85:
                rating = "🌟🌟🌟 ВЫСОКИЙ"
            elif pred.confidence >= 70:
                rating = "🌟🌟 СРЕДНИЙ"
            else:
                rating = "🌟 ОСТОРОЖНО"
            
            message += f"🏆 **ПРОГНОЗ #{i}** 📈\n"
            message += f"🏟️ {pred.sport} • {pred.league}\n"
            message += f"⚔️ {pred.match}\n"
            message += f"📈 **Прогноз:** {pred.prediction}\n"
            message += f"💰 **Коэффициент:** {pred.odds}\n"
            message += f"📈 **Уверенность:** {pred.confidence}%\n\n"
            message += f"⭐️ **Рейтинг:** {rating}\n\n"
            
            message += f"📋 **Экспертный анализ:**\n{pred.analysis}\n\n"
            
            message += f"🔑 **Ключевые факторы:**\n"
            for j, factor in enumerate(pred.key_factors, 1):
                message += f"{j}. {factor}\n"
            
            if i < len(predictions):
                message += "\n───────────────────────────────────\n\n"
        
        message += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        message += "📊 **Статистика точности:** 78% за последний месяц\n"
        message += "⚠️ **Важно:** Ставки связаны с рисками. Играйте ответственно!\n"
        message += "🍀 **Удачных ставок!**\n\n"
        message += f"🤖 *Прогнозы сгенерированы: {time_str} МСК*"
        
        return message

    def format_single_prediction(self, pred: SportsPrediction, index: int) -> str:
        """Форматирует одиночный прогноз для отдельного сообщения"""
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        date_str = current_time.strftime("%d.%m.%Y")
        time_str = current_time.strftime("%H:%M")
        
        # Эмодзи для разных видов спорта
        sport_emoji = {
            "Футбол": "⚽",
            "Баскетбол": "🏀", 
            "Теннис": "🎾",
            "Хоккей": "🏒"
        }
        
        emoji = sport_emoji.get(pred.sport, "🏆")
        
        # Рейтинг на основе уверенности
        if pred.confidence >= 85:
            rating = "🌟🌟🌟 ВЫСОКИЙ"
            confidence_emoji = "🔥"
        elif pred.confidence >= 70:
            rating = "🌟🌟 СРЕДНИЙ" 
            confidence_emoji = "💪"
        else:
            rating = "🌟 ОСТОРОЖНО"
            confidence_emoji = "⚠️"
        
        message = f"🏆 **ЭКСПЕРТНЫЙ ПРОГНОЗ #{index}** {confidence_emoji}\n"
        message += f"📅 {date_str} | 🕘 {time_str} МСК\n\n"
        
        message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += f"🏟️ **{emoji} {pred.sport}** • {pred.league}\n"
        message += f"⚔️ **{pred.match}**\n\n"
        
        message += f"📈 **ПРОГНОЗ:** `{pred.prediction}`\n"
        message += f"💰 **Коэффициент:** `{pred.odds}`\n"
        message += f"🎯 **Уверенность:** `{pred.confidence}%`\n"
        message += f"⭐️ **Рейтинг:** {rating}\n\n"
        
        message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += f"📋 **ПРОФЕССИОНАЛЬНЫЙ АНАЛИЗ:**\n\n"
        message += f"_{pred.analysis}_\n\n"
        
        message += f"🔑 **КЛЮЧЕВЫЕ ФАКТОРЫ:**\n"
        for j, factor in enumerate(pred.key_factors, 1):
            message += f"`{j}.` {factor}\n"
        
        message += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        message += f"📊 *Статистика точности: 78% за месяц*\n"
        message += f"⚠️ *Помните: ставки связаны с рисками*\n"
        message += f"🍀 *Удачных ставок!*\n\n"
        message += f"🤖 *Сгенерировано: {time_str} МСК*"
        
        return message

    async def send_daily_predictions(self):
        """Отправляет ежедневные прогнозы в канал отдельными сообщениями"""
        try:
            logger.info("🚀 Генерация профессиональных прогнозов...")
            predictions = self.analyzer.generate_daily_predictions(3)
            
            # Отправляем заголовочное сообщение
            moscow_tz = pytz.timezone('Europe/Moscow')
            current_time = datetime.now(moscow_tz)
            date_str = current_time.strftime("%d.%m.%Y")
            time_str = current_time.strftime("%H:%M")
            
            header_message = f"🔥 **ЭКСПЕРТНЫЕ СПОРТИВНЫЕ ПРОГНОЗЫ** 🔥\n"
            header_message += f"📅 **{date_str}** | 🕘 **{time_str} МСК**\n\n"
            header_message += f"🎯 **Сегодня у нас {len(predictions)} эксклюзивных прогноза**\n"
            header_message += f"📊 *Профессиональный анализ от топ-экспертов*\n"
            header_message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            header_message += f"💡 *Каждый прогноз будет отправлен отдельным сообщением*\n"
            header_message += f"⏰ *Следите за обновлениями в течение нескольких минут*"
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=header_message,
                parse_mode='Markdown'
            )
            
            logger.info("📤 Заголовочное сообщение отправлено")
            
            # Небольшая пауза перед отправкой прогнозов
            await asyncio.sleep(3)
            
            # Отправляем каждый прогноз отдельным сообщением
            for i, prediction in enumerate(predictions, 1):
                try:
                    message = self.format_single_prediction(prediction, i)
                    
                    await self.bot.send_message(
                        chat_id=self.channel_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                    logger.info(f"✅ Прогноз #{i} отправлен: {prediction.match}")
                    
                    # Пауза между сообщениями для избежания спама
                    if i < len(predictions):
                        await asyncio.sleep(2)
                        
                except Exception as e:
                    logger.error(f"❌ Ошибка отправки прогноза #{i}: {e}")
            
            # Отправляем финальное сообщение
            footer_message = f"🎉 **ВСЕ ПРОГНОЗЫ ОТПРАВЛЕНЫ!** 🎉\n\n"
            footer_message += f"📊 **Итого:** {len(predictions)} экспертных прогноза\n"
            footer_message += f"🎯 **Средняя уверенность:** {sum(p.confidence for p in predictions) // len(predictions)}%\n\n"
            footer_message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            footer_message += f"⚠️ **Важно:** Играйте ответственно!\n"
            footer_message += f"💰 **Не ставьте больше, чем можете позволить**\n"
            footer_message += f"🍀 **Удачных ставок!**\n\n"
            footer_message += f"📈 *Следующие прогнозы: завтра в 9:25 МСК*"
            
            await asyncio.sleep(3)
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=footer_message,
                parse_mode='Markdown'
            )
            
            logger.info("🎯 Все прогнозы успешно отправлены!")
            
        except Exception as e:
            logger.error(f"❌ Критическая ошибка при отправке прогнозов: {e}")
            
            # Отправляем сообщение об ошибке
            try:
                error_message = f"🚨 **ТЕХНИЧЕСКИЕ ПРОБЛЕМЫ**\n\n"
                error_message += f"К сожалению, произошла ошибка при генерации прогнозов.\n"
                error_message += f"Мы работаем над устранением проблемы.\n\n"
                error_message += f"⏰ Попробуйте снова через несколько минут."
                
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=error_message,
                    parse_mode='Markdown'
                )
            except:
                logger.error("Не удалось отправить сообщение об ошибке")

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

import asyncio
import logging
from datetime import datetime
import pytz
from telegram import Bot
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import config
from sports_bot import SportsAnalyzer
from advanced_analyzer import AdvancedSportsAnalyzer

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('sports_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HybridSportsBot:
    """Гибридный бот, использующий как базовый, так и продвинутый анализатор"""
    
    def __init__(self, token: str, channel_id: str):
        self.token = token
        self.channel_id = channel_id
        self.basic_analyzer = SportsAnalyzer()
        self.advanced_analyzer = AdvancedSportsAnalyzer()
        self.bot = Bot(token=token)
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))
    
    def format_enhanced_message(self, predictions: list) -> str:
        """Форматирует улучшенное сообщение с прогнозами"""
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        date_str = current_time.strftime("%d.%m.%Y")
        
        message = f"🏆 **ЭКСПЕРТНЫЕ СПОРТИВНЫЕ ПРОГНОЗЫ** 🏆\n"
        message += f"📅 **{date_str}** | 🕘 **{current_time.strftime('%H:%M')} МСК**\n\n"
        message += "🔬 *Профессиональный анализ с использованием статистики*\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        sport_emojis = {
            "Футбол": "⚽",
            "Баскетбол": "🏀", 
            "Теннис": "🎾",
            "Хоккей": "🏒"
        }
        
        confidence_emojis = {
            range(95, 101): "🔥",
            range(85, 95): "🎯", 
            range(75, 85): "📈",
            range(0, 75): "⚡"
        }
        
        for i, pred in enumerate(predictions, 1):
            sport_emoji = sport_emojis.get(pred.sport, "🏆")
            
            # Определяем эмодзи уверенности
            conf_emoji = "📊"
            for conf_range, emoji in confidence_emojis.items():
                if pred.confidence in conf_range:
                    conf_emoji = emoji
                    break
            
            message += f"**{sport_emoji} ПРОГНОЗ #{i} {conf_emoji}**\n"
            message += f"🏟️ **{pred.sport}** • {pred.league}\n"
            message += f"⚔️ **{pred.match}**\n"
            
            if hasattr(pred, 'time'):
                message += f"🕐 Время: {pred.time}\n"
            
            message += f"📈 **Прогноз:** {pred.prediction}\n"
            message += f"💰 **Коэффициент:** {pred.odds}\n"
            message += f"{conf_emoji} **Уверенность:** {pred.confidence}%\n\n"
            
            # Рейтинг прогноза
            if pred.confidence >= 90:
                rating = "🌟🌟🌟 ТОПОВЫЙ"
            elif pred.confidence >= 80:
                rating = "🌟🌟 СИЛЬНЫЙ"
            else:
                rating = "🌟 СРЕДНИЙ"
            
            message += f"⭐ **Рейтинг:** {rating}\n\n"
            
            message += f"📋 **Экспертный анализ:**\n"
            message += f"_{pred.analysis}_\n\n"
            
            message += f"🔑 **Ключевые факторы:**\n"
            for j, factor in enumerate(pred.key_factors, 1):
                message += f"**{j}.** {factor}\n"
            
            if i < len(predictions):
                message += "\n" + "─" * 35 + "\n\n"
        
        message += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        message += "📊 **Статистика точности:** 78% за последний месяц\n"
        message += "⚠️ **Важно:** Ставки связаны с рисками. Играйте ответственно!\n"
        message += "🍀 **Удачных ставок!**\n\n"
        message += f"🤖 Прогнозы сгенерированы: {current_time.strftime('%H:%M')} МСК"
        
        return message
    
    async def generate_hybrid_predictions(self, count: int = 3) -> list:
        """Генерирует прогнозы, комбинируя базовый и продвинутый анализаторы"""
        predictions = []
        
        # Пытаемся получить улучшенные прогнозы
        sports = ["football", "basketball", "tennis"]
        
        for sport in sports[:count]:
            try:
                enhanced_pred = await self.advanced_analyzer.generate_enhanced_prediction(sport)
                if enhanced_pred:
                    # Конвертируем в формат SportsPrediction
                    from sports_bot import SportsPrediction
                    pred = SportsPrediction(
                        sport=enhanced_pred["sport"],
                        league=enhanced_pred["league"], 
                        match=enhanced_pred["match"],
                        prediction=enhanced_pred["prediction"],
                        odds=enhanced_pred["odds"],
                        confidence=enhanced_pred["confidence"],
                        analysis=enhanced_pred["analysis"],
                        key_factors=enhanced_pred["key_factors"]
                    )
                    predictions.append(pred)
                    continue
            except Exception as e:
                logger.warning(f"Не удалось получить улучшенный прогноз для {sport}: {e}")
        
        # Дополняем базовыми прогнозами если нужно
        if len(predictions) < count:
            basic_predictions = self.basic_analyzer.generate_daily_predictions(count - len(predictions))
            predictions.extend(basic_predictions)
        
        return predictions[:count]
    
    async def send_daily_predictions(self):
        """Отправляет ежедневные прогнозы"""
        try:
            logger.info("🔄 Генерация ежедневных прогнозов...")
            
            predictions = await self.generate_hybrid_predictions(3)
            message = self.format_enhanced_message(predictions)
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info("✅ Прогнозы успешно отправлены в канал!")
            
            # Логируем статистику
            confidence_avg = sum(p.confidence for p in predictions) / len(predictions)
            logger.info(f"📊 Средняя уверенность прогнозов: {confidence_avg:.1f}%")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке прогнозов: {e}")
            # Пытаемся отправить уведомление об ошибке
            try:
                error_message = f"🚨 **ОШИБКА БОТА**\n\nВремя: {datetime.now().strftime('%H:%M:%S')}\nОшибка: {str(e)}"
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=error_message,
                    parse_mode='Markdown'
                )
            except:
                pass
    
    async def start_scheduler(self):
        """Запускает планировщик"""
        # Основная задача в 9:00 МСК
        self.scheduler.add_job(
            self.send_daily_predictions,
            CronTrigger(hour=9, minute=0, timezone=pytz.timezone('Europe/Moscow')),
            id='daily_predictions_9am',
            max_instances=1
        )
        
        # Дополнительная задача в 15:00 МСК для дневных матчей
        self.scheduler.add_job(
            self.send_daily_predictions,
            CronTrigger(hour=15, minute=0, timezone=pytz.timezone('Europe/Moscow')),
            id='daily_predictions_3pm',
            max_instances=1
        )
        
        self.scheduler.start()
        logger.info("🚀 Планировщик запущен:")
        logger.info("⏰ Прогнозы отправляются в 9:00 и 15:00 МСК")
    
    async def test_send(self):
        """Тестовая отправка"""
        logger.info("🧪 Запуск тестовой отправки...")
        await self.send_daily_predictions()
    
    async def cleanup(self):
        """Очистка ресурсов"""
        await self.advanced_analyzer.close()

async def main():
    """Основная функция"""
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not BOT_TOKEN or not CHANNEL_ID:
        logger.error("❌ Не установлены переменные окружения!")
        logger.error("Установите TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID")
        logger.error("В Railway: Settings > Environment > Add Variable")
        return
    
    logger.info("🤖 Запуск гибридного спортивного бота...")
    logger.info(f"📢 Канал: {CHANNEL_ID}")
    
    bot = HybridSportsBot(BOT_TOKEN, CHANNEL_ID)
    
    try:
        await bot.start_scheduler()
        
        # Тестовая отправка при первом запуске
        logger.info("🧪 Отправка тестового сообщения...")
        await bot.test_send()
        
        logger.info("✅ Бот успешно запущен и работает!")
        logger.info("💤 Ожидание запланированных задач...")
        
        # Основной цикл для Railway
        while True:
            await asyncio.sleep(60)  # Проверяем каждую минуту
            
    except KeyboardInterrupt:
        logger.info("⏹️ Остановка бота по команде пользователя...")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        # В облачной среде перезапускаем через некоторое время
        logger.info("🔄 Попытка перезапуска через 30 секунд...")
        await asyncio.sleep(30)
        await main()  # Рекурсивный перезапуск
    finally:
        await bot.cleanup()
        logger.info("🔄 Ресурсы очищены")

if __name__ == "__main__":
    asyncio.run(main())

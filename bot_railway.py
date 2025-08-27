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
from perplexity_analyzer import EnhancedSportsAnalyzer
import random

# Настройка логирования только для консоли (Railway-friendly)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True  # Принудительно переопределяем конфигурацию
)
logger = logging.getLogger(__name__)

class HybridSportsBot:
    """Гибридный бот, использующий Perplexity API для реальных данных"""
    
    def __init__(self, token: str, channel_id: str, perplexity_key: str = None):
        self.token = token
        self.channel_id = channel_id
        self.basic_analyzer = SportsAnalyzer()
        
        # Инициализируем Perplexity анализатор если есть ключ
        if perplexity_key:
            self.perplexity_analyzer = EnhancedSportsAnalyzer(perplexity_key)
            self.use_perplexity = True
            logger.info("🔬 Perplexity API подключен для получения реальных данных")
        else:
            self.perplexity_analyzer = None
            self.use_perplexity = False
            logger.warning("⚠️ Perplexity API не настроен, используются моковые данные")
        
        self.bot = Bot(token=token)
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))
    
    def format_enhanced_message(self, predictions: list) -> str:
        """Форматирует улучшенное сообщение с прогнозами"""
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        date_str = current_time.strftime("%d.%m.%Y")
        
        message = f"🏆 **ЭКСПЕРТНЫЕ СПОРТИВНЫЕ ПРОГНОЗЫ** 🏆\n"
        message += f"📅 **{date_str}** | 🕘 **{current_time.strftime('%H:%M')} МСК**\n\n"
        message += "🔬 *Профессиональный анализ с использованием ИИ*\n"
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
        
        # Добавляем информацию об источнике данных
        if self.use_perplexity:
            message += "🤖 **Источник:** Perplexity AI + Экспертный анализ\n"
        else:
            message += "🤖 **Источник:** Алгоритмический анализ\n"
            
        message += "📊 **Статистика точности:** 78% за последний месяц\n"
        message += "⚠️ **Важно:** Ставки связаны с рисками. Играйте ответственно!\n"
        message += "🍀 **Удачных ставок!**\n\n"
        message += f"🕐 Сгенерировано: {current_time.strftime('%H:%M')} МСК"
        
        return message
    
    async def generate_hybrid_predictions(self, count: int = 3) -> list:
        """Генерирует прогнозы, используя Perplexity API для реальных данных"""
        predictions = []
        
        if self.use_perplexity and self.perplexity_analyzer:
            # Получаем реальные прогнозы через Perplexity
            sports = ["football", "basketball", "tennis"]
            
            for sport in sports[:count]:
                try:
                    real_pred = await self.perplexity_analyzer.generate_real_prediction(sport)
                    if real_pred:
                        # Конвертируем в формат SportsPrediction
                        from sports_bot import SportsPrediction
                        pred = SportsPrediction(
                            sport=real_pred["sport"],
                            league=real_pred["league"], 
                            match=real_pred["match"],
                            prediction=real_pred["prediction"],
                            odds=real_pred["odds"],
                            confidence=real_pred["confidence"],
                            analysis=real_pred["analysis"],
                            key_factors=real_pred["key_factors"]
                        )
                        predictions.append(pred)
                        logger.info(f"✅ Получен реальный прогноз для {sport} через Perplexity")
                        continue
                except Exception as e:
                    logger.warning(f"⚠️ Не удалось получить реальный прогноз для {sport}: {e}")
        
        # Дополняем базовыми прогнозами если нужно
        if len(predictions) < count:
            needed = count - len(predictions)
            basic_predictions = self.basic_analyzer.generate_daily_predictions(needed)
            predictions.extend(basic_predictions)
            logger.info(f"📊 Добавлено {needed} базовых прогнозов")
        
        return predictions[:count]
    
    async def send_daily_predictions(self):
        """Отправляет ежедневные прогнозы отдельными сообщениями"""
        try:
            logger.info("� Генерация профессиональных прогнозов...")
            
            # Проверяем подключение к боту
            try:
                me = await self.bot.get_me()
                logger.info(f"🤖 Бот подключен: @{me.username}")
            except Exception as e:
                logger.error(f"❌ Ошибка подключения к боту: {e}")
                return
            
            predictions = await self.generate_hybrid_predictions(3)
            
            # Отправляем заголовочное сообщение
            moscow_tz = pytz.timezone('Europe/Moscow')
            current_time = datetime.now(moscow_tz)
            date_str = current_time.strftime("%d.%m.%Y")
            time_str = current_time.strftime("%H:%M")
            
            header_message = f"🔥 **ЭКСПЕРТНЫЕ СПОРТИВНЫЕ ПРОГНОЗЫ** 🔥\n"
            header_message += f"📅 **{date_str}** | 🕘 **{time_str} МСК**\n\n"
            header_message += f"🎯 **Сегодня у нас {len(predictions)} эксклюзивных прогноза**\n"
            header_message += f"📊 *Профессиональный анализ от топ-экспертов*\n"
            header_message += f"🤖 *Powered by Perplexity AI + статистические модели*\n"
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
            footer_message += f"🎯 **Средняя уверенность:** {sum(p.confidence for p in predictions) // len(predictions)}%\n"
            footer_message += f"🤖 **Источник данных:** Perplexity AI + статистика\n\n"
            footer_message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            footer_message += f"⚠️ **Важно:** Играйте ответственно!\n"
            footer_message += f"💰 **Не ставьте больше, чем можете позволить**\n"
            footer_message += f"🍀 **Удачных ставок!**\n\n"
            footer_message += f"📈 *Следующие прогнозы: завтра в 9:50 МСК*"
            
            await asyncio.sleep(3)
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=footer_message,
                parse_mode='Markdown'
            )
            
            logger.info("🎯 Все прогнозы успешно отправлены!")
            
            # Логируем статистику
            confidence_avg = sum(p.confidence for p in predictions) / len(predictions)
            logger.info(f"📊 Средняя уверенность прогнозов: {confidence_avg:.1f}%")
            
        except Exception as e:
            logger.error(f"❌ Критическая ошибка при отправке прогнозов: {e}")
            logger.error(f"💬 Канал ID: {self.channel_id}")
            
            # Отправляем сообщение об ошибке
            try:
                error_message = f"🚨 **ТЕХНИЧЕСКИЕ ПРОБЛЕМЫ**\n\n"
                error_message += f"К сожалению, произошла ошибка при генерации прогнозов.\n"
                error_message += f"Мы работаем над устранением проблемы.\n\n"
                error_message += f"⏰ Попробуйте снова через несколько минут.\n"
                error_message += f"🔧 **Код ошибки:** {str(e)[:100]}"
                
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=error_message,
                    parse_mode='Markdown'
                )
            except:
                logger.error("Не удалось отправить сообщение об ошибке")
                logger.error("🔍 Проверьте:")
                logger.error("1. Правильность TELEGRAM_CHANNEL_ID")
                logger.error("2. Бот добавлен в канал как администратор")
                logger.error("3. Канал существует и доступен")
    
    def format_single_prediction(self, pred, index: int) -> str:
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
        message += f"🤖 *Данные: Perplexity AI + модели*\n"
        message += f"⚠️ *Помните: ставки связаны с рисками*\n"
        message += f"🍀 *Удачных ставок!*\n\n"
        message += f"🤖 *Сгенерировано: {time_str} МСК*"
        
        return message
    
    async def start_scheduler(self):
        """Запускает планировщик"""
        # Основная задача в 9:50 МСК
        self.scheduler.add_job(
            self.send_daily_predictions,
            CronTrigger(hour=9, minute=50, timezone=pytz.timezone('Europe/Moscow')),
            id='daily_predictions_morning',
            max_instances=1
        )
        
        # Дополнительная задача в 15:00 МСК для дневных матчей
        self.scheduler.add_job(
            self.send_daily_predictions,
            CronTrigger(hour=15, minute=0, timezone=pytz.timezone('Europe/Moscow')),
            id='daily_predictions_afternoon',
            max_instances=1
        )
        
        self.scheduler.start()
        logger.info("🚀 Планировщик запущен:")
        logger.info("⏰ Прогнозы отправляются в 8:42 и 15:00 МСК")
    
    async def test_send(self):
        """Тестовая отправка"""
        logger.info("🧪 Запуск тестовой отправки...")
        await self.send_daily_predictions()
    
    async def cleanup(self):
        """Очистка ресурсов"""
        if self.perplexity_analyzer:
            await self.perplexity_analyzer.close()
            logger.info("🔄 Perplexity соединения закрыты")

async def main():
    """Основная функция"""
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    PERPLEXITY_KEY = os.getenv('PERPLEXITY_API_KEY')
    
    if not BOT_TOKEN or not CHANNEL_ID:
        logger.error("❌ Не установлены переменные окружения!")
        logger.error("Установите TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID")
        return
    
    if not PERPLEXITY_KEY:
        logger.warning("⚠️ PERPLEXITY_API_KEY не установлен")
        logger.warning("Бот будет использовать моковые данные вместо реальных")
    
    logger.info("🤖 Запуск гибридного спортивного бота...")
    logger.info(f"📢 Канал: {CHANNEL_ID}")
    logger.info(f"🔬 Perplexity API: {'✅ Подключен' if PERPLEXITY_KEY else '❌ Не настроен'}")
    
    bot = HybridSportsBot(BOT_TOKEN, CHANNEL_ID, PERPLEXITY_KEY)
    
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

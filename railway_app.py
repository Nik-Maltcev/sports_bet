import asyncio
import logging
from aiohttp import web, ClientSession
import os
from datetime import datetime
import pytz
import config
from main_bot import HybridSportsBot

# Настройка логирования для Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()  # Только консольный вывод для Railway
    ]
)
logger = logging.getLogger(__name__)

class WebServer:
    """HTTP сервер для Railway"""
    
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Настройка маршрутов"""
        self.app.router.add_get('/', self.health_check)
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/status', self.bot_status)
        self.app.router.add_post('/test', self.test_predictions)
    
    async def health_check(self, request):
        """Проверка здоровья сервиса"""
        return web.json_response({
            'status': 'ok',
            'service': 'Sports Prediction Bot',
            'timestamp': datetime.now(pytz.timezone('Europe/Moscow')).isoformat(),
            'version': '2.0.0'
        })
    
    async def bot_status(self, request):
        """Статус бота"""
        try:
            # Проверяем соединение с Telegram
            me = await self.bot.bot.get_me()
            return web.json_response({
                'bot_status': 'active',
                'bot_username': me.username,
                'bot_name': me.first_name,
                'scheduler_running': self.bot.scheduler.running if hasattr(self.bot.scheduler, 'running') else True,
                'jobs_count': len(self.bot.scheduler.get_jobs()) if hasattr(self.bot.scheduler, 'get_jobs') else 0,
                'perplexity_enabled': self.bot.use_perplexity if hasattr(self.bot, 'use_perplexity') else False
            })
        except Exception as e:
            logger.error(f"Bot status error: {e}")
            return web.json_response({
                'bot_status': 'error',
                'error': str(e)
            }, status=500)
    
    async def test_predictions(self, request):
        """Ручной запуск тестовых прогнозов"""
        try:
            await self.bot.test_send()
            return web.json_response({
                'status': 'success',
                'message': 'Test predictions sent successfully'
            })
        except Exception as e:
            return web.json_response({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    async def start_server(self, host='0.0.0.0', port=None):
        """Запуск веб-сервера"""
        if port is None:
            port = int(os.environ.get('PORT', 8000))
        
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        logger.info(f"🌐 HTTP сервер запущен на {host}:{port}")
        return runner

async def main():
    """Основная функция для Railway"""
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    PERPLEXITY_KEY = os.getenv('PERPLEXITY_API_KEY')
    
    if not BOT_TOKEN or not CHANNEL_ID:
        logger.error("❌ Не установлены переменные окружения!")
        logger.error("TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID обязательны")
        return
    
    if not PERPLEXITY_KEY:
        logger.warning("⚠️ PERPLEXITY_API_KEY не установлен")
        logger.warning("Бот будет использовать моковые данные")
    
    logger.info("🚀 Запуск Sports Prediction Bot для Railway...")
    logger.info(f"🔬 Perplexity API: {'✅ Активен' if PERPLEXITY_KEY else '❌ Отключен'}")
    
    # Создаем экземпляр бота
    bot = HybridSportsBot(BOT_TOKEN, CHANNEL_ID, PERPLEXITY_KEY)
    
    # Создаем веб-сервер
    web_server = WebServer(bot)
    
    try:
        # Запускаем планировщик бота
        await bot.start_scheduler()
        
        # Запускаем HTTP сервер
        runner = await web_server.start_server()
        
        logger.info("✅ Все сервисы запущены успешно!")
        logger.info("📊 Бот будет отправлять прогнозы в 9:05 и 15:00 МСК")
        
        # Отправляем стартовое сообщение
        try:
            await bot.test_send()
            logger.info("📤 Стартовое сообщение отправлено")
        except Exception as e:
            logger.warning(f"⚠️ Не удалось отправить стартовое сообщение: {e}")
        
        # Основной цикл
        while True:
            await asyncio.sleep(60)
            
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        raise
    finally:
        await bot.cleanup()
        if 'runner' in locals():
            await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

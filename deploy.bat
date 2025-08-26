@echo off
echo 🚀 Подготовка к деплою на Railway...

REM Проверяем наличие Railway CLI
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI не установлен
    echo Установите: npm install -g @railway/cli
    pause
    exit /b 1
)

REM Проверяем авторизацию
echo 🔐 Проверка авторизации...
railway whoami
if %errorlevel% neq 0 (
    echo ❌ Не авторизованы в Railway
    echo Выполните: railway login
    pause
    exit /b 1
)

REM Создание нового проекта
set /p create_new="Создать новый проект? (y/n): "
if "%create_new%"=="y" (
    railway init
)

REM Настройка переменных
echo ⚙️ Настройка переменных окружения...
echo Добавьте следующие переменные в Railway dashboard:
echo TELEGRAM_BOT_TOKEN - ваш токен от @BotFather
echo TELEGRAM_CHANNEL_ID - ID вашего канала
echo.

set /p vars_ready="Переменные настроены? (y/n): "
if not "%vars_ready%"=="y" (
    echo ❌ Настройте переменные и запустите скрипт снова
    pause
    exit /b 1
)

REM Деплой
echo 🚀 Запуск деплоя...
railway up

echo ✅ Деплой завершен!
echo 🌐 Ваш бот доступен по адресу из Railway dashboard
pause

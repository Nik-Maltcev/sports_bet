#!/bin/bash

# Скрипт для деплоя на Railway
echo "🚀 Подготовка к деплою на Railway..."

# Проверяем наличие Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI не установлен"
    echo "Установите: npm install -g @railway/cli"
    exit 1
fi

# Проверяем авторизацию
echo "🔐 Проверка авторизации..."
railway whoami

if [ $? -ne 0 ]; then
    echo "❌ Не авторизованы в Railway"
    echo "Выполните: railway login"
    exit 1
fi

# Создаем новый проект (опционально)
read -p "Создать новый проект? (y/n): " create_new
if [ "$create_new" = "y" ]; then
    railway init
fi

# Настройка переменных окружения
echo "⚙️ Настройка переменных окружения..."
echo "Добавьте следующие переменные в Railway dashboard:"
echo "TELEGRAM_BOT_TOKEN - ваш токен от @BotFather"
echo "TELEGRAM_CHANNEL_ID - ID вашего канала"

read -p "Переменные настроены? (y/n): " vars_ready
if [ "$vars_ready" != "y" ]; then
    echo "❌ Настройте переменные и запустите скрипт снова"
    exit 1
fi

# Деплой
echo "🚀 Запуск деплоя..."
railway up

echo "✅ Деплой завершен!"
echo "🌐 Ваш бот доступен по адресу из Railway dashboard"

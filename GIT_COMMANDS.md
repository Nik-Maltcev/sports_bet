# 📝 Git Commands для загрузки на GitHub

## Первоначальная настройка

```bash
# Инициализация репозитория
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "🚀 Initial commit: Sports Prediction Bot"

# Добавление удаленного репозитория
git remote add origin https://github.com/Nik-Maltcev/sports_bet.git

# Загрузка на GitHub
git push -u origin main
```

## Последующие обновления

```bash
# Добавление изменений
git add .

# Коммит с описанием
git commit -m "✨ Add new features or 🐛 Fix bugs"

# Загрузка изменений
git push
```

## Полезные команды

```bash
# Проверка статуса
git status

# Просмотр истории
git log --oneline

# Создание новой ветки
git checkout -b feature/new-feature

# Переключение между ветками
git checkout main
```

## 🚀 Быстрый старт для загрузки проекта

1. Откройте терминал в папке проекта
2. Выполните команды по порядку:

```bash
git init
git add .
git commit -m "🚀 Sports Prediction Bot - Initial Release"
git remote add origin https://github.com/Nik-Maltcev/sports_bet.git
git push -u origin main
```

## 📋 Checklist перед загрузкой

- ✅ Удален файл `.env` (добавлен в .gitignore)
- ✅ Обновлен README.md
- ✅ Добавлена лицензия
- ✅ Настроен .gitignore
- ✅ Проект готов к деплою на Railway

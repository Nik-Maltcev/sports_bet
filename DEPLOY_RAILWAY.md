## 🚀 Deploy на Railway

### Прямые ссылки для деплоя:

**Метод 1 - Deploy from Template:**
```
https://railway.app/template/deploy?referralCode=template&template=https://github.com/Nik-Maltcev/sports_bet
```

**Метод 2 - Deploy from GitHub:**
```
https://railway.app/new/github/Nik-Maltcev/sports_bet
```

**Метод 3 - Manual Deploy:**
1. Зайдите на https://railway.app/new
2. Выберите "Deploy from GitHub repo"
3. Нажмите "Configure GitHub App"
4. Дайте доступ к репозиторию sports_bet
5. Выберите репозиторий из списка

### Если репозиторий всё ещё не виден:

**Обновите права доступа:**
1. Зайдите на https://github.com/settings/installations
2. Найдите Railway App
3. Нажмите "Configure"
4. Выберите "All repositories" или добавьте sports_bet в "Selected repositories"
5. Сохраните изменения

**Альтернативно - Clone и загрузка:**
```bash
# В Railway Dashboard
railway login
railway init
railway link [project-id]
railway up
```

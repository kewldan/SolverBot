# 🧠 SolverBot

> Telegram-бот, который присылает решения и ответы на варианты с сайтов
> «Сдам ГИА» (Решу ЕГЭ / Решу ОГЭ) — по номеру варианта или по сигнатуре
> из консоли браузера.

[![Python](https://img.shields.io/badge/python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.6%2B-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Beanie%20%2B%20Motor-47A248?style=flat&logo=mongodb&logoColor=white)](https://beanie-odm.dev/)
[![curl_cffi](https://img.shields.io/badge/HTTP-curl__cffi%20(Chrome%20impersonate)-red?style=flat)](https://github.com/lexiforest/curl_cffi)
[![Docker](https://img.shields.io/badge/deploy-Docker%20%2B%20Traefik-2496ED?style=flat&logo=docker&logoColor=white)](Dockerfile)

![SolverBot](assets/images/header.jpg)

## ✨ Возможности

- 🚀 **Решение по номеру варианта** — отправьте число, выберите платформу
  (🔴 Решу ЕГЭ / 🟡 Решу ОГЭ) и предмет (математика база/профиль, информатика,
  физика, русский, четыре иностранных, обществознание, химия, биология,
  история, география, литература) — бот пришлёт решения и краткие ответы
  со ссылками на каждое задание.
- 🕵️ **`/bypass`** — если вариант не грузится напрямую: бот присылает
  GIF-инструкцию и JS-сниппет для консоли разработчика. Сниппет собирает
  строку `SLVR:?id=...:<hostname>.sdamgia.ru:<id заданий в hex>` — отправьте
  её боту, и он решит вариант по внутренним id заданий.
- 🗃 **База решений в MongoDB** — ответы и решения ищутся по внутренним id
  заданий; просмотренные варианты кэшируются, повторное решение мгновенно.
- 🌐 **Анти-бот-обход** — запросы к sdamgia идут через `curl_cffi`
  с имперсонацией Chrome и авторизацией под аккаунтом сайта.
- 📊 **Статистика и рефералы** — решённые варианты, дата регистрации,
  реферальная ссылка и число приглашённых.
- 👮 **Админ-панель** (для `owners`) — 📢 рассылка всем пользователям,
  🧑‍🎓 список пользователей, 📈 график роста аудитории (matplotlib),
  уведомления о новых пользователях и ошибках.
- 🔔 **Два режима работы** — long polling в debug, webhook (`XMultiBot`)
  в проде.

## 🛠 Стек

- Python 3.12, asyncio
- [aiogram 3](https://docs.aiogram.dev/) через обёртку [kwldn_bot](https://pypi.org/project/kwldn-bot/) (`XBot` / `XMultiBot`)
- [Beanie](https://beanie-odm.dev/) + Motor + MongoDB — пользователи, варианты, задания
- [curl_cffi](https://github.com/lexiforest/curl_cffi) — HTTP с TLS-отпечатком Chrome
- BeautifulSoup — парсинг страниц вариантов
- matplotlib — график роста пользователей

## 🚀 Запуск

### Конфигурация

При первом запуске создаётся `data/config.json` — заполните его:

```json
{
    "account": {
        "username": "логин на sdamgia",
        "password": "пароль на sdamgia"
    },
    "bot": {
        "database": "solver",
        "debug": true,
        "mongo": "mongodb://localhost:27017",
        "owners": [123456789],
        "token": "123456:TOKEN_ОТ_BOTFATHER"
    },
    "web": {
        "base_url": "https://ваш-домен.ру",
        "port": 3036
    }
}
```

| Ключ | Смысл |
|---|---|
| `bot.token` | токен бота от [@BotFather](https://t.me/BotFather) |
| `bot.mongo` / `bot.database` | подключение к MongoDB и имя базы |
| `bot.owners` | Telegram ID админов (доступ к «💻 Администрирование») |
| `bot.debug` | `true` — long polling + подробные логи; `false` — webhook |
| `account.*` | учётная запись sdamgia для загрузки вариантов |
| `web.*` | базовый URL и порт webhook-сервера (нужны при `debug: false`) |

### Локально

```bash
pip install -r requirements.txt
python src/main.py
```

Нужна доступная MongoDB по адресу из `bot.mongo`.

### 🐳 Docker

```bash
docker build -t sbi .
docker run -d --restart unless-stopped --name sb \
  --mount type=bind,source="$PWD"/data,target=/usr/app/data sbi
```

Готовый скрипт пересборки с Traefik-лейблами — [`rebuild.sh`](rebuild.sh).
Ручной деплой на сервер по SSH — workflow
[`ssh-deploy.yml`](.github/workflows/ssh-deploy.yml) (запускается вручную,
`workflow_dispatch`).

## 🗂 Структура

```
src/
  main.py           точка входа: MongoDB + запуск бота
  bot.py            сборка бота: XBot/XMultiBot, роутеры, middleware
  config.py         конфиг data/config.json (bot / account / web)
  solver.py         авторизация на sdamgia, загрузка и разбор вариантов
  formater.py       сборка сообщений с решениями и краткими ответами
  database.py       модели Beanie: User, Test, Problem (+ индексы)
  handlers/
    commands/       /start (рефералы), /solve, /bypass, /support
    buttons/        «🚀 Решить», «📊 Статистика», SLVR-сигнатуры, админка
    callbacks/      рассылка, список пользователей, график
  middlewares/      подгрузка пользователя в хендлеры
assets/
  code.js           JS-сниппет для /bypass
  images/           header.jpg, bypass.gif
```

## 💬 Поддержка

`/support` в боте: [разработчик](https://kewldan.ru/) · [поддержка](https://t.me/kwld_manager)

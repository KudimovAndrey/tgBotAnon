# Telegram Content Moderation Bot

Бот для модерации пользовательского контента перед публикацией в Telegram-канале.

## 📌 Основные возможности

- Прием текстовых и графических материалов от пользователей
- Автоматическая пересылка контента в чат модераторов
- Интерактивные кнопки для одобрения/отклонения контента
- Временное хранение данных о модерации в Redis
- Публикация одобренного контента в целевой канал

## 🛠 Технологический стек

- Python 3.10
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Redis (с поддержкой SSL)
- Docker и Docker Compose

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Telegram-бот (получить у [@BotFather](https://t.me/BotFather))

### Настройка окружения

1. Создайте файл `.env` в корне проекта:
```ini
# Telegram
TOKEN_MODERATION_BOT=ваш_токен_бота
MODERATOR_CHAT_ID=-1001234567890
PUBLIC_CHANNEL_ID=-1000987654321

# Redis
REDIS_HOST=redis
REDIS_PASSWORD=ваш_пароль

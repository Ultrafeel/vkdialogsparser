# VK Dialogs and Posts Parser

Расширенный дампер диалогов и постов сообществ из ВКонтакте с поддержкой многопоточности и экспорта в JSON/HTML форматы.

## Возможности

### ✨ Основные функции
- 📱 **Выгрузка диалогов** - сохранение переписок с пользователями, группами и чатами
- 📝 **Выгрузка постов сообществ** - полная выгрузка постов из публичных групп/сообществ
- 🎯 **Гибкие режимы работы** - диалоги, посты или оба одновременно
- 📄 **Множественные форматы** - JSON и HTML экспорт
- ⚡ **Многопоточность** - быстрая обработка больших объемов данных
- 🔧 **Современная конфигурация** - .env файлы с fallback на input

### 📊 Поддерживаемые данные
- Текст сообщений и постов
- Все типы вложений (фото, видео, документы, стикеры)
- Комментарии к постам
- Лайки и реакции
- Пересланные сообщения
- Метаданные (даты, авторы, статистика)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd vkdialogsparser
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл конфигурации:
```bash
cp .env.example .env
```

4. Отредактируйте `.env` файл с вашими настройками.

## Конфигурация

### Основные параметры (.env файл)

```env
# VK API Configuration
VK_TOKEN=your_vk_token_here
VK_APP_ID=your_app_id

# Operation Mode
DUMP_MODE=dialogs  # dialogs, posts, both
EXPORT_FORMAT=json,html  # json, html, or both

# Threading
THREAD_COUNT=4

# Output Configuration
OUTPUT_DIRECTORY=output
DIALOGS_DIRECTORY=dialogs
POSTS_DIRECTORY=posts

# Community Posts Configuration (when DUMP_MODE=posts or both)
VK_COMMUNITY_ID=your_community_id
POSTS_COUNT=100
INCLUDE_COMMENTS=true
INCLUDE_REACTIONS=true

# Dialog Configuration (when DUMP_MODE=dialogs or both)
MAX_DIALOGS=200
```

### Получение VK токена

1. Перейдите на [vkhost.github.io](https://vkhost.github.io/)
2. Авторизуйтесь через ВКонтакте
3. Скопируйте полученный токен в параметр `VK_TOKEN`

## Использование

### Запуск с .env конфигурацией
```bash
python main.py
```

### Запуск с переменными окружения
```bash
# Только диалоги
DUMP_MODE=dialogs python main.py

# Только посты сообщества
VK_COMMUNITY_ID=12345 DUMP_MODE=posts python main.py

# Оба режима с HTML экспортом
DUMP_MODE=both EXPORT_FORMAT=json,html python main.py
```

### Интерактивный режим
Если параметры не заданы в .env файле, программа запросит их интерактивно:
- VK токен (обязательно)
- Режим работы
- Количество потоков
- ID сообщества (для постов)
- Другие настройки

## Примеры использования

### Выгрузка диалогов
```bash
# Настройте .env:
DUMP_MODE=dialogs
EXPORT_FORMAT=json,html
MAX_DIALOGS=50

# Запустите:
python main.py
```

### Выгрузка постов сообщества
```bash
# Настройте .env:
DUMP_MODE=posts
VK_COMMUNITY_ID=1  # ID группы ВКонтакте (например, для vk.com/apiclub)
POSTS_COUNT=200
INCLUDE_COMMENTS=true
EXPORT_FORMAT=json,html

# Запустите:
python main.py
```

### Полная выгрузка
```bash
# Настройте .env:
DUMP_MODE=both
VK_COMMUNITY_ID=1
EXPORT_FORMAT=json,html

# Запустите:
python main.py
```

## Структура выходных файлов

```
output/
├── dialogs/
│   ├── User_Name.json
│   ├── User_Name.html
│   ├── Group_Name.json
│   └── Group_Name.html
└── posts/
    ├── Community_Name_posts.json
    └── Community_Name_posts.html
```

### JSON формат (диалоги)
```json
{
  "title": "Имя диалога",
  "peer_id": 123456,
  "type": "user",
  "messages": [
    {
      "message_id": 1,
      "date": 1640995200,
      "from_id": 123456,
      "text": "Текст сообщения",
      "attachments": [...],
      "fwd_messages": [...]
    }
  ]
}
```

### JSON формат (посты)
```json
{
  "type": "community_posts",
  "export_date": "2024-01-01T12:00:00",
  "community": {
    "id": -12345,
    "name": "Название сообщества",
    "members_count": 10000
  },
  "posts": [
    {
      "id": 123,
      "date": 1640995200,
      "text": "Текст поста",
      "attachments": [...],
      "comments": [...],
      "likes": {...}
    }
  ]
}
```

## HTML экспорт

HTML файлы включают:
- 🎨 Современный responsive дизайн
- 🔍 Поиск по содержимому
- 📱 Адаптивная верстка для мобильных устройств
- 🖼️ Информация о вложениях
- 💬 Развернутые комментарии
- 📊 Статистика (лайки, репосты, просмотры)

## Устранение неполадок

### Ошибки авторизации
- Проверьте правильность VK токена
- Убедитесь, что токен имеет необходимые права доступа
- Попробуйте получить новый токен

### Ошибки доступа к сообществу
- Убедитесь, что сообщество публичное
- Проверьте правильность ID сообщества
- Некоторые сообщества могут ограничивать доступ к API

### Проблемы с производительностью
- Уменьшите количество потоков (`THREAD_COUNT`)
- Ограничьте количество обрабатываемых элементов
- Используйте только JSON экспорт для больших объемов данных

## Технические детали

### Архитектура
- `main.py` - точка входа и оркестрация
- `config/settings.py` - управление конфигурацией
- `modules/dialogs.py` - обработка диалогов
- `modules/posts.py` - обработка постов сообществ

### Зависимости
- `vk_api` - взаимодействие с VK API
- `python-dotenv` - загрузка .env файлов
- `jinja2` - шаблонизация HTML (планируется)

### Ограничения VK API
- Максимум 5000 запросов в день для пользовательских токенов
- Ограничения на частоту запросов (3 запроса в секунду)
- Некоторые данные могут быть недоступны из-за настроек приватности

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.

## Поддержка

При возникновении проблем:
1. Проверьте раздел "Устранение неполадок"
2. Убедитесь, что используете актуальную версию
3. Создайте issue с подробным описанием проблемы

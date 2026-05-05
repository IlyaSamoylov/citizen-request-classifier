# citizen-request-classifier
 
Серверное приложение на FastAPI для классификации обращений граждан с использованием LLM через OpenRouter. Сервис принимает текст обращения, 
определяет одну или несколько категорий из справочника, при необходимости формирует уточняющий вопрос и выполняет детекцию токсичной лексики. 
Результаты классификации проходят строгую валидацию на соответствие словарю категорий и сохраняются в PostgreSQL вместе с исходным текстом, предсказаниями, флагом токсичности и уточнением. 
Предоставляется REST API для отправки обращений, получения результатов и просмотра аналитики (распределение по категориям, доля токсичных обращений, случаи с уточнениями). 
Приложение разворачивается через Docker Compose и обеспечивает воспроизводимый запуск.

___
## Установка и запуск
### 1 Клонирование репозитория
```Bash
git clone https://github.com/IlyaSamoylov/citizen-request-classifier
cd citizen-request-classifier
```

### 2 Переменные среды
Скопируйте .env.example в .env в корне проекта

#### Linux
```bash
cp .env.example .env
```

#### Windows
```bash
Copy-Item .env.example .env
```
Заполните .env:
- Сгенерируйте свой API ключ на платформе [OpenRouter](https://openrouter.ai/) и установите в `OPENROUTER_API_KEY`
- Ссылку на бесплатную модель можно взять [здесь](https://openrouter.ai/models?fmt=cards&max_price=0&order=newest&output_modalities=text) либо вставьте
`openrouter/free` OpenRouter автоматически подберет бесплатную модель
- заполнить `OPENROUTER_MODEL`

```bash
APP_NAME=request-classifier
APP_ENV=local

APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO
APP_DEBUG=False

DB_USER=user
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
DB_NAME=app_db

CATEGORIES_FILE=app/core/categories.yaml

OPENROUTER_API_KEY=your-api-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=OpenRouter-request-classifier

LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=2
```
### Вариант1 - Docker
### 3 Запуск
```bash
docker compose up --build
```

### Вариант2 - локально через uv
### 3 Установка uv
```bash
pip install uv
```

### 4 Создание и активация виртуального окружения
```bash
uv venv
```
#### Linux:
```bash
source .venv/bin/activate
```

#### Windows:
```bash
.venv\Scripts\Activate.ps1
```
### 5 Установка зависимостей
```bash
uv sync
```

### 6 Запуск
```bash
uv run uvicorn app.main:app --reload
```
___
после этого интерактивная документация будет доступна по ссылке:

API: http://localhost:8000

Swagger: http://localhost:8000/docs или http://127.0.0.1:8000/docs

___
## Структура проекта
```comandline
citizen-request-classifier/
├── pyproject.toml                 # Зависимости проекта (uv)
├── README.md                      # Описание проекта и запуск
├── .env.example                   # Пример переменных окружения
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README.py
│   ├── script.py.mako
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # Точка входа FastAPI
│   │
│   │
│   ├── api.py
│   │   ├── __init__.py
│   │   ├── deps.py                # Зависимости
│   │   ├── exc_handlers           # Обработчик ошибок
│   │   ├── routes_analytics.py    # /analytics/*
│   │   └── routes_requests.py     # /request/*
│   │
│   ├── core/                      # Общие компоненты и инфраструктура
│   │   ├── __init__.py
│   │   ├── categories.yaml        # справочник доступных классов
│   │   ├── categories_loader.py   # Загрузчик категорий справочника
│   │   ├── errors.py              # Доменные исключения
│   │   └── config.py              # Конфигурация приложения (env → Settings)
│   │
│   ├── db/                        # Слой работы с БД
│   │   ├── __init__.py
│   │   ├── healthcheck.py         # Проверка статуса
│   │   ├── session.py             # Async engine и sessionmaker
│   │   └── uow.py                 # Unit of Work
│   │
│   ├── models/                    # ORM модели
│   │   ├── __init__.py
│   │   ├── base.py                # DeclarativeBase
│   │   ├── category.py            # Категории
│   │   ├── clarification.py       # Уточнения
│   │   ├── request.py             # Обращения
│   │   ├── request_category.py    # many-to-many таблица обращений-категорий
│   │
│   ├── repos/                     # Репозитории 
│   │   ├── __init__.py
│   │   ├── analytics_repo.py      # Репозиторий для сбора аналитики
│   │   ├── category_repo.py       # Доступ к категориям
│   │   ├── clarification_repo.py  # Доступ к уточнениям
│   │   └── request_repo.py        # Доступ к обращениям
│   │
│   ├── schemas/                   # Pydantic-схемы (вход/выход API)
│   │   ├── __init__.py
│   │   ├── analytics.py           # Аналитика
│   │   ├── category_seed.py       # Сид классов
│   │   ├── clarification.py       # Обращения
│   │   └── requests.py            # Запросы
│   │
│   ├── services/                  # Внешние сервисы
│   │   ├── __init__.py
│   │   ├── classifier.py       # Классификатор
│   │   ├── dataclasses.py      # Датаклассы обращения и предсказания
│   │   └── utils.py            # Схема и промпт
│   │
│   └── usecases/               # Бизнес логика 
│   │   ├── __init__.py
│   │   ├── analytics.py       # Аналитика
│   │   ├── clarification.py   # Уточнения
│   │   ├── common.py          # Сборка результата
│   │   ├── request.py         # Запросы
└── └── └── seed.py            # Заполнение справочника

```

##  Подход к классификации

Сервис использует LLM для много-меточной классификации обращений по справочнику категорий. Чтобы снизить риск некорректного формата и упростить последующую обработку, ответ запрашивается в structured output, заданном JSON Schema. Если structured output недоступен, сервис автоматически откатывается к JSON-ответу без `response_format` и повторяет попытку с повторной валидацией. 

Для повышения устойчивости запросов температура установлена = 0, используется `response-healing`. Кроме того, применяется валидация результата: возвращенные коды сверяются со списком допустимых `allowed_codes`, значения confidence проверяются на корректность, а уточняющий вопрос принимается только при наличии флага `needs_clarification`. Отдельно модель определяет наличие токсичной лексики, а при недостатке информации формулирует уточняющий вопрос.

При пустом ответе модели, временных ошибок OpenRouter уровня 5хх и ошибках, связанных с неподдержкой SO, используются retry, количество которых задано в .env.

## Примеры работы

### 1 Обычная классификация

**Запрос:**
```json
{
  "text": "Во дворе дома 12 уже неделю не вывозят мусор, контейнеры переполнены."
}
```
**Ответ:**
```json
{
  "categories": [
    { "code": "public_services" }
  ],
  "is_toxic": false,
  "clarification_question": null
}
```

### 2 Токсичный запрос

**Запрос:**
```json
{
  "text": "Вы вообще работать собираетесь или нет? Во дворе снова неделями не убирают мусор, это уже издевательство."
}
```
**Ответ:**
```json
{
  "categories": [
    { "code": "public_services" }
  ],
  "is_toxic": true,
  "clarification_question": null
}
```

### 3 Уточнение

**Уточнение:**
```json
{
  "answer": "Сломаны все скамейки"
}
```
**Результат:**
```json
{
  "id": 23,
  "raw_text": "Во дворе что-то сломано, нужно исправить",
  "categories": [],
  "is_toxic": false,
  "clarifications": [
    {
      "step": 1,
      "question": "Что именно сломано во дворе? Пожалуйста, уточните, чтобы мы могли определить категорию.",
      "answer": "Сломаны все скамейки",
      "created_at": "2026-05-05T18:42:56.277547Z"
    }
  ],
  "created_at": "2026-05-05T18:42:56.271149Z",
  "updated_at": "2026-05-05T18:44:19.294090Z"
}
```




# Tron Account Info API
Этот проект предоставляет API для получения информации об аккаунтах в сети Tron (TRX) и хранения этой информации в базе данных. Проект реализован на FastAPI и использует асинхронную работу с базой данных (SQLite) и сетью Tron.
## Функционал
- **Получение информации об аккаунте из сети Tron**: 
  - Эндпоинт `/API/fromAPI` принимает адрес аккаунта и возвращает информацию: имя (если есть), адрес, баланс TRX, bandwidth и energy.
  - Данные сохраняются в базу данных.
- **Получение истории запросов из базы данных**:
  - Эндпоинт `/API/fromDB` возвращает последние записи из базы данных с пагинацией.
## Зависимости
- Python 3.11+
- Зависимости проекта перечислены в `requirements.txt`
## Запуск приложения
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Создайте файл .env и вставьте туда свой ключ TronApi или используйте готовый (API_KEY = '2955947c-1c12-4b4e-9f9e-a31ae1b12192')
3. Запустите приложение:
   ```bash
   uvicorn src.main:app --reload
   ```
4. Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## Тестирование
### Запуск тестов
1. Установите тестовые зависимости:
   ```bash
   pip install -r requirements-dev.txt
   ```
2. Запустите тесты:
   ```bash
   pytest -v
   ```
### Описание тестов
- **Интеграционный тест**: Проверяет работу эндпоинта `/API/fromAPI` (запрос к API, сохранение в БД).
- **Юнит-тест**: Проверяет корректность записи данных в БД при вызове функции `get_info`.
## Использование API
### Получение информации об аккаунте
Запрос:
```bash
curl -X 'POST' \
  'http://localhost:8000/API/fromAPI' \
  -H 'Content-Type: application/json' \
  -d '{
  "addr": "TXYZabcdef1234567890"
}'
```
Ответ:
```json
{
  "id": 1,
  "name": "test_name",
  "adress": "TXYZabcdef1234567890",
  "bandwidth": 1000,
  "energy": 5000,
  "trx": 1000000
}
```
### Получение истории запросов
Запрос:
```bash
curl -X 'POST' \
  'http://localhost:8000/API/fromDB' \
  -H 'Content-Type: application/json' \
  -d '{
  "limit": 5,
  "offset": 0
}'
```
Ответ:
```json
[
  {
    "id": 1,
    "name": "test_name",
    "adress": "TXYZabcdef1234567890",
    "bandwidth": 1000,
    "energy": 5000,
    "trx": 1000000
  }
]
```
## Структура проекта
- `src/` - исходный код приложения
  - `main.py` - точка входа, создание приложения FastAPI
  - `api/` - модуль с API
    - `controller.py` - роутеры FastAPI
    - `view.py` - бизнес-логика
  - `database/` - работа с базой данных
    - `database.py` - подключение к БД
    - `models.py` - модели SQLModel
- `tests/` - тесты
  - `test_integration.py` - интеграционные тесты
  - `test_unit.py` - юнит-тесты
  - `conftest.py` - фикстуры pytest
- `requirements.txt` - зависимости для запуска

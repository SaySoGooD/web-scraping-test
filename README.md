# Тестовое задание для позиции Python Junior Developer

## Описание

Python-парсер таблицы testDB.users из phpMyAdmin.

## Структура проекта

```
WebTest/<br>
├── logs/                      # Логи выполнения (автоматически создаётся)<br>
├── src/<br>
│   ├── http/                  # HTTP-клиенты и работа с API<br>
│   │   ├── pma_client.py      # Основная логика работы с phpMyAdmin<br>
│   │   └── request_handler.py # Базовый HTTP-клиент<br>
│   ├── utils/                 # Вспомогательные утилиты<br>
│   │   ├── config_loader.py   # Загрузка конфигурации<br>
│   │   ├── logger.py          # Настройка логгирования<br>
│   │   ├── parsers/           # Парсеры HTML/ответов<br>
│   │   └── printer.py         # Форматированный вывод<br>
│   ├── models.py              # Data-классы<br>
│   └── main.py                # Точка входа<br>
├── config.ini                 # Конфигурационные параметры<br>
└── README.md                  # Этот файл
```

## Требования

- Python 3.8+
- Зависимости:
  ```
  requests>=2.25.1
  beautifulsoup4>=4.9.3
  ```

### **Установка и запуск (Windows)**

#### 1. Установка Python
- Скачайте Python 3.8+ с [официального сайта](https://www.python.org/downloads/)
- **Важно:** При установке отметьте галочку **"Add Python to PATH"**  
- Проверьте установку в командной строке:
  ```bash
  python --version
  # или
  python3 --version
  ```

#### 2. Настройка виртуального окружения
- Откройте командную строку в папке проекта:
  ```bash
  cd C:\путь_к_проекту
  ```
- Создайте и активируйте окружение:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
  *(В PowerShell используйте `.\venv\Scripts\Activate.ps1`)*

#### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

## Использование

1. Настройте параметры в `config.ini`:
   ```ini
   [auth]
   username = логин
   password = пароль
   
   [db]
   base_url = http://185.244.219.162/phpmyadmin
   database = testDB
   table = users
   ```

2. Запустите скрипт:
   ```bash
   python -m src.main
   ```

## Пример вывода

```
2025-08-04 05:12:52 - __main__ - INFO - Запуск приложения
2025-08-04 05:12:52 - __main__ - INFO - Попытка аутентификации
2025-08-04 05:12:53 - __main__ - INFO - Аутентификация успешна
2025-08-04 05:12:53 - __main__ - INFO - Запрос данных таблицы users
2025-08-04 05:12:53 - __main__ - SUCCESS - Получено 4 записей

Структура таблицы [testDB.users]:
Столбцы: ['id', 'name']

Строк: 5
1. {'id': '4', 'name': 'Алексей'}
2. {'id': '3', 'name': 'Василий'}
3. {'id': '2', 'name': 'Пётр'}
4. {'id': '1', 'name': 'Иван'}
```

## Контакты

- Email: k.jczk@mail.ru
- Telegram: @saysogood

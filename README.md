# Scrapy Parser PEP

Асинхронный парсер документов PEP (Python Enhancement Proposals) на базе фреймворка Scrapy.

## 📋 О проекте

Парсер собирает информацию о всех документах PEP с сайта `https://peps.python.org/`. Результаты сохраняются в двух CSV-файлах:

1. **pep_ДатаВремя.csv** — список всех PEP (номер, название, статус)
2. **status_summary_ДатаВремя.csv** — сводка по статусам (статус, количество, Total)

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/badroom1904/scrapy_parser_pep.git
cd scrapy_parser_pep

2. Создание и активация виртуального окружения

python -m venv venv
venv\Scripts\activate

3. Установка зависимостей

pip install -r requirements.txt

4.Использование

scrapy crawl pep

4.1 Запуск с дополнительными опциями

# Запуск с очисткой кеша
scrapy crawl pep -s HTTPCACHE_ENABLED=False

# Запуск с логированием DEBUG (для отладки)
scrapy crawl pep -s LOG_LEVEL=DEBUG

5.Результаты

После выполнения парсинга в папке results/ появляются два файла:

1.pep_2026-06-30T12-00-00.csv
2.status_summary_2026-06-30_12-00-00.csv

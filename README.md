# goodrsearch

Django приложение для полнотекстового поиска по содержимому офисных документов, хранящихся на Google Диске.

## Возможности
- Индексация документов Google Drive (PDF, DOCX, PPTX, XLSX и др.)
- Поиск по содержимому с морфологической нормализацией (pymorphy3)
- Поддержка русского языка
- Веб-интерфейс на Django
- Пагинация результатов поиска
- Автоматическая индексация через cron (django-crontab)

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/cathxrsys/goodrsearch.git
   cd goodrsearch
   ```
2. Установите зависимости:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt
   ```
3. Настройте Google API credentials (см. папку `credentials/`).
4. Проведите миграции:
   ```bash
   python manage.py migrate
   ```
5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## Использование
- Откройте веб-интерфейс по адресу http://localhost:8000
- Введите поисковый запрос для поиска по документам

## Автоматическая индексация
- Используется django-crontab для периодического запуска задачи индексации файлов Google Drive.
- Настройка расписания в `settings.py` (CRONJOBS).

## Лицензия
MIT
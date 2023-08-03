import os

from celery import Celery

# Установка переменной окружения для работы с Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_ozon_parser.settings")

app = Celery("django_ozon_parser")

# Загрузка настроек celery из файла settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение и регистрация задач (tasks) из всех приложений Django
app.autodiscover_tasks()

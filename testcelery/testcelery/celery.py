from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите значение по умолчанию для переменной окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcelery.settings')

app = Celery('testcelery')

# Используйте строку подключения для брокера из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите модули задач из всех зарегистрированных приложений Django
app.autodiscover_tasks()

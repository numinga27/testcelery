from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную среды по умолчанию для настроек Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcelery.settings')

app = Celery('testcelery')

# Используйте строку URL-адреса для настройки брокера (например RabbitMQ, Redis, Amazon SQS, и т.д.)
app.conf.broker_url = 'redis://localhost:6379/0'

# Опционально: сконфигурируйте Celery так, чтобы он использовал настройки проекта Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите задачу модулей из всех зарегистрированных приложений Django.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
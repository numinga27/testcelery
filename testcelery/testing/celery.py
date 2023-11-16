# В файле celery.py или в конфигурационном файле для Celery

from celery import Celery
from celery.schedules import crontab

app = Celery('testcelery')

app.conf.beat_schedule = {
    'send-request-every-minute': {
        'task': 'path.to.send_request_task',  # замените на путь к вашей задаче
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
    # Другие периодические задачи здесь…
}


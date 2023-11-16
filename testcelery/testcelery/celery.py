from celery import Celery
from celery.schedules import crontab

# app = Celery('testcelery')
app = Celery('testcelery', broker='redis://localhost:6379/0')
app.conf.beat_schedule = {
    'send-request-every-minute': {
        'task': 'path.to.send_request_task',  # замените на путь к вашей задаче
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
    # Другие периодические задачи здесь…
}



from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "reservation_tasks",
    broker="redis://localhost:6379/1", 
    backend="redis://localhost:6379/1",
)

celery_app.conf.task_routes = {
    "app.tasks.process_reservation_queue": {"queue": "reservation_queue"}
}

celery_app.conf.beat_schedule = {
    "process-reservation-queue-every-minute": {
        "task": "app.tasks.process_reservation_queue",
        "schedule": crontab(minute="*"),  # اجرای هر ۱ دقیقه یک‌بار
    }
}


# celery -A app.celery_worker.celery_app worker --loglevel=info
# celery -A app.celery_worker.celery_app beat --loglevel=info


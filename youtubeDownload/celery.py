import os
from datetime import timedelta
from .settings import BASE_DIR


from celery import Celery
from celery.schedules import crontab

from celery.utils.log import get_task_logger
logger = get_task_logger("tasks")

from post_request_task.task import PostRequestTask

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtubeDownload.settings')

app = Celery('youtubeDownload', task_cls=PostRequestTask, backend='database')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



@app.task(bind=True)
def remove_logs(self):
    return os.system("rm -rf %s/logs/*" % BASE_DIR)



app.conf.beat_schedule = {
    "remove logs": {
        "task":"youtubeDownload.celery.remove_logs",
        "schedule": crontab(hour="*/12", minute=0)
    },

    "statistique videos": {
        "task": "videos.tasks.stats_all_videos",
        "schedule": crontab(hour="*/3", minute=0)
    },

    # "statistique channels": {
    #     "task": "videos.tasks.stats_all_channels",
    #     "schedule": crontab(hour="*/4", minute=15)
    # },

    "remove files": {
        "task": "app.tasks.delete_video_downloaded",
        "schedule": crontab(hour="*/4", minute=15)
    },

    # "facials to bdd": {
    #     "task": "facials.tasks.VideoToFace",
    #     "schedule": crontab(hour="*", minute="*/32")
    # },

    "update videos channels": {
        "task": "videos.tasks.update_channels",
        "schedule": crontab(hour="*/2", minute=15)
    },

}


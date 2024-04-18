# app/tasks.py
import os, sys, re
from app.models import Downloaded
from app.libraries import DownloaderRedis
from videos.models import Videos
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.timezone import utc

from videos.tasks import videos_infos

from youtubeDownload.celery import app

import logging
logger = logging.getLogger("tasks")




@app.task
def update_downloaded(downloaded_id, status, percent_float, downloaded_bytes, total_bytes):
    down = Downloaded.objects.filter(id=downloaded_id).first()
    if down is None:
        logger.warning("Down Not Found")
        return "Down Not Found"

    down.percent = percent_float
    down.downloaded_bytes = downloaded_bytes
    down.total_bytes = total_bytes

    if status=="downloading": down.status = Downloaded.Status.DOWNLOADING
    if status=="converting": down.status = Downloaded.Status.CONVERTING
    if status=="finished": down.status = Downloaded.Status.FINISHED
    down.save()
    return






@app.task
def delete_video_downloaded(nb_hours=3, Downloaded_id=None):
    now = datetime.utcnow().replace(tzinfo=utc)
    deltaTime = now - timedelta(hours=nb_hours)
    downs = Downloaded.objects.filter(status__in = [Downloaded.Status.FINISHED, Downloaded.Status.DELETING], 
        created_at__lte=deltaTime).all()
    
    for down in downs:
        if down.status != Downloaded.Status.DELETING:
            down.status = Downloaded.Status.DELETING
            down.save()
        
        try:
            os.remove(down.path)
            logger.debug("File %s Deleted" % down.url_id)
        except Exception as e:
            sys.stderr.write(e)
            logger.warning("File %s Not Deleted - %s" % (down.url_id, e))
        finally:pass

        down.status = Downloaded.Status.DELETED
        down.save()
        
    return





@app.task
def download_video_none():
    downs = Downloaded.objects.filter(video__isnull=True).all()
    for down in downs:
        video = Videos.objects.filter(url_id=down.url_id)
        if video.count()==0:
            # videos_infos.apply_async((down.id, down.url, down.url_id,"odnoklassniki"))
            continue
        down.video = video.first()
        down.save()
    return









@app.task
def download_file(downloaded_id):
    try:
        downloaded = Downloaded.objects.get(id=downloaded_id)
        d = DownloaderRedis(downloaded_id)
        d.download()
    except Downloaded.DoesNotExist:
        logger.error("Download %s Does not exist" % downloaded_id)
        return "Download %s Does not exist" % downloaded_id








@app.task
def resume_downloads():
    try:
        downs = Downloaded.objects.exclude(status__in=Downloaded.Status.FINISHED).all()

    except Exception as e:
        logger.error("Resume download - %s" % e)
        return "Resume download - %s" % e
# vocals/tasks.py
from django.core.exceptions import *
from post_request_task.task import shared_task
from datetime import datetime
from app.models import Downloaded
from videos.models import Videos
from vocals.models import Subtitles
from vocals.libraries import VocalLib

from youtubeDownload.celery import app

import logging
logger = logging.getLogger("tasks")


## Tasks Load Video file
## Cut audio by phrases

@app.task
def AudioToDb(url_id=None):
	if not url_id:
		from random import choice
		ids = Subtitles.objects.all().values("video_id").distinct()
		ids = list(map(lambda d:d['video_id'], ids))
		url_ids = Videos.objects.exclude(id__in=ids).values("url_id").distinct()
		url_ids = list(map(lambda d:d['url_id'], url_ids))
		url_id = choice(url_ids)


	try:
		url = "https://www.youtube.com/watch?v=%s" % url_id
		down = VocalLib.download(url)
		if not down:
			return

		audio_file, srt_file = down

		Phrases_dict = VocalLib.srtDict(srt_file)
		Subs_db = VocalLib.SrtToBdd(url_id, Phrases_dict)
		VocalLib.AudioToBdd(audio_file, Phrases_dict, Subs_db)

		logger.info("AudioToDb Reussi")
	except Exception as e:
		logger.error(e)
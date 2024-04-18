# facials/tasks.py
import os, sys
from django.core.exceptions import *
from celery.exceptions import *

from post_request_task.task import shared_task
from datetime import time
from facials.libraries import FacialLib
from videos.models import Videos, Channels
from facials.models import *

from youtubeDownload.celery import app

import logging
logger = logging.getLogger("tasks")


## Tasks Load Video file
## Search faces & Save Sequences

@app.task(soft_time_limit=(44*60), time_limit=(45*60))
def VideoToFace(video_id=None):
	if not video_id:
		from random import choice
		ids = Faces.objects.all().values("video_id").distinct()
		ids = list(map(lambda d:d['video_id'], ids))
		video_ids = Videos.objects.filter(duration__lte=time(minute=8)).exclude(id__in=ids).values("id").distinct()
		video_ids = list(map(lambda d:d['id'], video_ids))
		if len(video_ids)==0:
			logger.warning("Aucune nouvelles vidéos")
			return "Aucunes vidéos"

		video_id = choice(video_ids)

	else:
		ids = Faces.objects.all().values("video_id").distinct()
		ids = list(map(lambda d:d['video_id'], ids))
		if video_id in ids:
			logger.warning("Vidéo déjà traité")
			return "Vidéo déjà traité"


	try:
		video = Videos.objects.get(id=video_id)
	except Videos.DoesNotExist:
		logger.error("Video %s Not Found" % video_id)
		return "Video %s Not Found" % video_id


	now = datetime.now()
		
	logger.debug("Started - %s" % datetime.now())
	logger.debug(video.title)

	logger.debug("%s - Download" % (datetime.now() - now))
	video_file = FacialLib.download(video.url)


	try:

		logger.debug("%s - Extract Faces" % (datetime.now() - now))
		face_dbs, nbNewFaces = FacialLib.extractFaces(video_file, video)
		logger.debug("%s - %d Faces - %d New" % ((datetime.now() - now), len(face_dbs), nbNewFaces))

		removeFile.apply_async((video_file,))

		# face_dbs = Faces.objects.filter(video=video).all()

		logger.debug("%s - Extract Sequences" % (datetime.now() - now))
		sequence_dbs = FacialLib.extractSequences(face_dbs, video)
		logger.debug("%s - %d Sequences" % ((datetime.now() - now), len(sequence_dbs)))

		# sequence_dbs = Sequences.objects.filter(video=video).all()

		logger.debug("%s - Remove Faces not in Sequences" % (datetime.now() - now))
		nbFaces = FacialLib.removeFacesSequences(video, face_dbs, sequence_dbs)
		logger.debug("%s - %d (%.2f%%) Faces deleted" % ((datetime.now() - now), nbFaces, (nbFaces*100/len(face_dbs))))


		logger.debug("%s - Remove Short Sequences" % (datetime.now() - now))
		nbSeq, nbFaces = FacialLib.removeSmallSequences(sequence_dbs)
		logger.debug("%s - %d (%.2f%%) Sequences deleted" % ((datetime.now() - now), nbSeq, (nbSeq*100/len(sequence_dbs))))


		logger.debug("%s - Copy Tags" % (datetime.now() - now))
		nbTags = FacialLib.copyTags(video)
		logger.debug("%s - %d New Tags" % ((datetime.now() - now), nbTags))

		removeWorstTags.apply_async((video.channel.channel_id, ))
		
		logger.info("VideoToFace %s Terminate in %s" % (youtube_id, (datetime.now() - now)))



	except SoftTimeLimitExceeded:
		logger.warning("VideoToFace %s SoftTimeLimitExceeded %s" % (youtube_id, (datetime.now() - now)))
		removeSequences.apply_async((video,))
		removeFile.apply_async((video_file,))
		return "VideoToFace %s SoftTimeLimitExceeded %s" % (youtube_id, (datetime.now() - now))
	except TimeLimitExceeded:
		logger.warning("VideoToFace %s TimeLimitExceeded %s" % (youtube_id, (datetime.now() - now)))
		removeSequences.apply_async((video,))
		removeFile.apply_async((video_file,))
		return "VideoToFace %s TimeLimitExceeded %s" % (youtube_id, (datetime.now() - now))
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return str(e)
	except Exception as e:
		logger.warning(str(e))
		removeSequences.apply_async((video,))
		removeFile.apply_async((video_file,))
		return str(e)





@app.task
def removeSequences(video):
	try:
		FacialLib.removeSequences(video)
		logger.debug("Séquences Removed")
	except Exception as e:
		logger.error("Séquences Removed Error : %s" % e)
		pass







@app.task
def removeFile(video_file):
	try:
		os.remove(video_file)
		logger.debug("Video File Removed")
	except Exception as e:
		logger.error("Remove Error : %s" % e)
		pass









@app.task
def removeWorstTags(channel_id=None):
	if channel_id is None:
		from random import choice
		channel_ids = Channels.objects.all().values_list("channel_id").distinct()
		channel_ids = list(map(lambda c:c[0], channel_ids))
		channel_id = choice(channel_ids)

	try:
		channel = Channels.objects.get(channel_id=channel_id)
	except Channels.DoesNotExist:return False

	tags_count = {}
	for video in channel.videos.all():
		for tag in video.tags.all():
			if tag.value not in tags_count.keys():
				tags_count[tag.value] = 0
			tags_count[tag.value] += 1



	tags_count_sorted = dict(sorted(tags_count.items(), key=lambda item: item[1], reverse=True))
	
	nbVideos = channel.videos.count()
	max_number = 2
	max_unshow = max_number if nbVideos>max_number else nbVideos
	tags_show = []
	tags_unshow = []
	for tag_value, tag_number in tags_count_sorted.items():
		if tag_number<=max_number:
			tags_unshow.append(tag_value)
		else:
			tags_show.append(tag_value)

	Tags.objects.filter(value__in=tags_unshow).update(show=False)
	Tags.objects.filter(value__in=tags_show).update(show=True)

	nbUnshow = Tags.objects.filter(value__in=tags_unshow).count()
	nbShow = Tags.objects.filter(value__in=tags_show).count()

	logger.debug("%d tags unshowed %d showed" % (nbUnshow, nbShow))









@app.task
def removeAllWorstTags():

	tags_count = {}
	for channel in Channels.objects.all():
		for video in channel.videos.all():
			for tag in video.tags.all():
				if tag.value not in tags_count.keys():
					tags_count[tag.value] = 0
				tags_count[tag.value] += 1

	

	tags_count_sorted = dict(sorted(tags_count.items(), key=lambda item: item[1], reverse=True))
	
	tags_show = []
	tags_unshow = []
	for tag_value, tag_number in tags_count_sorted.items():
		if tag_number<=2:
			tags_unshow.append(tag_value)
		else:
			tags_show.append(tag_value)

	Tags.objects.filter(value__in=tags_unshow).update(show=False)
	Tags.objects.filter(value__in=tags_show).update(show=True)

	nbUnshow = Tags.objects.filter(value__in=tags_unshow).count()
	nbShow = Tags.objects.filter(value__in=tags_show).count()

	logger.debug("%d tags unshowed %d showed" % (nbUnshow, nbShow))




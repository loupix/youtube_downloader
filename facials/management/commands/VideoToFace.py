import sys
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from facials.libraries import FacialLib
from videos.models import *
from facials.models import *
from facials.tasks import *


class Command(BaseCommand):
	help = 'Create spectre and save in database'
	_now = datetime.now()

	def handle(self, *args, **options):

		from random import choice
		ids = Faces.objects.all().values("video_id").distinct()
		ids = list(map(lambda d:d['video_id'], ids))
		youtube_ids = Videos.objects.filter(duration__lte=time(minute=8)).exclude(id__in=ids).values("youtube_id").distinct()
		youtube_ids = list(map(lambda d:d['youtube_id'], youtube_ids))
		if len(youtube_ids)==0:
			logger.warning("Aucune nouvelles vidéos")
			return "Aucunes vidéos"

		youtube_id = choice(youtube_ids)


		# ann = [[298, 84, 78, 78],[298, 84, 78, 78],[298, 84, 78, 78],[298, 84, 78, 78]]
		# print(ann)
		# print([298, 84, 78, 78] in ann)

		try:
			video = Videos.objects.get(youtube_id=youtube_id)
		except Videos.DoesNotExist:
			logger.error("Video %s Not Found" % youtube_id)
			return "Video %s Not Found" % youtube_id

		print("Started - %s" % datetime.now())
		print("%s - %s" % (video.title, video.duration))

		print("%s - Download" % (datetime.now() - self._now))
		video_file = FacialLib.download(video)

		print("%s - Extract Faces" % (datetime.now() - self._now))
		face_dbs, nbNewFaces = FacialLib.extractFaces(video_file, video)
		print("%s - %d Faces - %d New" % ((datetime.now() - self._now), len(face_dbs), nbNewFaces))

		removeFile.apply_async((video_file,))

		# face_dbs = Faces.objects.filter(video=video).all()

		print("%s - Extract Sequences" % (datetime.now() - self._now))
		sequence_dbs = FacialLib.extractSequences(face_dbs, video)
		print("%s - %d Sequences" % ((datetime.now() - self._now), len(sequence_dbs)))

		# sequence_dbs = Sequences.objects.filter(video=video).all()

		print("%s - Remove Faces not in Sequences" % (datetime.now() - self._now))
		nbFaces = FacialLib.removeFacesSequences(video, face_dbs, sequence_dbs)
		print("%s - %d (%.2f%%) Faces deleted" % ((datetime.now() - self._now), nbFaces, (nbFaces*100/len(face_dbs))))


		print("%s - Remove Short Sequences" % (datetime.now() - self._now))
		nbSeq, nbFaces = FacialLib.removeSmallSequences(sequence_dbs)
		print("%s - %d (%.2f%%) Sequences deleted" % ((datetime.now() - self._now), nbSeq, (nbSeq*100/len(sequence_dbs))))


		print("%s - Copy Tags" % (datetime.now() - self._now))
		nbTags = FacialLib.copyTags(video)
		print("%s - %d New Tags" % ((datetime.now() - self._now), nbTags))

		removeWorstTags.apply_async((video.channel.channel_id, ))


		print("%s - Terminer" % (datetime.now() - self._now))
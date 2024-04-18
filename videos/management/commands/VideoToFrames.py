from django.core.management.base import BaseCommand, CommandError

from videos.models import *
from videos.libraries import *
from facials.tasks import *


class Command(BaseCommand):
	help = 'Extract Frames from videos'

	def add_arguments(self , parser):
		parser.add_argument('video_id' , nargs='+' , type=str, help='evid')

	def handle(self, *args, **options):

		video_id =  options['video_id']
		if len(video_id)>0:
			video_id = video_id[0]
		else:
			from random import choice
			ids = Frames.objects.all().values("video_id").distinct()
			ids = list(map(lambda d:d['video_id'], ids))
			video_ids = Videos.objects.filter(duration__lte=time(minute=8)).exclude(id__in=ids).values("video_id").distinct()
			video_ids = list(map(lambda d:d['video_id'], video_ids))
			if len(video_ids)==0:
				logger.warning("Aucune nouvelles vidéos")
				return "Aucunes vidéos"

			video_id = choice(video_ids)

		now = datetime.now()


		try:
			video = Videos.objects.get(id=video_id)
		except Videos.DoesNotExist:
			logger.error("Video %s Not Found" % video_id)
			return "Video %s Not Found" % video_id

		print("Started - %s" % datetime.now())
		print("%s - %s" % (video.title, video.duration))

		print("%s - Download" % (datetime.now() - now))
		video_file = FrameLib.download(video.url)

		print("%s - Extract Frames" % (datetime.now() - now))
		nbFrames, nbNewFrames = FrameLib.extractFrames(video_file, video)
		print("%s - %d Frames - %d New" % ((datetime.now() - now), nbFrames, nbNewFrames))

		removeFile.apply_async((video_file,))


		return


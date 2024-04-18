# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from googleapiclient.discovery import build

import html
import youtube_dl
from datetime import datetime
from django.utils import timezone
from videos.models import Videos

import random, string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Command(BaseCommand):
	help = 'Closes the speazcified poll for voting'

	def handle(self, *args, **options):
		import pprint
		url = "https://www.youtube.com/watch?v=OBazwQuur1M"
		# url = "https://ok.ru/video/54401501764"
		# url = "https://www.dailymotion.com/video/xn5lx"

		url_id = "OBazwQuur1M"
		ydl_opts = {
			# 'outtmpl': os.path.join(self._directory, '%(title)s.%(ext)s'),
			'nocheckcertificate': True,
			'quiet': True,
			'noplaylist': True,
			'nopart': False,
			"simulate": True,
			# 'ignoreerrors': True,
			'format': "best",
			# 'logger': MyLogger(self, self.socket, self.downloaded),
			# 'progress_hooks': [self._my_hook],
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.cache.remove()
			infos = ydl.extract_info(url, download=False)

		pprint.pprint(infos)


		# infos['description'] = html.unescape(infos['description'])
		# infos['description'] = infos['description'].encode('ascii', 'xmlcharrefreplace').decode("utf-8")

		# infos['upload_date'] = datetime.strptime(infos['upload_date'],"%Y%m%d").replace(tzinfo=timezone.utc)
		# infos['duration'] = datetime.utcfromtimestamp(infos['duration']).time()

		# website = Videos.Website.TWITTER
		# video = Videos(url=url, url_id=url_id, website=website, video_id=id_generator(14),
		# 	title=infos['title'], description=infos['description'],
		# 	duration=infos['duration'], published_at=infos['upload_date'])
		# video.save()


		return



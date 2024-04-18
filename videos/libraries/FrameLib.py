import json, sys, re, os, io
from datetime import datetime, timedelta, date
from math import *
import yt_dlp as youtube_dl
import cv2

from youtubeDownload.settings import BASE_DIR
from videos.models import *
from django.db import transaction
from facials.models import *

import logging
logger = logging.getLogger("libraries")

VIDEO_DIR = os.path.join(str(BASE_DIR),"tmp", "videos")

class FrameLib:

	_now = datetime.now()

	if not os.path.exists(VIDEO_DIR):os.makedirs(VIDEO_DIR)







	
	"""
	Download Video File
	:param  String url
	:return String video_file

	:throws Throwable
	"""
	@staticmethod
	def download(url) -> str:
		try:
			ydl_opts = {
				'outtmpl': os.path.join(VIDEO_DIR, '%(id)s_%(format_id)s.%(ext)s'),
				'nocheckcertificate': True,
				'quiet': True,
				'noplaylist': True,
				'nopart': False,

				# "simulate": True,
				# 'ignoreerrors': True,
				'format': "worstvideo[ext=webm]",
				# 'logger': MyLogger(self, self.socket, self.downloaded),
				# 'progress_hooks': [self._my_hook],
				# 'print_json': True
			}


			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.cache.remove()
				info_dict = ydl.extract_info(url, download=False)
				ydl.prepare_filename(info_dict)
				ydl.download([url])

			video_file = os.path.join(VIDEO_DIR, "%s_%s.%s" % (info_dict['id'], info_dict['format_id'], info_dict['ext']))
			
			return video_file

		except youtube_dl.utils.DownloadError as e:
			raise Exception(str(e))
		except Exception as e:
			raise Exception(str(e))










	"""
		Extract frames & Save BDD
		:param  String video_file
		:param  Videos video
		:return Integer nbFrames
		:return Integer nbNewFrames

		:throws Throwable
	"""
	@staticmethod
	def extractFrames(video_file, video, nb_frames=20):

		vidcap = cv2.VideoCapture(video_file)
		fps = vidcap.get(cv2.CAP_PROP_FPS)

		width  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
		total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

		frames_step = total_frames/float(nb_frames)

		frame_dbs = []
		frame_to_db = []


		for i in range(nb_frames):
			vidcap.set(1,i*frames_step)

			timestamp = datetime.utcfromtimestamp(vidcap.get(cv2.CAP_PROP_POS_MSEC)/1000)
			timestamp = timestamp.time()

			success,image = vidcap.read()
			if not success:continue

			image_bytes = cv2.imencode('.jpg', image)[1].tobytes()

			try:
				frame = Frames.objects.get(video=video, time_at=timestamp, width=width, height=height)
			except Frames.DoesNotExist:
				frame = Frames(video=video, time_at=timestamp, width=width, height=height, content=image_bytes)
				frame_to_db.append(frame)
			frame_dbs.append(frame)

		with transaction.atomic():
			for frame in frame_to_db:frame.save()

		vidcap.release()

		return len(frame_dbs), len(frame_to_db)










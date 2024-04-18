from django.core.management.base import BaseCommand, CommandError
from youtube.models import *
from youtube.libraries import YoutubeApi, YoutubeCrud
from googleapiclient.discovery import build

# import os
# os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')
# import vlc

import cv2, pafy

class Command(BaseCommand):
	help = 'Closes the speazcified poll for voting'

	def handle(self, *args, **options):
		import pprint
		youtube_id = "PMZaMgyYYcU"

		url   = "https://www.youtube.com/watch?v=%s" % youtube_id
		video = pafy.new(url)
		best  = video.getbest(preftype="webm")

		print(best)

		capture = cv2.VideoCapture(best.url)
		check, frame = capture.read()
		print (check, frame)

		cv2.imshow('frame',frame)
		cv2.waitKey(10)

		capture.release()
		cv2.destroyAllWindows()

		# media = vlc.MediaPlayer(best.url)
		# media.play()

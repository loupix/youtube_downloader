import json, sys, re, os, io
from datetime import datetime

import yt_dlp as youtube_dl
import webvtt
import ffmpeg

from youtubeDownload.settings import BASE_DIR
from videos.models import Videos
from vocals.models import *

from opensoundscape.audio import Audio
from opensoundscape.spectrogram import Spectrogram
from pathlib import Path

AUDIO_DIR = os.path.join(BASE_DIR,"/tmp/audios/")
SRT_DIR = os.path.join(BASE_DIR,"/tmp/srt/")


class VocalLib:


	_now = datetime.now()

	if not os.path.exists(AUDIO_DIR):os.makedirs(AUDIO_DIR)
	if not os.path.exists(SRT_DIR):os.makedirs(SRT_DIR)

	"""
		Download Audio File
		:param  String url
		:return Boolean

		:throws Throwable
	"""

	@staticmethod
	def download(youtube_id):
		url = "https://www.youtube.com/watch?v=%s" % youtube_id
		try:

			ydl_opts = {
				'outtmpl': AUDIO_DIR+'%(title)s.%(ext)s',
				'nocheckcertificate': True,
				'quiet': True,
				'noplaylist': True,
				'nopart': False,

				"withsubtitle": True,
				"writeautomaticsub": True,
				'subtitleslangs': ['fr'],

				# "simulate": True,
				# 'ignoreerrors': True,
				'format': "bestaudio",
				# 'logger': MyLogger(self, self.socket, self.downloaded),
				# 'progress_hooks': [self._my_hook],
				# 'print_json': True
			}



			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.cache.remove()
				info_dict = ydl.extract_info(url, download=False)
				ydl.prepare_filename(info_dict)
				ydl.download([url])

			audio_file = "%s/%s.%s" % (AUDIO_DIR, info_dict['title'], info_dict['ext'])
			srt_file = "%s/%s.fr.vtt" % (AUDIO_DIR, info_dict['title'])

			if os.path.exists(srt_file):
				return (audio_file, srt_file)
			return False


		except youtube_dl.utils.DownloadError as e:
			raise Exception(e)
		except Exception as e:
			raise Exception(e)







	"""
		Srt File to Dictionnarie
		:param  String srt_file
		:return Dict phrases_dict
	"""

	@staticmethod
	def srtDict(srt_file):
		vtt = webvtt.read(srt_file)
		Excepts = ['[Musique]', '[Applaudissements]']
		Phrases_dict = {}

		previous = None
		for caption in vtt:
			lines = caption.text.strip().splitlines()
			for line in lines:
				if line in Excepts:continue

				if line not in Phrases_dict.keys():
					Phrases_dict[line] = []
					Phrases_dict[line].append([caption.start, caption.end])

				elif line not in previous:
					Phrases_dict[line].append([caption.start, caption.end])


			previous = lines
		return Phrases_dict







	"""
		Srt Dict to Database
		:param  String youtube_id 
		:param  Dict Phrases_dict 
		:return DictOfObj srt_obj
	"""
	@staticmethod
	def SrtToBdd(youtube_id, Phrases_dict={}):


		try:
			video_db = Videos.objects.get(youtube_id=youtube_id)
		except Videos.DoesNotExist as e:
			raise Exception(e)


		Phrases_db = {}
		Subs_db = {}
		for p, times in Phrases_dict.items():
			if p in Phrases_db.keys():phrase = Phrases_db[p]
			else:
				# Save Phrases
				try:
					phrase = Phrases.objects.get(value=p)
				except Phrases.DoesNotExist:
					phrase = Phrases(value=p)
					phrase.save()
				Phrases_db[p] = phrase

			Subs_db[p] = []
			for time in times:
				start, end = time


				start = datetime.strptime(start, "%H:%M:%S.%f")
				end = datetime.strptime(end, "%H:%M:%S.%f")
				duration = end-start


				# Save Subtitles
				try:
					sub = Subtitles.objects.get(video=video_db, phrase=phrase,
						startTime=start, endTime=end)
				except Subtitles.DoesNotExist:
					sub = Subtitles(video=video_db, phrase=phrase,
						startTime=start, endTime=end)
					sub.save()
				Subs_db[p].append(sub)

		return Subs_db








	"""
		Audio Files & Picture to Database
		:param  String audio_file 
		:param  Dict Phrases_dict 
		:param DictOfObj srt_obj
		:return Boolean
	"""
	@staticmethod
	def AudioToBdd(audio_file, Phrases_dict, Subs_db):
		epoch_time = datetime(1900, 1, 1)
		i=0
		nPhrases = len(Phrases_dict.keys())
		for phrase, times in Phrases_dict.items():

			if not os.path.exists("%s/%s" % (SRT_DIR, phrase)):
				os.makedirs(("%s/%s" % (SRT_DIR, phrase)))
			j=0
			sub_obj = Subs_db[phrase]
			for start, end in times:

				start = (datetime.strptime(start, "%H:%M:%S.%f") - epoch_time).total_seconds() * 1000
				end = (datetime.strptime(end, "%H:%M:%S.%f") - epoch_time).total_seconds() * 1000

				(
					ffmpeg
					.input(audio_file)
					.filter('atrim', start=str(start)+"ms", end=str(end)+"ms")
					.output("%s/%s/%d.wav" % (SRT_DIR, phrase, j))
					.run(quiet=True)
				)


				#Read & Save file
				with open("%s/%s/%d.wav" % (SRT_DIR, phrase, j), "rb") as fh:
					content = fh.read()
					# Save File
					try:
						file = Files.objects.get(subtitle = sub_obj[j])
					except Files.DoesNotExist:
						file = Files(content=content, subtitle=sub_obj[j])
						file.save()
					fh.close()



				# Create spectre

				# Settings
				image_shape = (224, 224) #(height, width) not (width, height)

				# Load audio file as Audio object
				audio = Audio.from_file("%s/%s/%d.wav" % (SRT_DIR, phrase, j))

				# Create Spectrogram object from Audio object
				spectrogram = Spectrogram.from_audio(audio)

				# Convert Spectrogram object to Python Imaging Library (PIL) Image
				
				image = spectrogram.to_image(shape=image_shape,invert=True)

				img_byte_arr = io.BytesIO()
				image.save(img_byte_arr, format='PNG')
				content = img_byte_arr.getvalue()

				# Save Spectogram
				phraseObj = Phrases.objects.get(value=phrase)
				try:
					spectre = Spectres.objects.get(subtitle = sub_obj[j])
				except Spectres.DoesNotExist:
					spectre = Spectres(content=content, subtitle=sub_obj[j], phrase=phraseObj)
					spectre.save()

				image.close()
				os.unlink("%s/%s/%d.wav" % (SRT_DIR, phrase, j))
				
				j+=1

			os.rmdir("%s/%s" % (SRT_DIR, phrase))
			i+=1
			percent = (i/nPhrases)*100
			sys.stdout.write("\r%s - %d / %d - %.2f%%" % ((datetime.now() - VocalLib._now), i, nPhrases, percent))
		return True




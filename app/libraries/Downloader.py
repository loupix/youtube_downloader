from django.conf import settings

import threading, queue
import multiprocessing

import yt_dlp as youtube_dl
from datetime import datetime

NB_CORE = multiprocessing.cpu_count()



class MyLogger(object):
	def debug(self, msg):
		print(msg)
		pass

	def warning(self, msg):
		sys.stderr.write(msg)
		pass

	def error(self, msg):
		sys.stderr.write(msg)



class Downloader(threading.Thread):

	_directory = str(settings.BASE_DIR)+"/app/"+settings.STATIC_URL+"downloads/"
	_formatOut = 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/mp4'

	def __init__(self, youtube_id, Dowloaded, handleDownload=None):
		threading.Thread.__init__(self)
		self._stopEvent = threading.Event()
		self._status_queue = queue.Queue()

		self.youtube_id = youtube_id
		self.downloaded = Downloaded
		self.handleDownload = handleDownload


	def wait_for_exc_info(self):
		return self.__status_queue.get()

	def join_with_exception(self):
		ex_info = self.wait_for_exc_info()
		if ex_info is None:
			return
		else:
			raise ex_info


	def my_hook(self, d):
		id = d['filename'].split(".")[0]
		file = id.split("\\")[-1]
		if d['status'] == 'downloading':
			self.downloaded.status = self.downloaded.Status.DOWNLOADING
		elif d['status'] == 'finished':
			self.downloaded.status = self.downloaded.Status.FINISHED
		elif d['status'] == 'error':
			self.downloaded.status = self.downloaded.Status.ERROR

		self.downloaded.percent = (d['downloaded_bytes'] / d['total_bytes'])*100
		self.downloaded = self.downloaded.save()

		progress = {
			'downloaded_bytes': d.downloaded_bytes,
			'total_bytes': d.total_bytes,
			'total_bytes_estimate': d.total_bytes_estimate,
			'elapsed': d.elapsed,
			'eta': d.eta,
			'speed': d.speed,
		}

		if self.handleDownload is not None:
			self.handleDownload(progress)


	def runThread(self):
		self.downloaded.status = self.downloaded.Status.WAITING
		ydl_opts = {
			'outtmpl': self._directory+'%(id)s.%(ext)s',
			'nocheckcertificate': True,
			# 'ignoreerrors': True,
			'format': self._format,
			# 'postprocessors': [{
		 #        'key': 'FFmpegExtractAudio',
		 #        'preferredcodec': 'mp3',
		 #        'preferredquality': '192',
		 #    }],
			'logger': MyLogger(),
			'progress_hooks': [self.my_hook],
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download('https://www.youtube.com/watch?v=%s' % self.youtube_id)

		return



	def run(self):
		try:
			self.runThread()
		except Exception as err:
			self.__status_queue.put(err)
		self._stopEvent.set()
		self._status_queue.put(None)
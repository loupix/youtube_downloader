from django.db import models
from django.contrib.auth.models import User
from videos.models import Videos, Formats
import base64

import random, string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# Create your models here.


class Visitors(models.Model):
	id = models.CharField(max_length=7, primary_key=True)
	address_ip = models.CharField(max_length=15)
	kind = models.CharField(max_length=155, blank=True)
	model = models.CharField(max_length=155, blank=True)
	platform = models.CharField(max_length=155, blank=True)
	platform_version = models.CharField(max_length=155, blank=True)
	browser = models.CharField(max_length=155, blank=True)
	browser_version = models.CharField(max_length=155, blank=True)
	is_bot = models.BooleanField(default=False)

	location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="visitors")

	# user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	
	def __str__(self):
		return "Visitor #%s - %s" % (self.id, self.address_ip)

	def json(self):
		return {
			'id' : self.id,
			'is_bot' : self.is_bot
		}















class Location(models.Model):
	pays = models.CharField(max_length=255, null=True)
	region = models.CharField(max_length=255, null=True)
	ville = models.CharField(max_length=255, null=True)
	code_postal = models.CharField(max_length=255, null=True)
	latitude = models.FloatField(default=0.00)
	longitude = models.FloatField(default=0.00)
	_picture = models.TextField(db_column='picture', blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def set_picture(self, picture):
		# self._picture = picture
		self._picture = base64.b64encode(picture).decode()

	def get_picture(self):
		return self._picture
		# self._picture = base64.b64decode(picture)
		# return base64.decodebytes(self._picture)
		# return base64.encodebytes(self._picture).decode()


	picture = property(get_picture, set_picture)


	def __str__(self):
		return "Location #%d - %s  %s  %s" % (self.id, self.pays, self.region, self.ville)


	def json(self):
		return {
			"pays": self.pays,
			"region": self.region,
			"ville": self.ville,
			"code_postal": self.code_postal,
			"latitude": self.latitude,
			"longitude": self.longitude,
		}





















class Downloaded(models.Model):

	class Status(models.IntegerChoices):
		PENDING = 1
		WAITING = 2
		DOWNLOADING = 3
		DOWNLOADED = 4
		CONVERTING = 5
		FINISHED = 6
		DELETING = 7
		DELETED = 8
		ERROR = 9


	class Extension(models.IntegerChoices):
		MP4 = 1
		MKV = 2
		MP3 = 3
		WAV = 4

	id = models.CharField(max_length=14, primary_key=True)

	visitors = models.ManyToManyField("Visitors")
	status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
	
	downloaded_bytes = models.IntegerField(default=0)
	total_bytes = models.IntegerField(default=0)
	percent = models.FloatField(default=0.00)

	format_file = models.ForeignKey(Formats, on_delete=models.CASCADE, related_name="downloads")
	format_type = models.CharField(max_length=7, default="video")

	path = models.CharField(max_length=255)
	filename = models.CharField(max_length=255)

	url = models.CharField(max_length=255)
	url_id = models.CharField(max_length=25)
	video = models.ForeignKey(Videos, on_delete=models.CASCADE, null=True, related_name="downloads")

	downloaded = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)
	number_download = models.IntegerField(default=1)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	_thumbnail = models.TextField(db_column='thumbnail', blank=True)

	def set_thumbnail(self, thumbnail):
		# self._thumbnail = thumbnail
		self._thumbnail = base64.b64encode(thumbnail).decode()

	def get_thumbnail(self):
		return self._thumbnail
		# self._thumbnail = base64.b64decode(thumbnail)
		# return base64.decodebytes(self._thumbnail)
		# return base64.encodebytes(self._thumbnail).decode()


	thumbnail = property(get_thumbnail, set_thumbnail)

	def __str__(self):
		return "Download %s  %d%% - %s" % (self.id, self.percent, self.get_status_display())

	def json(self):

		return {
			'id': self.id,
			'url': self.url,
			'visitor': self.visitor.json(),
			'video': self.video.json(),
			'status': self.get_status_display(),
			'filename': self.filename,
			'thumbnail': self.thumbnail,
			'path': self.path,
			'total_bytes': self.total_bytes,
			'downloaded_bytes': self.downloaded_bytes,
			'downloaded': self.downloaded,
			'deleted': self.deleted,
			'number_download': self.number_download,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
		}

















class Queue(models.Model):
	id = models.CharField(max_length=7, primary_key=True)
	visitor = models.ForeignKey("Visitors", on_delete=models.CASCADE, related_name="queues")
	downloads = models.ManyToManyField(Downloaded)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return "Queue %s - %d downloads" % (self.id, len(self.downloads.all()))


	def json(self):

		return {
			"id": self.id,
			"downloads": list(map(lambda d:d.json(), self.downloads.exclude(video__isnull=True).all())),
		}
	
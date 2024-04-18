from django.db import models
from videos.models import Videos
import base64

# Create your models here.




class Tags(models.Model):
	value = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.value

	def __repr__(self):
		return self.value


class Phrases(models.Model):
	value = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.value

	def __repr__(self):
		return self.value








class Subtitles(models.Model):

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

	class Langage(models.IntegerChoices):
		EN = 0
		FR = 1
		ES = 2
		IT = 3
		DE = 4
		RU = 5

	lang = models.IntegerField(choices=Langage.choices, default=Langage.FR)
	status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

	startTime = models.TimeField()
	endTime = models.TimeField()

	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="subtitles")
	phrase = models.ForeignKey(Phrases, on_delete=models.CASCADE, related_name="files")


	created_at = models.DateTimeField(auto_now_add=True)


	@property
	def duration(self):
		return self.end - self.start
	







class Spectres(models.Model):
	subtitle = models.ForeignKey(Subtitles, on_delete=models.CASCADE, related_name="spectres")
	phrase = models.ForeignKey(Phrases, on_delete=models.CASCADE, related_name="spectres")

	tags = models.ManyToManyField(Tags)

	_content = models.TextField(db_column='content', blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def set_content(self, content):
		self._content = base64.b64encode(content).decode()

	def get_content(self):
		return self._content

	content = property(get_content, set_content)





class Files(models.Model):
	subtitle = models.ForeignKey(Subtitles, on_delete=models.CASCADE, related_name="files")

	content = models.BinaryField()
	created_at = models.DateTimeField(auto_now_add=True)
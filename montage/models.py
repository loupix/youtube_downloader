from django.db import models

from videos.models import Videos
from account.models import MyUser


class UserVideos(models.Model):
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="montages")
	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="montages")

	startTime = models.TimeField()
	endTime = models.TimeField()

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



class Filtres(models.Model):


	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
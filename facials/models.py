from django.db import models
import base64
from datetime import datetime, timedelta, date
from videos.models import Videos

# Create your models here.


class Tags(models.Model):
	value = models.CharField(max_length=255, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	show = models.BooleanField(default=True)

	def __str__(self):
		return "%s - %s" % (self.id, self.value)

	def json(self):
		return {
			"id":self.id,
			"value":self.value,
			"created_at":self.created_at,
		}



class Groups(models.Model):
	value = models.CharField(max_length=255, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)

	tags = models.ManyToManyField(Tags)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')

	def __str__(self):
		return "%s - %s" % (self.id, self.value)

	def json(self):
		return {
			"id":self.id,
			"value":self.value,
			"created_at":self.created_at,
			"tags":list(map(lambda t:t.json(), self.tags.all()))
		}



class Faces(models.Model):
	x = models.IntegerField()
	y = models.IntegerField()
	width = models.IntegerField()
	height = models.IntegerField()

	x_rel = models.FloatField(null=True)
	y_rel = models.FloatField(null=True)
	width_rel = models.FloatField(null=True)
	height_rel = models.FloatField(null=True)

	time_at = models.TimeField()

	# tags = models.ManyToManyField(Tags)

	_content = models.TextField(db_column='content', blank=True)

	def set_content(self, content):
		self._content = base64.b64encode(content).decode()

	def get_content(self):
		return self._content

	content = property(get_content, set_content)


	@property
	def contentDecoded(self):
		return base64.b64decode(self.content)


	def __str__(self):
		return "Face %d - %s - (%s %s %s %s)" % (self.id, self.time_at, self.x, self.y, self.width, self.height)



	class Category(models.IntegerChoices):
		UNKNOW = 0
		FACE = 1
		EYE = 2
		MOUTH = 3
		BODY = 4

	category = models.IntegerField(choices=Category.choices, default=Category.UNKNOW)
	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="faces")

	created_at = models.DateTimeField(auto_now_add=True)


	def json(self, content=True):
		return{
			"id":self.id,
			"x":self.x,
			"y":self.y,
			"width":self.width,
			"height":self.height,
			"time_at":self.time_at,
			"category":self.category_display(),
			"content":self.content,
		}




class Sequences(models.Model):

	faces = models.ManyToManyField(Faces)
	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="sequences")

	startTime = models.TimeField()
	endTime = models.TimeField()

	tags = models.ManyToManyField(Tags)


	class Category(models.IntegerChoices):
		UNKNOW = 0
		FACE = 1
		EYE = 2
		MOUTH = 3
		BODY = 4

	category = models.IntegerField(choices=Category.choices, default=Category.UNKNOW)
	

	created_at = models.DateTimeField(auto_now_add=True)


	@property
	def duration(self):
		end = datetime.combine(date.today(), self.endTime)
		start = datetime.combine(date.today(), self.startTime)
		tdelta = end-start
		fmt = "{minutes}:{seconds}"
		d = {"days": tdelta.days}
		d["hours"], rem = divmod(tdelta.seconds, 3600)
		d["minutes"], d["seconds"] = divmod(rem, 60)
		return fmt.format(**d)


	@property
	def durationSeconds(self):
		end = datetime.combine(date.today(), self.endTime)
		start = datetime.combine(date.today(), self.startTime)
		tdelta = end-start
		return tdelta.seconds


	@property
	def startSeconds(self):
		t = datetime.combine(date.min, self.startTime) - datetime.min
		return t.total_seconds()


	@property
	def endSeconds(self):
		t = datetime.combine(date.min, self.endTime) - datetime.min
		return t.total_seconds()



	def json(self):
		return {
			'id': self.id,
			'startTime': self.startTime,
			'endTime': self.endTime,
			'startSeconds': self.startSeconds,
			'endSeconds': self.endSeconds,
			'duration': self.duration,
			'created_at': self.endTime,
			"video_id":self.video.id,
			"youtube_id":self.video.youtube_id,
			"tags":list(map(lambda t:t.json(), self.tags.all())),
			"faces":list(map(lambda f:f.content, self.faces.all()))
		}












# class ModelsLearning(models.Model):

# 	number_learn = models.IntegerField()
# 	number_test = models.IntegerField()
# 	percent_reussite = models.FloatField()

# 	content = models.TextField()

# 	tags = models.ManyToManyField(Tags)
# 	group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="models")

# 	created_at = models.DateTimeField(auto_now_add=True)





# class TagsSuggested(models.Model):
# 	tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name="tags_suggested")
# 	face = models.ForeignKey(Faces, null=True, on_delete=models.CASCADE, related_name="tags_suggested")
# 	sequence = models.ForeignKey(Sequences, null=True, on_delete=models.CASCADE, related_name="tags_suggested")
# 	percent = models.FloatField(default=0)

# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)





# class GroupsSuggested(models.Model):
# 	group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="groups_suggested")
# 	face = models.ForeignKey(Faces, null=True, on_delete=models.CASCADE, related_name="groups_suggested")
# 	sequence = models.ForeignKey(Sequences, null=True, on_delete=models.CASCADE, related_name="groups_suggested")
# 	percent = models.FloatField(default=0)

# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)





# class Personne(models.Model):

# 	class Metier(models.IntegerChoices):
# 		UNKNOW = 0
# 		ARTISTE = 1
# 		CHANTEUR = 2
# 		COMPOSITEUR = 3
# 		JOURNALISTE = 4
# 		POLITIQUE = 5
# 		ACTEUR = 6


# 	name = models.CharField(max_length=255, unique=True)
# 	metier = models.IntegerField(choices=Metier.choices, default=Metier.UNKNOW)

# 	tags = models.ManyToManyField(Tags)

# 	firstname = models.CharField(max_length=255, null=True)
# 	lastname = models.CharField(max_length=255, null=True)
# 	dateOfBirth = models.DateField(null=True)

# 	sequences = models.ManyToManyField(Sequences)

# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)



	

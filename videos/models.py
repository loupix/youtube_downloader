from django.db import models
import base64


import random, string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))





















class Channels(models.Model):

	class Website(models.IntegerChoices):
		YOUTUBE = 1
		DAILYMOTION = 2
		VIMEO = 3
		FACEBOOK = 4
		INSTAGRAM = 5
		ODNOKLASSNIKI = 6
		TWITTER = 7
		TWITCH = 8
		XHAMSTER = 9
		YOUPORN = 10
		PORNHUB = 11


	url = models.CharField(max_length=255)
	url_id = models.CharField(max_length=155)
	channel_id = models.CharField(max_length=155)

	website = models.IntegerField(choices=Website.choices, default=Website.YOUTUBE)

	title = models.CharField(max_length=255)
	description = models.TextField()
	published_at = models.DateTimeField()
	default_language = models.CharField(max_length=25, default="French")

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	@property
	def get_absolute_url(self):
		return "v/"+self.youtube_id

	def json(self):
		return {
			'title': self.title,
			'description': self.description,
			'published_at': self.published_at,
		}
















class Tags(models.Model):
	value = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	def json(self):
		return {
			"value": self.value,
			"created_at": self.created_at,
		}



















class Formats(models.Model):
	format_id = models.CharField(max_length=128)
	format_note = models.CharField(max_length=128, null=True)
	name = models.CharField(max_length=128)
	ext = models.CharField(max_length=128)
	acodec = models.CharField(max_length=128, null=True)
	vcodec = models.CharField(max_length=128, null=True)
	asr = models.IntegerField(default=0, null=True)
	tbr = models.IntegerField(default=0, null=True)
	container = models.CharField(max_length=128, null=True)
	width = models.IntegerField(default=0)
	height = models.IntegerField(default=0)
	fps = models.FloatField(default=0, null=True)
	quality = models.IntegerField(default=0, null=True)

	def __str__(self):
		return "Format %s : %s %s" % (self.format_id, self.format_note, self.ext)

	def json(self):
		return {
			"format": self.name,
			"format_id": self.format_id,
			"format_note": self.format_note,
			"ext": self.ext,
			"width": self.width,
			"height": self.height,
			"fps": self.fps,
			"quality": self.quality,
			"asr": self.asr,
			"tbr": self.tbr,
		}






















class Videos(models.Model):

	class Category(models.IntegerChoices):
		FILM_ANIMATION = 1
		AUTOS_VEHICULE = 2
		MUSIC = 10
		PETS_ANIMAL = 15
		SPORTS = 17
		SHORTS_MOVIES = 18
		TRAVELS_EVENTS = 19
		GAMING = 20
		VIDEO_BLOGGING = 21
		PEOPLE_BLOGS = 22
		COMEDY = 23
		ENTERTAINMENT = 24


	class Website(models.IntegerChoices):
		YOUTUBE = 1
		DAILYMOTION = 2
		VIMEO = 3
		FACEBOOK = 4
		INSTAGRAM = 5
		ODNOKLASSNIKI = 6
		TWITTER = 7
		TWITCH = 8
		XHAMSTER = 9
		YOUPORN = 10
		PORNHUB = 11


	class Status(models.IntegerChoices):
		PENDING = 1
		FINISHED = 2
		ERROR = 3
		DOWNLOADING = 4
		DOWNLOADED = 5
		FACING = 6
		FACED = 7
		VOCALISING = 8
		VOCALISED = 9

	id = models.CharField(max_length=7, primary_key=True)
	url = models.CharField(max_length=255)
	url_id = models.CharField(max_length=155)

	website = models.IntegerField(choices=Website.choices, default=Website.YOUTUBE)
	category = models.IntegerField(choices=Category.choices, default=Category.ENTERTAINMENT)
	status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

	title = models.CharField(max_length=255)
	description = models.TextField(null=True)
	duration = models.TimeField()
	published_at = models.DateTimeField()

	channel = models.ForeignKey(Channels, on_delete=models.CASCADE, related_name="videos", null=True)
	tags = models.ManyToManyField(Tags)
	formats = models.ManyToManyField(Formats)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return "/v/"+self.youtube_id

	@property
	def duration_seconds(self):
		t = self.duration
		return (t.hour * 60 + t.minute) * 60 + t.second

	@property
	def nb_downloads(self):
		nb = 0
		for down in self.downloads.all():
			nb += down.number_download
		return nb


	def json(self, facials=False, stats=False):
		d = {
			'id': self.id,
			'url': self.url,
			'url_id': self.url_id,
			'title': self.title,
			'description': self.description,
			# 'category': self.get_category_display(),
			'duration': self.duration_seconds,
			'published_at': self.published_at,
			'nb_downloads': self.nb_downloads,
			'created_at': self.created_at,
			'website': self.get_website_display().lower(),
			'status': self.get_status_display(),
			# 'channel': self.channel.json(),
			'tags': list(map(lambda t:t.json(), self.tags.all())),
			# 'thumbnails': list(map(lambda t:t.json(), self.thumbnails.all())),
			'thumbnail': self.thumbnails.first().json(),
			'formats': list(map(lambda f:f.json(), self.formats.all())),
		}
		if facials:
			d['faces'] = self.faces.count()
			d['sequences'] = self.sequences.count()

		if stats:
			if self.statistiques.count()>0:
				stat = self.statistiques.last()
				d['statistiques'] = stat.json()
			else:d['statistiques'] = None

		return d


















class Format_urls(models.Model):
	format_video = models.ForeignKey(Formats, on_delete=models.CASCADE, related_name="urls")
	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="format_urls")
	url = models.CharField(max_length=510)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.url

	def json(self):
		return {
			"format": self.format_video.json(),
			"url": self.url,
			"created_at": self.created_at,
			"updated_at": self.updated_at,
		}















class Playlists(models.Model):
	playlist_id = models.CharField(max_length=155)

	title = models.CharField(max_length=255)
	description = models.TextField(null=True)
	published_at = models.DateTimeField()
	default_language = models.CharField(max_length=25, default="French")

	channel = models.ForeignKey(Channels, on_delete=models.CASCADE, related_name="playlists")
	videos = models.ManyToManyField(Videos)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

















	

class Statistique(models.Model):
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	commentaires = models.IntegerField(default=0)
	favorites = models.IntegerField(default=0)
	reposts = models.IntegerField(default=0)

	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="statistiques")

	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return "views %d, commentaires %d - %s" % (self.views, self.commentaires, self.created_at)


	def json(self):
		return {
			"views":self.views,
			"likes":self.likes,
			"dislikes":self.dislikes,
			"commentaires":self.commentaires,
			"favorites":self.favorites,
			"reposts":self.reposts,
			"created_at":self.created_at,
		}


















class Statistique_channel(models.Model):
	views = models.IntegerField(default=0)
	subcribers = models.IntegerField(default=0)
	videos = models.IntegerField(default=0)

	channel = models.ForeignKey(Channels, on_delete=models.CASCADE, related_name="statistiques_channel")

	created_at = models.DateTimeField(auto_now_add=True)


	def json(self):
		return {
			"views":self.views,
			"subscribers":self.subscribers,
			"videos":self.videos,
		}

















class Thumbnails(models.Model):

	class ThumbDimension(models.IntegerChoices):
		DEFAULT = 0
		MEDIUM = 1
		HIGH = 2
		LOW = 3
		STANDARD = 4
		MAXRES = 5
		MULTIPLE = 6
		UNKNOW = 7

	dimension = models.IntegerField(choices=ThumbDimension.choices, default=ThumbDimension.DEFAULT)
	# resolution = models.CharField(max_length=10)
	width = models.IntegerField(default=0)
	height = models.IntegerField(default=0)
	url = models.CharField(max_length=255)
	_content = models.TextField(db_column='content', blank=True)

	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name = 'thumbnails')

	created_at = models.DateTimeField(auto_now_add=True)

	def set_content(self, content):
		self._content = base64.b64encode(content).decode()

	def get_content(self):
		return self._content

	content = property(get_content, set_content)


	def json(self):
		return {
			"dimension": self.get_dimension_display(),
			"width": self.width,
			"height": self.height,
			"url": self.url,
			"content": self.content,
		}




















class Frames(models.Model):
	video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name = 'frames')
	
	time_at = models.TimeField()
	width = models.IntegerField(default=0)
	height = models.IntegerField(default=0)
	_content = models.TextField(db_column='content', blank=True)

	created_at = models.DateTimeField(auto_now_add=True)


	def set_content(self, content):
		self._content = base64.b64encode(content).decode()

	def get_content(self):
		return self._content

	content = property(get_content, set_content)


	def json(self):
		return {
			"time_at": self.time_at,
			"width": self.width,
			"height": self.height,
			"content": self.content,
		}

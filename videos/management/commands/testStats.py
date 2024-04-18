from django.core.management.base import BaseCommand, CommandError
from youtube.models import Videos, Statistique
from youtube.libraries import YoutubeApi


class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		print("Load ids")
		youtube_ids = Videos.objects.values_list("youtube_id")
		youtube_ids = list(map(lambda v:v[0], youtube_ids))
		print("Load data")
		data = YoutubeApi.getInfosVideos(youtube_ids[0])
		print(data)
		# print("Save data")

		# for item in data['items']:
		# 	video = Videos.objects.filter(youtube_id=item['id']).first()
		# 	print(video)
		# 	stat = item['statistics']
		# 	print(stat)
		# 	statObj = Statistique(video=video, views=int(stat['viewCount']), commentaires=int(stat['commentCount']),
		# 		likes=int(stat['likeCount']), favorites=int(stat['favoriteCount']))
		# 	print(statObj)


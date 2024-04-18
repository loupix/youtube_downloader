from django.core.management.base import BaseCommand, CommandError
from youtube.models import Videos, Channels, Statistique, Statistique_channel
from youtube.libraries import YoutubeApi


class Command(BaseCommand):
	help = 'Closes the speazcified poll for voting'

	def handle(self, *args, **options):
		channel_ids = Channels.objects.values_list("channel_id")
		channel_ids = list(map(lambda v:v[0], channel_ids))
		print(channel_ids)
		# logger.info("Load data")
		data = YoutubeApi.getStatsChannels(channel_ids)

		# logger.info("Save data")

		for item in data['items']:
			channel = Channels.objects.filter(channel_id=item['id']).first()
			if not channel:raise ObjectDoesNotExist("Channel")
			stat = item['statistics']
			statObj = Statistique_channel(channel=channel, views=int(stat['viewCount']),
				subcribers=int(stat['subscriberCount']), videos=int(stat['videoCount']))
			statObj.save()


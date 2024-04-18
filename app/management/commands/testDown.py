from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import sys, os, json
import redis

from app.tasks import download_file
from app.models import Downloaded



class Command(BaseCommand):
	help = 'Closes the speazcified poll for voting'

	def handle(self, *args, **options):
		from random import choice
		import pprint as pp
		download_ids = Downloaded.objects.values('id').all()
		download_ids = list(map(lambda d:d['id'], download_ids))
		download_id = choice(download_ids)

		download = Downloaded.objects.get(id=download_id)

		try:
			os.remove(download.path)
		except:pass

		download.total_bytes = 0
		download.download_bytes = 0
		download.percent = 0
		download.save()

		download_file.apply_async((download.id,))

		r = redis.StrictRedis(host=settings.REDIS_URL, port=settings.REDIS_PORT, db=1)
		p = r.pubsub()
		p.psubscribe(download_id)
		for message in p.listen():
			if message:
				m_type = message.get('type', '')
				m_pattern = message.get('pattern', '')
				m_channel = message.get('channel', '')
				data = message.get('data', '')

				print(m_type, m_pattern, m_channel)

				if m_type=="pmessage":
					data = json.loads(data)
					print(data)
					if data['status'] in ["Error", "finished"]:break


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import sys, os, json
import redis



class Command(BaseCommand):
	help = 'Closes the speazcified poll for voting'

	def handle(self, *args, **options):
		r = redis.StrictRedis(host=settings.REDIS_URL, port=settings.REDIS_PORT, db=1)
		p = r.pubsub()
		
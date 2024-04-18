import sys
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from facials.libraries import LearnLib
from videos.models import *
from facials.models import *

import cv2


class Command(BaseCommand):
	help = 'Create spectre and save in database'
	_now = datetime.now()

	def handle(self, *args, **options):
		import pprint
		g = Groups.objects.last()
		pp.pprint(g)

		sample = LearnLib.getGroupsFaces(g.id)
		pp.pprint(sample)

		return

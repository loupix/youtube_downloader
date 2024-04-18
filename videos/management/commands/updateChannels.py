from django.core.management.base import BaseCommand, CommandError
from youtube.models import *
from youtube.libraries import *
from youtube.tasks import *


class Command(BaseCommand):

	def handle(self, *args, **options):

		update_channels()
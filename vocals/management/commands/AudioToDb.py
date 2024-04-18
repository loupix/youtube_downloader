import sys
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from vocals.libraries import VocalLib


class Command(BaseCommand):
	help = 'Create spectre and save in database'
	_now = datetime.now()

	def handle(self, *args, **options):
		youtube_id = "ix1OXzR1HXo" 		# ZAZ
		# youtube_id = "xiFrIP8HGBY"	# ABC de CAVous
		
		print("%s - Download" % (datetime.now() - self._now))
		down = VocalLib.download(youtube_id)
		if not down:
			sys.exit("No Subtitles")


		audio_file, srt_file = down


		print("%s - Gen Phrases" % (datetime.now() - self._now))
		Phrases_dict = VocalLib.srtDict(srt_file)


		print("%s - Save Phrases & Subtitles" % (datetime.now() - self._now))
		Subs_db = VocalLib.SrtToBdd(youtube_id, Phrases_dict)
		
		try:
			print("%s - Save Audio & Spectres" % (datetime.now() - self._now))
			VocalLib.AudioToBdd(audio_file, Phrases_dict, Subs_db)
		except Exception as e:
			sys.exit(e)













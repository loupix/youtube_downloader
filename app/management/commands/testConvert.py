from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os
import subprocess as sp
import sys
from ffmpeg_progress import start



def ffmpeg_callback(infile: str, outfile: str, vstats_path: str):
	return sp.Popen(['ffmpeg',
			'-nostats',
			'-loglevel', '0',
			'-y',
			'-vstats_file', vstats_path,
			'-i', infile,
			outfile]).pid


def on_message_handler(percent: float,
						fr_cnt: int,
						total_frames: int,
						elapsed: float):
	sys.stdout.write('\r{:.2f}%'.format(percent))
	sys.stdout.flush()






class Command(BaseCommand):
	help = 'Closes the speazcified poll for voting'

	def handle(self, *args, **options):


		file_in = os.path.join(settings.MEDIA_ROOT,'iMjeB_c33iU_134.mp4')
		file_out = os.path.join(settings.MEDIA_ROOT, 'iMjeB_c33iU.mp4')

		try:
			os.remove(file_out)
		except:pass

		start(file_in,
			file_out,
			ffmpeg_callback,
			on_message=on_message_handler,
			on_done=lambda: print(''),
			wait_time=1)  # seconds


		# cmd = [
		# 	"ffmpeg", "-i", file_in, "-c:v", "libx264", "-preset", "fast", file_out,
		# ]

		# ff = FfmpegProgress(cmd)
		# with tqdm(total=100, position=1, desc="Test") as pbar:
		# 	for progress in ff.run_command_with_progress():
		# 		pbar.update(progress - pbar.n)


		# cmd = 'ffmpeg -i %s -vcodec h264 %s' % (file_in, file_out)
		# thread = pexpect.spawn(cmd)
		# print("started %s" % cmd)
		# cpl = thread.compile_pattern_list([
		#     pexpect.EOF,
		#     "frame= *\d+",
		#     '(.+)'
		# ])
		# while True:
		# 	i = thread.expect_list(cpl, timeout=None)
		# 	if i == 0: # EOF
		# 		print("the sub process exited")
		# 		break
		# 	elif i == 1:
		# 		frame_number = thread.match.group(0)
		# 		print(frame_number)
		# 		thread.close
		# 	elif i == 2:
		# 		fps_number = thread.match.group(0)
		# 		print(fps_number)
		# 		thread.close
		# 	elif i == 3:
		# 		size = thread.match.group(0)
		# 		print(size)
		# 		pass


	    # file_in = os.path.join(settings.MEDIA_ROOT,'iMjeB_c33iU_134.mp4')
		# file_out = os.path.join(settings.MEDIA_ROOT, 'iMjeB_c33iU.mp4')

		# out, err = (
		# 	ffmpeg #pylint: disable = no-member
		# 		.input(file_in)
		# 		.output(file_out, vcodec="h264")
		# 		.overwrite_output()
		# 		.run(quiet=False)
		# )

		# print('ffmpeg stdout: %s', out.decode())
		# print('ffmpeg stderr: %s', err.decode())



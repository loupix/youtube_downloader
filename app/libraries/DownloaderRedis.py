import os, sys, re
import yt_dlp as youtube_dl
import ffmpeg
import redis
import json

from datetime import datetime, timedelta

from django.conf import settings
from django.utils.timezone import utc

from app.models import Downloaded

import logging
logger = logging.getLogger("libraries")

class DownloaderRedis:
    
    _killed = False
    _downloaded = None
    _redis_client = None

    def __init__(self, downloaded_id):
        try:
            self._downloaded = Downloaded.objects.get(id=downloaded_id)
        except Downloaded.DoesNotExist:return

        self._redis_client = redis.StrictRedis(host=settings.REDIS_URL, port=settings.REDIS_PORT, db=1)



    @property
    def kill(self):
        return self._killed

    @kill.setter
    def kill(self, value=True):
        self._killed = value




    def my_hook(self, obj):
        # sys.stderr.write("\n%s" % obj)
        obj['download_id'] = self._downloaded.id
        obj['status_type'] = "Hook"
        if not self._killed:
            self._redis_client.publish(self._downloaded.id, json.dumps(obj))

        update=False
        if '_percent_str' in obj:
            self._downloaded.percent = float(obj['_percent_str'][0:-1])
            update=True
        if 'downloaded_bytes' in obj:
            self._downloaded.downloaded_bytes = obj['downloaded_bytes']
            update=True
        if 'total_bytes' in obj:
            self._downloaded.total_bytes = obj['total_bytes']
            update=True

        if 'status' in obj:
            if obj['status']=="downloading": self._downloaded.status = Downloaded.Status.DOWNLOADING
            if obj['status']=="converting": self._downloaded.status = Downloaded.Status.CONVERTING
            if obj['status']=="finished": self._downloaded.status = Downloaded.Status.FINISHED
            update=True
        
        if update: self._downloaded.save()


    def download(self):
        url = self._downloaded.url
        format_file = self._downloaded.format_file.format_id

        ydl_opts = {
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(id)s_%(format_id)s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': False,
            'noplaylist': True,
            'nopart': False,
            # "simulate": True,
            # 'ignoreerrors': True,
            'format': format_file,
            'logger': MyLogger(self, self._downloaded, self._redis_client),
            'progress_hooks': [self.my_hook],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # ydl.cache.remove()
                info_dict = ydl.extract_info(url, download=False)
                ydl.prepare_filename(info_dict)
                ydl.download([url])

        except Downloaded.DoesNotExist:
            logger.error('Downloaded Object %s Not Found.' % self._downloaded.id)
            d = {}
            d['status_type'] = 'Error'
            d['content'] = "%s" % e
            d['download_id'] = self._downloaded.id
            if not self._killed:
                self._redis_client.publish(self._downloaded.id, json.dumps(d))
                self._killed = True

        except youtube_dl.utils.DownloadError as e:
            logger.error('This URL is invalid.')
            d = {}
            d['status_type'] = 'Error'
            d['content'] = 'This URL is invalid.'
            d['download_id'] = self._downloaded.id
            if not self._killed:
                self._redis_client.publish(self._downloaded.id, json.dumps(d))
                self._killed = True

        except Exception as e:
            logger.error("%s" % e)
            d = {}
            d['status_type'] = 'Error'
            d['content'] = "%s" % e
            d['download_id'] = self._downloaded.id
            if not self._killed:
                self._redis_client.publish(self._downloaded.id, json.dumps(d))
                self._killed = True



    def converting(self, downloaded, extension=".mp4"):
        no_extension = str(os.path.splitext(downloaded.path))
        with_ext = no_extension + extension
        out, err = (
            ffmpeg #pylint: disable = no-member
                .input(downloaded.path)
                .output(with_ext, vcodec="h264")
                .overwrite_output()
                .run(quiet=True)
            )

        print('ffmpeg stdout: %s', out.decode())
        print('ffmpeg stderr: %s', err.decode())
        return







class MyLogger(object):

    _thread = None
    _downloaded = None
    _redis_client = None

    def __init__(self, thread, downloaded, redis_client):
        self._thread = thread
        self._downloaded = downloaded
        self._redis_client = redis_client


    def debug(self, msg):
        # sys.stderr.write("\nDebug %s" % msg)
        logger.debug(msg)

        m = re.match(pattern=r"\[(?P<status>\w+)\] (?P<content>.*)", string=msg)
        if m:
            d = m.groupdict()
            d['status_type'] = "Debug"
            d['download_id'] = self._downloaded.id
            if not self._thread.kill:
                self._redis_client.publish(self._downloaded.id, json.dumps(d))
        return


    def infos(self, msg):
        # sys.stderr.write("\nInfos %s" % msg)
        logger.infos(msg)

        m = re.match(pattern=r"(?P<status>\w+) (?P<content>.*)", string=msg)
        if m:
            d = m.groupdict()
            d['status_type'] = 'Infos'
            d['download_id'] = self._downloaded.id
            if not self._thread.kill:
                self._redis_client.publish(self._downloaded.id, json.dumps(d))
        return

    def warning(self, msg):
        # sys.stderr.write("\nWarning %s" % msg)
        logger.warning(msg)

        d = {}
        d['status_type'] = 'Warning'
        d['content'] = msg
        d['download_id'] = self._downloaded.id
        if not self._thread.kill:
            self._redis_client.publish(self._downloaded.id, json.dumps(d))
        return

    def error(self, msg):
        # sys.stderr.write("\nError %s" % msg)
        logger.error(msg)
        
        d = {}
        d['status_type'] = 'Error'
        d['content'] = msg
        d['download_id'] = self._downloaded.id
        if not self._thread.kill:
            self._redis_client.publish(self._downloaded.id, json.dumps(d))
        return
from django.conf import settings
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.consumer import SyncConsumer

import json, sys, re, os
import redis
import urllib

from multiprocessing import Process, Event
import threading, queue

import logging
logger = logging.getLogger("channels")

from app.models import Downloaded
from app.libraries import DownloadCrud, QueueCrud
from app.tasks import *
from facials.tasks import *
from videos.tasks import *


class InvalidURL(Exception):
    pass

class SongExists(Exception):
    pass

class Stop_Download(Exception): # This is our own special Exception class
    pass

    def usr1_handler(signum,frame): # When signal comes, run this func
        raise Stop_Download


 


class DownloadChannels(WebsocketConsumer):

    _directory = settings.MEDIA_ROOT
    _all_process = {}
    _resume_event = Event()
    _queue = None

    def connect(self):
        sys.stdout.write("\nConnexion")
        self.accept()


    def disconnect(self, close_code):
        sys.stderr.write("\nDeconnexion code %s" % close_code)
        self._resume_event.set()
        super().disconnect(close_code)




    def receive(self, text_data, **kwargs):
        response = json.loads(text_data)
        message_type = response.get("message_type")
        if not self._queue:
            self._queue = QueueCrud.read(self.scope['session'])

        if message_type == "queue.get":
            self._queue = QueueCrud.read(self.scope['session'])
            self.send(text_data=json.dumps({
                'message_type': "queue.get",
                "id": self._queue.id,
                "downloading": list(map(lambda d: {'percent':d.percent, 'filename':d.filename, 
                    'path':d.path, 'thumbnail':d.thumbnail, 'status':d.status, 'id':d.id},
                    self._queue.downloads.all()))
            }))


        if message_type == "queue.del":
            download_id = response.get("download_id")
            downloaded = Downloaded.objects.get(id=download_id)
            if not downloaded:return

            if download_id in self._all_process.keys():
                self._all_process[download_id].terminate()

            self._queue = QueueCrud.remove(self._queue, downloaded)
            self.send(text_data=json.dumps({
                'message_type': "queue.del",
                "id": self._queue.id,
                "download_id": download_id
            }))


        if message_type == "download.reload":
            download_id = response.get("download_id")
            visitor_id = response.get("visitor_id")
            try:
                downloaded = Downloaded.objects.get(id=download_id)
            except Downloaded.DoesNotExist:
                logger.warning("download %s not found")


            if not downloaded:return

            if downloaded.status == Downloaded.Status.FINISHED or downloaded.percent==100:
                downloaded.status = Downloaded.Status.FINISHED
                downloaded.save()
                if os.path.exists(downloaded.path):
                    d = {}
                    d['message_type'] = 'download.debug'
                    d['download_id'] = downloaded.id
                    d['filename'] = downloaded.filename
                    d['total_bytes'] = downloaded.total_bytes
                    d['format_file'] = downloaded.format_file.json()
                    d['thumbnail'] = downloaded.thumbnail
                    d['file_path'] = os.path.join(settings.MEDIA_URL, downloaded.path.split("/")[-1])
                    d['status'] = "finished"
                    d['_percent_float'] = downloaded.percent
                    self.send(text_data = json.dumps(d))
                    return
                

            _my_process = threadDownload(self, downloaded)
            _my_process.start()
            self._all_process[downloaded.id] = _my_process



        if message_type == "download.start":
            format_type = response.get("format_type")
            format_file = response.get("format_file")
            filename = response.get("filename")
            thumbnail_url = response.get("thumbnail_url")
            url = response.get("url")
            url_id = response.get("url_id")
            website = response.get("website")


            # Ajoute à la BDD
            fp = urllib.request.urlopen(thumbnail_url)
            thumbnail = fp.read()
            fp.close()
            
            downloaded = DownloadCrud.create({
                'percent': 0,
                'filename': filename,
                'path': os.path.join(settings.MEDIA_ROOT, url_id+"_"+format_file['format_id']+"."+format_file['ext']),
                'visitor_id': self.scope['session'].get("visitor_id"),
                'url':url,
                'url_id':url_id,
                'format_file':format_file,
                'format_type':format_type,
                'thumbnail':thumbnail,
                'status': Downloaded.Status.PENDING,
            })


            # Envoie les données
            self.send(text_data=json.dumps({'message_type':'download.started',  
                'percent': 0,
                'download_id': downloaded.id,
                'filename': filename,
                'thumbnail': downloaded.thumbnail,
                'url':url,
                'url_id':url_id,
                'format_type':format_type,
                'format_file':format_file
            }))


            # Ajoute à une file d'attente
            self._queue.downloads.add(downloaded)
            self._queue.save()


            # Asynchrone infos video
            videos_infos.apply_async((downloaded.id, url, url_id, website))
            logger.info("Downloading - %s" % url_id)


            # Execute processus download
            _my_process = threadDownload(self, downloaded)
            _my_process.start()
            self._all_process[downloaded.id] = _my_process

        elif message_type == "download.update":
            try:
                download_id = response.get("download_id")
                d = Downloaded.objects.get(id=download_id)
                if d is None:raise ObjectDoesNotExist("downloaded")
                d.downloaded = True
                d.number_download += 1
                d.save()
            except Exception as e:sys.stderr.write("\n%s" % e)

        elif message_type == "youtube.infos":
            sys.stderr.write("\nCalling API")

        pass


















class threadDownload(threading.Thread):

    _socket = None
    _downloaded = None
    _subsribe = None
    _task = None
    _killed = False
    _redis_client = None
    _started = True


    def __init__(self, socket, downloaded):
        threading.Thread.__init__(self)
        self._stopEvent = threading.Event()
        self._status_queue = queue.Queue()

        self._socket = socket
        self._downloaded = downloaded

        self._redis_client = redis.StrictRedis(host=settings.REDIS_URL, port=settings.REDIS_PORT, db=1)
        self._subsribe = self._redis_client.pubsub()



    def wait_for_exc_info(self):
        return self._status_queue.get()

    def join_with_exception(self):
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            return
        else:
            raise ex_info

    @property
    def kill(self):
        return self._killed

    @kill.setter
    def kill(self, value=True):
        self._killed = value


    def terminate(self):
        self._killed = True




    def hook(self, data):

        # sys.stderr.write("\nHook %s" % data)

        if "_percent_str" in data:
            data["_percent_float"] = float(data['_percent_str'][0:-1])


        data['message_type'] = 'download.progress'
        data['url_id'] = self._downloaded.url_id
        data['download_id'] = self._downloaded.id
        data['format_file'] = self._downloaded.format_file.json()
        data['format_type'] = self._downloaded.format_type
        data['filename'] = self._downloaded.filename
        data['file_path'] = os.path.join(settings.MEDIA_URL, self._downloaded.path.split("/")[-1])
        if self._started:
            data['thumbnail'] = self._downloaded.thumbnail

        if self._started:self._started=False

        if not self._killed:
            self._socket.send(text_data = json.dumps(data))





    def debug(self, data):
        # sys.stderr.write("\nDebug %s" % data)

        data['message_type'] = 'download.debug'
        data['download_id'] = self._downloaded.id
        data['downloaded_bytes'] = self._downloaded.downloaded_bytes
        data['total_bytes'] = self._downloaded.total_bytes
        data['format_file'] = self._downloaded.format_file.json()
        data['filename'] = self._downloaded.filename
        data['file_path'] = os.path.join(settings.MEDIA_URL, self._downloaded.path.split("/")[-1])
        if self._started:
            data['thumbnail'] = self._downloaded.thumbnail

        if self._started:self._started=False


        if data['status'] == "ffmpeg":
            update_downloaded.apply_async((self._downloaded.id, data['status'], 98, 
                data['downloaded_bytes'], data['total_bytes']))


        if data['status'] == "download":
            sys.stderr.write("\n%s" % data['content'])

            if "Destination" in data['content']:return
            if "ETA" in data['content']:return

            if "Unable to resume" in data['content']:
                data['message_type'] = 'download.error'
                update_downloaded.apply_async((self._downloaded.id, data['status'], 0, 
                    self._downloaded.downloaded_bytes, self._downloaded.total_bytes))
                removeFile.apply_async((self._downloaded.path,))

            if "has already been downloaded and merged" in data['content']:
                data['status'] = "finished"
                data['_percent_float'] = 100
                # Asynchrone update percent
                update_downloaded.apply_async((self._downloaded.id, data['status'], 100, 
                    self._downloaded.downloaded_bytes, self._downloaded.total_bytes))


            if "has already been downloaded" in data['content']:
                data['status'] = "finished"
                data['_percent_float'] = 100
                # Asynchrone update percent
                update_downloaded.apply_async((self._downloaded.id, data['status'], 100, 
                    self._downloaded.downloaded_bytes, self._downloaded.total_bytes))

        if not self._killed:
            self._socket.send(text_data = json.dumps(data))


    def infos(self, data):
        sys.stderr.write("\nInfos %s" % data)

        data['message_type'] = 'download.infos'
        data['_filename'] = self.downloaded.path.split("/")[-1]
        if not self._killed:
            self._socket.send(text_data = json.dumps(data))

    def warning(self, data):
        sys.stderr.write("\nWarning %s" % msg)

        data['message_type'] = 'download.warning'
        if not self._killed:
            self._socket.send(text_data = json.dumps(data))
        return

    def error(self, data):
        sys.stderr.write("\nError %s" % msg)
        data['message_type'] = 'download.error'
        if not self._killed:
            self._socket.send(text_data = json.dumps(data))
            self._killed = True
        return







    def subscribe(self):
        self._subsribe.psubscribe(self._downloaded.id)
        for message in self._subsribe.listen():
            if message:
                m_type = message.get('type', '')
                m_pattern = message.get('pattern', '')
                m_channel = message.get('channel', '')
                data = message.get('data', '')
                if m_type=="pmessage":
                    data = json.loads(data)
                    if data['status_type']=="Hook":self.hook(data)
                    elif data['status_type']=="Debug":self.debug(data)
                    elif data['status_type']=="Info":self.info(data)
                    elif data['status_type']=="Warning":self.warning(data)
                    elif data['status_type']=="Error":self.error(data)




    def run(self):
        try:
            if self._downloaded.status not in [Downloaded.Status.FINISHED, Downloaded.Status.DOWNLOADING]:
                download_file.apply_async((self._downloaded.id,))
            self.subscribe()
        except Exception as err:
            sys.stderr.write("\nError Subscribe %s" % err)
            self._status_queue.put(err)
            self._stopEvent.set()
            self._status_queue.put(None)


















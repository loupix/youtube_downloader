# videos/tasks.py
from django.core.exceptions import *
from math import *
import threading
from datetime import datetime, time

from django.contrib.sessions.backends.db import SessionStore

from youtubeDownload.celery import app

from app.models import *
from facials.tasks import *
from videos.models import *
from videos.libraries import *

import logging
logger = logging.getLogger("tasks")

from .views import MAX_VIDEOS_HOME

import multiprocessing
NB_CORE = multiprocessing.cpu_count()




quotas_exceeded = False
quotas_exceeded_time = datetime.now()

# limit_quotas_sec = 30*60

# session = SessionStore(session_key='sessionid')
# session['quotas_exceeded'] = False
# session['quotas_exceeded_time'] = datetime.now()

# def get_quotas_exceeded():
#     global session, limit_quotas_sec
#     if session['quotas_exceeded']:
#         td = datetime.now() - session['quotas_exceeded_time']
#         if td.total_seconds()>=limit_quotas_sec:
#             session['quotas_exceeded'] = False
#             session.save()
#             return False
#         else:
#             return True
#     else:
#         return False



# def set_quotas_exceeded(status=True):
#     global session
#     if session['quotas_exceeded'] != status:
#         session['quotas_exceeded'] = status
#         session['quotas_exceeded_time'] = datetime.now() if status else False


# def get_quotas_exceeded_time():
#     global session, limit_quotas_sec
#     td = datetime.now() - session['quotas_exceeded_time']
#     return datetime.utcfromtimestamp(limit_quotas_sec - td.total_seconds()).time()


# def set_quotas_exceeded_time():
#     global session
#     session['quotas_exceeded_time'] = datetime.now()
#     session.save()


# def init_session():
#     global session
#     session['quotas_exceeded'] = False
#     session['quotas_exceeded_time'] = datetime.now()
#     session.save()


# @app.task
# def youtube_infos(url, url_id, downloaded_id):
#     try:
#         video = YoutubeCrud.create({'url_id':url_id, 'url':url})
#         if video is None:raise ObjectDoesNotExist("Youtube Video")

#         down = Downloaded.objects.get(id=downloaded_id)
#         if down is None:raise ObjectDoesNotExist("Downloaded")

#         down.video = video
#         down.save()

#         # Taches Async

#         stats_video.apply_async((video.url_id,))
#         update_channel.apply_async((video.channel.channel_id,), countdown=30)

#         seconds = (video.duration.hour * 60 + video.duration.minute) * 60 + video.duration.second
#         if seconds <= (8*60):
#             VideoToFace.apply_async((video.url_id,), countdown=120)

#         return down
#     except ObjectDoesNotExist as e:
#         logger.error("ObjectDoesNotExist %s" % e)
#     except Exception as e:
#         if "Erreur de Quotas" in str(e):
#             set_quotas_exceeded(True)
#         logger.error(e)









@app.task
def videos_infos(downloaded_id, url, url_id, website):
    try:
        video = VideoCrud.create({'url':url, 'url_id':url_id, 'website':website, })
        if video is None:raise ObjectDoesNotExist("Video")

        down = Downloaded.objects.get(id=downloaded_id)
        if down is None:raise ObjectDoesNotExist("Downloaded")

        down.video = video
        down.save()

        # Taches Async

        # stats_video.apply_async((video.url_id,))
        # update_channel.apply_async((video.channel.channel_id,), countdown=30)


        if video.frames.count()==0:
            videos_frames.apply_async((video.id,))


        # seconds = (video.duration.hour * 60 + video.duration.minute) * 60 + video.duration.second
        # if seconds <= (8*60):
        #     VideoToFace.apply_async((video.url_id,), countdown=120)


        return down
    except ObjectDoesNotExist as e:
        logger.error("ObjectDoesNotExist %s" % e)
    except Exception as e:
        if "Erreur de Quotas" in str(e):
            set_quotas_exceeded(True)
        logger.error(e)





















@app.task
def videos_frames(video_id=None):
    try:
        if video_id is None:
            from random import choice
            ids = Frames.objects.all().values("video_id").distinct()
            ids = list(map(lambda d:d['video_id'], ids))
            video_ids = Videos.objects.exclude(id__in=ids).values("id").distinct()
            video_ids = list(map(lambda d:d['id'], video_ids))
            if len(video_ids)==0:
                logger.warning("Aucune nouvelles vidéos")
                return "Aucunes vidéos"

            video_id = choice(video_ids)

        now = datetime.now()

        try:
            video = Videos.objects.get(id=video_id)
        except Videos.DoesNotExist:
            logger.error("Video %s Not Found" % video_id)
            return "Video %s Not Found" % video_id
                    
        logger.debug("Started - %s" % datetime.now())
        logger.debug("%s - %s" % (video.title, video.duration))

        logger.debug("%s - Download" % (datetime.now() - now))
        video_file = FrameLib.download(video.url)

        logger.debug("%s - Extract Frames" % (datetime.now() - now))
        nbFrames, nbNewFrames = FrameLib.extractFrames(video_file, video)
        logger.debug("%s - %d Frames - %d New" % ((datetime.now() - now), nbFrames, nbNewFrames))

        removeFile.apply_async((video_file,))
    except Videos.DoesNotExist as e:
        logger.error("ObjectDoesNotExist %s" % e)
    except ObjectDoesNotExist as e:
        logger.error("ObjectDoesNotExist %s" % e)
    except Exception as e:
        if "Erreur de Quotas" in str(e):
            set_quotas_exceeded(True)
        logger.error(e)


























@app.task
def stats_channel(channel_id):

    if get_quotas_exceeded():
        return "Quotas Waiting - %s" % get_quotas_exceeded_time()

    try:
        channel = Channels.objects.get(channel_id=channel_id)

        # data = YoutubeApi.getStatsVideos(url_id)
        # if len(data['items'])==0:raise ObjectDoesNotExist("Stats Videos")

        # item = data['items'][0]
        # stat = item['statistics']
        # try:
        #     Statistique.objects.get(video=video, views=int(stat['viewCount']), commentaires=int(stat['commentCount']),
        #     likes=int(stat['likeCount']), favorites=int(stat['favoriteCount']))
        # except Statistique.DoesNotExist:
        #     statObj = Statistique(video=video, views=int(stat['viewCount']), commentaires=int(stat['commentCount']),
        #         likes=int(stat['likeCount']), favorites=int(stat['favoriteCount']))
        #     statObj.save()

        return channel

    except ObjectDoesNotExist as e:
        logger.error("ObjectDoesNotExist %s" % e)
    except Exception as e:
        if "Erreur de Quotas" in str(e):
            set_quotas_exceeded(True)
        logger.error(e)










@app.task
def stats_multi_video(url_ids):

    if get_quotas_exceeded():
        return "Quotas Waiting - %s" % get_quotas_exceeded_time()

    try:
        nbVideos = 0

        step = 10
        for i in range(0, len(url_ids), step):
            
            try:
                data = YoutubeApi.getStatsVideos_multi(url_ids[i:i+step])
            except Exception as e:
                logger.error(e)
                return str(e)


            for item in data['items']:
                try:
                    video = Videos.objects.get(url_id=item['id'])
                except Videos.DoesNotExist:continue

                stat = item['statistics']
                try:
                    Statistique.objects.get(video=video, views=int(stat['viewCount']), commentaires=int(stat['commentCount']),
                    likes=int(stat['likeCount']), favorites=int(stat['favoriteCount']))
                except Statistique.DoesNotExist:
                    statObj = Statistique(video=video, views=int(stat['viewCount']), commentaires=int(stat['commentCount']),
                        likes=int(stat['likeCount']), favorites=int(stat['favoriteCount']))
                    statObj.save()
                    nbVideos+=1

        logger.info("stats_multi_videos %d videos" % nbVideos)
    except ObjectDoesNotExist as e:
        logger.error("ObjectDoesNotExist %s" % e)
    except Exception as e:
        if "Erreur de Quotas" in str(e):
            set_quotas_exceeded(True)
        logger.error(e)






# @app.task
# def stats_all_videos():

#     if get_quotas_exceeded():
#         return "Quotas Waiting - %s" % get_quotas_exceeded_time()

#     try:

#         nbVideos = 0
#         step = 20
#         for i in range(0,Videos.objects.count(),step):

#             # logger.info("Load ids")
#             url_ids = Videos.objects.filter(website=Videos.Website.YOUTUBE).order_by("-published_at").values_list("url_id")[i:i+step]
#             url_ids = list(map(lambda v:v[0], url_ids))
#             url_ids = url_ids[:MAX_VIDEOS_HOME]
#             # logger.info("Load data")


#             try:
#                 data = YoutubeApi.getStatsVideos_multi(url_ids)
#             except Exception as e:logger.error("%s" % e)



#             for item in data['items']:
#                 try:
#                     video = Videos.objects.get(url_id=item['id'])
#                 except Videos.DoesNotExist:continue

#                 stat = item['statistics']
#                 try:
#                     Statistique.objects.get(video=video, views=int(stat['viewCount']), commentaires=int(stat['commentCount']),
#                     likes=int(stat['likeCount']), favorites=int(stat['favoriteCount']))
#                 except Statistique.DoesNotExist:
#                     statObj = Statistique(video=video, views=int(stat['viewCount']), commentaires=int(stat['commentCount']),
#                         likes=int(stat['likeCount']), favorites=int(stat['favoriteCount']))
#                     statObj.save()
#                     nbVideos+=1

#         logger.info("stats_all_videos %d videos" % nbVideos)
#     except ObjectDoesNotExist as e:
#         logger.error("ObjectDoesNotExist %s" % e)
#     except Exception as e:
#         if "Erreur de Quotas" in str(e):
#             set_quotas_exceeded(True)
#         logger.error(e)











@app.task
def stats_all_channels():

    if get_quotas_exceeded():
        return "Quotas Waiting - %s" % get_quotas_exceeded_time()

    try:

        nbChannels = 0
        step = 20
        for i in range(0,Channels.objects.count(),step):

            # logger.info("Load ids")
            channel_ids = Channels.objects.values_list("channel_id")[i:i+step]
            channel_ids = list(map(lambda v:v[0], channel_ids))
            # logger.info("Load data")
            data = YoutubeApi.getStatsChannels(channel_ids)
            
            # logger.info("Save data")

            for item in data['items']:
                channel = Channels.objects.filter(channel_id=item['id']).first()
                if not channel:raise ObjectDoesNotExist("Channel")
                stat = item['statistics']
                try:
                    Statistique_channel.objects.get(channel=channel, views=int(stat['viewCount']),
                    subcribers=int(stat['subscriberCount']), videos=int(stat['videoCount']))
                except Statistique_channel.DoesNotExist:
                    statObj = Statistique_channel(channel=channel, views=int(stat['viewCount']),
                        subcribers=int(stat['subscriberCount']), videos=int(stat['videoCount']))
                    statObj.save()
                    nbChannels+=1
        logger.info("stats_all_channels %d channels" % nbChannels)

    except ObjectDoesNotExist as e:
        logger.error("ObjectDoesNotExist %s" % e)
    except Exception as e:
        if "Erreur de Quotas" in str(e):
            set_quotas_exceeded(True)
        logger.error(e)









@app.task
def update_channels():

    if get_quotas_exceeded():
        return "Quotas Waiting - %s" % get_quotas_exceeded_time()

    totalChannels, totalVideos = 0, 0
    for channel in Channels.objects.all():
        try:
            url_ids = YoutubeCrud.getOrCreateChannelVideos(channel.channel_id)
            if len(url_ids)>0:
                url_ids = url_ids[:MAX_VIDEOS_HOME]
                stats_multi_video.apply_async((url_ids, ))
            totalVideos += len(url_ids)
            totalChannels+=1
        except Exception as e:
            if "Erreur de Quotas" in str(e):
                set_quotas_exceeded(True)
            return str(e)
    return "%d channels mise à jours, et %d videos" % (totalChannels, totalVideos)






@app.task
def update_channel(channel_id):
    totalVideos = 0
    try:
        url_ids = YoutubeCrud.getOrCreateChannelVideos(channel_id)
        if len(url_ids)>0:
            stats_multi_video.apply_async((url_ids, ))
        totalVideos += len(url_ids)
    except:pass

    return "%d videos mise à jours" % totalVideos









class thread_stats(threading.Thread):

    _video = None

    def __init__(self, video):
        threading.Thread.__init__(self)
        self._stopEvent = threading.Event()

        self._video = video


    def run(self):
        infos = VideoCrud.getInfos(self._video.url)

        viewCount=infos['view_count'] if 'view_count' in infos else 0
        likeCount=infos['like_count'] if 'like_count' in infos else 0
        dislikeCount=infos['dislike_count'] if 'dislike_count' in infos else 0
        commentCount=infos['comment_count'] if 'comment_count' in infos else 0
        repostCount=infos['repost_count'] if 'repost_count' in infos else 0

        VideoCrud.getOrCreateStat(video, viewCount, commentCount, repostCount, likeCount, dislikeCount)





@app.task
def stats_all_videos():
    threads = []
    nbVideos = 0
    for video in Videos.objects.order_by("-created_at").all():
        t = thread_stats(video)
        t.start()
        threads.append(t)
        nbVideos += 1
        if len(threads)>=NB_CORE:
            for t in threads:t.join()
            threads = []

    for t in threads:t.join()
    return "%d videos" % nbVideos




@app.task
def stats_video(url):
    try:
        video = Videos.object.get(url=url)
    except Videos.DoesNotExist:
        logger.warning("Video not found %s" % url)
        return "Video not found %s" % url

    t = thread_stats(video)
    t.start()
    t.join()
    return True
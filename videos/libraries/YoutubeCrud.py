from videos.libraries.YoutubeApi import YoutubeApi
from videos.models import *

from django.core.exceptions import *
from django.db import DatabaseError
from django.conf import settings

from app.exceptions import CrudError

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import datetime
import urllib
import logging
logger = logging.getLogger("libraries")

"""
 Model CRUD des videos youtube in database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""


class YoutubeCrud():




    @staticmethod
    def create(data):
        try:
            if 'url_id' not in data:
                raise FieldDoesNotExist("Not url_id")
            if 'url' not in data:
                raise FieldDoesNotExist("Not url")
            url = data.get("url")
            url_id = data.get("url_id")

            try:
                YtVideo = Videos.objects.get(url_id=url_id)
            except Videos.DoesNotExist:
                YtInfos = YoutubeApi.getInfosVideos(url_id)
                snippet = YtInfos['items'][0]['snippet']
                contentDetails = YtInfos['items'][0]['contentDetails']
                YtVideo = YoutubeCrud.getOrCreateVideo(url, url_id, snippet, contentDetails)

            return YtVideo


        except DatabaseError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e))







    @staticmethod
    def getOrCreateChannel(channel_id) -> Channels:
        try:
            YtChan = Channels.objects.get(channel_id=channel_id)
            return YtChan
        except Channels.DoesNotExist:

            YtInfos = YoutubeApi.getInfosChannels(channel_id)
            snippet = YtInfos['items'][0]['snippet']
            contentDetails = YtInfos['items'][0]['contentDetails']

            YtChan = Channels(channel_id=channel_id, title = snippet['title'],
                    description = snippet['description'],
                    published_at = snippet['publishedAt'])
            YtChan.save()

            # for YtPlay in contentDetails['relatedPlaylists']:
            #     YoutubeCrud.getOrCreatePlaylist(YtPlay['uploads'], YtChan)

            logger.debug("Channel %d created" % YtChan.id)
            return YtChan





    @staticmethod
    def getOrCreateChannelVideos(channel_id):
        YtChan = YoutubeCrud.getOrCreateChannel(channel_id)
        url_ids = list(map(lambda v:v.url_id, YtChan.videos.all()))
        YtVideos = YoutubeApi.getVideosChannel(channel_id, maxResults = 20)

        ids = []
        for item in YtVideos['items']:
            try:
                if not item['id']['videoId']:continue
                if item['id']['videoId'] not in url_ids:
                    ids.append(item['id']['videoId'])
            except:continue

        if len(ids)==0:return []

        step = 12
        for i in range(0, len(ids), step):

            try:
                YtVideos = YoutubeApi.getInfosVideosMulti(ids[i:i+step])
            except Exception as e:
                logger.warning(e)
                raise Exception(str(e))

            for item in YtVideos['items']:
                try:
                    url = "https://www.youtube.com/watch?v=%s" % item['id']
                    YoutubeCrud.getOrCreateVideo(url, item['id'], item['snippet'], item['contentDetails'])
                except:pass
        return ids




    @staticmethod
    def getOrCreatePlaylist(playlist_id, YtChan) -> Playlists:

        try:
            YtPlay = Playlists.objects.get(playlist_id=playlist_id)
            return YtPlay
        except Playlists.DoesNotExist:

            YtInfos = YoutubeApi.getInfosPlaylists(channel_id)
            snippet = YtInfos['items'][0]['snippet']

            YtPlay = Playlists(channel_id=channel_id, title = snippet['title'],
                    default_language = snippet['defaultLanguage'], description = snippet['description'],
                    published_at = snippet['publishedAt'], channel=YtChan)
            YtPlay.save()
            logger.debug("Playlist %d created" % YtPlay.id)
            return YtPlay




    @staticmethod
    def getOrCreateVideo(url, url_id, snippet, contentDetails) -> Videos:
        try:
            YtVideo = Videos.objects.get(url_id=url_id)
            return YtVideo
        except Videos.DoesNotExist:
            YtVideo = Videos(url_id=url_id, url=url,
            duration = datetime.datetime.strptime(contentDetails['duration'], "PT%MM%SS"),
            published_at = snippet['publishedAt'])

            if 'localized' in snippet:
                YtVideo.title = snippet['localized']['title']
                YtVideo.description = snippet['localized']['description'].encode('ascii', errors='ignore').decode("utf-8")
            else:
                YtVideo.title = snippet['title']
                YtVideo.description = snippet['description'].encode('ascii', errors='ignore').decode("utf-8")


            YtVideo.channel = YoutubeCrud.getOrCreateChannel(snippet['channelId'])
            YtVideo.save()


            if 'tags' in snippet:
                tags = list(map(lambda t:YoutubeCrud.getOrCreateTag(t), snippet['tags']))
                for tag in tags:YtVideo.tags.add(tag)

            for key, vals in snippet['thumbnails'].items():

                YtThumb = Thumbnails(width=vals['width'], height=vals['height'], url=vals['url'])
                YtThumb.video = YtVideo
                if key == "default":
                    YtThumb.dimension = Thumbnails.ThumbDimension.DEFAULT
                elif key == "low":
                    YtThumb.dimension = Thumbnails.ThumbDimension.LOW
                elif key == "high":
                    YtThumb.dimension = Thumbnails.ThumbDimension.HIGH
                elif key == "medium":
                    YtThumb.dimension = Thumbnails.ThumbDimension.MEDIUM
                elif key == "standard":
                    YtThumb.dimension = Thumbnails.ThumbDimension.STANDARD
                elif key == "maxres":
                    YtThumb.dimension = Thumbnails.ThumbDimension.MAXRES
                else:
                    YtThumb.dimension = Thumbnails.ThumbDimension.UNKNOW

                try:
                    fp = urllib.request.urlopen(vals['url'])
                    YtThumb.content = fp.read()
                    fp.close()
                    YtThumb.save()
                    logger.debug("Thumbnails %d created" % YtThumb.id)
                except Exception as e:
                    logger.warning("Thumbnails - %s" % e)
                finally:pass
            
            YtVideo.save()

            return YtVideo






    @staticmethod
    def getOrCreateTag(value) -> Tags:
        try:
            tag = Tags.objects.get(value=value)
            return tag
        except Tags.DoesNotExist:pass

        tag = Tags(value=value)
        tag.save()
        logger.debug("Tag %s created" % tag.value)
        return tag






    """
       Create video youtube
       And save channels, thumbnails and tags
     :param  data
     :return Videos
     
     :throws Throwable
    """








    """
       Read file
     :param  data
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def read(data):
        try:
            if 'video_id' in data:
                return Videos.objects.filter(id=data["video"]).first()
            if 'url_id' not in data:
                raise FieldDoesNotExist("Not url_id")

            if Videos.objects.filter(url_id=data['url_id']).count() == 0:
                raise ObjectDoesNotExist("Videos")
            
            return Videos.objects.filter(url_id=data['url_id']).first()

        except DatabaseError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e))







    """
       Update file
     :param  data
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def update(data):
        try:
            visitor = YoutubeCrud.read(data)
            return

        except DatabaseError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e))








    """
       Delete file
     :param  data
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def delete(data):
        try:
            YtVideo = YoutubeApi.read(data)
            YtVideo.delete()
            logger.info("Video %d deleted" % YtVideo.id)
        except DatabaseError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(YoutubeCrud.__class__.__name__, str(e))


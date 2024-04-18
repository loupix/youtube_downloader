from django.core.exceptions import *
from django.db import DatabaseError
from django.conf import settings

from app.exceptions import CrudError

from videos.models import *

from datetime import datetime
from django.utils import timezone

import urllib
import html
import yt_dlp as youtube_dl
import io, os, sys
from PIL import Image

import logging
logger = logging.getLogger("libraries")

import random, string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




"""
 Model CRUD des videos in database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""


class VideoCrud():





    @staticmethod
    def getInfos(url):
        ydl_opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'noplaylist': True,
            'nopart': False,
            "simulate": True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict



    @staticmethod
    def getInfosAudio(url):
        ydl_opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'noplaylist': True,
            'nopart': False,
            "simulate": True,
            "format": "bestaudio"
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict







    @staticmethod
    def getInfosVideo(url):
        ydl_opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'noplaylist': True,
            'nopart': False,
            "simulate": True,
            "format": "bestvideo"
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict







    @staticmethod
    def create(data) -> Videos:
        try:
            fields = ['url','url_id','website']
            for f in fields:
                if f not in data: raise FieldDoesNotExist(f)


            url = data.get("url")
            url_id = data.get("url_id")
            website = data.get("website")



            if data['website'] == "youtube":
                website = Videos.Website.YOUTUBE
            elif data['website']=="dailymotion":
                website = Videos.Website.DAILYMOTION
            elif data['website']=="vimeo":
                website = Videos.Website.VIMEO
            elif data['website']=="facebook":
                website = Videos.Website.FACEBOOK
            elif data['website']=="instagram":
                website = Videos.Website.INSTAGRAM
            elif data['website']=="odnoklassniki":
                website = Videos.Website.ODNOKLASSNIKI
            elif data['website']=="twitter":
                website = Videos.Website.TWITTER
            elif data['website']=="twitch":
                website = Videos.Website.TWITCH
            else:
                raise ObjectDoesNotExist("Website")

            infos = VideoCrud.getInfos(url)


            try:
                video = Videos.objects.get(website=website, url=url)
            except Videos.DoesNotExist:

                infos['upload_date'] = datetime.strptime(infos['upload_date'],"%Y%m%d").replace(tzinfo=timezone.utc)
                infos['duration'] = datetime.utcfromtimestamp(infos['duration']).time()

                if 'description' in infos:
                    infos['description'] = infos['description'].encode('ascii', 'xmlcharrefreplace').decode("utf-8")
                else:
                    infos['description'] = None

                infos['title'] = infos['title'].encode('ascii', 'xmlcharrefreplace').decode("utf-8")

                video = Videos(id=id_generator(7), url=url, url_id=url_id, website=website,
                    title=infos['title'], description=infos['description'],
                    duration=infos['duration'], published_at=infos['upload_date'])
                video.save()

                sys.stderr.write("\n%s" % video)


                viewCount=infos['view_count'] if 'view_count' in infos else 0
                likeCount=infos['like_count'] if 'like_count' in infos else 0
                dislikeCount=infos['dislike_count'] if 'dislike_count' in infos else 0
                commentCount=infos['comment_count'] if 'comment_count' in infos else 0
                repostCount=infos['repost_count'] if 'repost_count' in infos else 0
                
                VideoCrud.getOrCreateStat(video, viewCount, commentCount, repostCount, likeCount, dislikeCount)

            save=False
            for formatDict in infos['formats']:
                
                format_video = VideoCrud.getOrCreateFormat(formatDict)
                if format_video and format_video not in video.formats.all():
                    save=True
                    video.formats.add(format_video)

                # if 'url' in formatDict:
                #     f_url = VideoCrud.getOrCreateFormatUrl(video, format_video, formatDict)
                #     if f_url not in video.format_urls.all():
                #         save=True
                #         video.format_urls.add(f_url)

            if save:video.save()
            save=False
            
            for thumbnail in infos['thumbnails']:
                VideoCrud.getOrCreateThumbnail(video, thumbnail)

            if 'tags' in infos:
                for val in infos['tags']:
                    t = VideoCrud.getOrCreateTag(val)
                    if t not in video.tags.all():
                        save=True
                        video.tags.add(t)

            if save:video.save()


            return video


        except DatabaseError as e:
            raise CrudError(VideoCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(VideoCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(VideoCrud.__class__.__name__, str(e))












    @staticmethod
    def read(video_id):
        try:
            video = Videos.objects.get(id=video_id)
            return video
        except Videos.DoesNotExist:
            raise ObjectDoesNotExist("Video %s Not Found" % video_id)














    @staticmethod
    def getOrCreateFormat(formatDict) -> Formats:
        try:
            format_obj = Formats.objects.get(format_id=formatDict['format_id'])
        except Formats.DoesNotExist:

            formatDict['height'] = formatDict['height'] if 'height' in formatDict else 0
            formatDict['width'] = formatDict['width'] if 'width' in formatDict else 0

            format_obj = Formats(name=formatDict['format'], format_id=formatDict['format_id'],
                width=formatDict['width'], height=formatDict['height'])

            if 'format_note' in formatDict:
                format_obj.format_note = formatDict['format_note']
            if 'quality' in formatDict:
                format_obj.quality = formatDict['quality']
            if 'ext' in formatDict:
                format_obj.ext = formatDict['ext']
            if 'fps' in formatDict:
                format_obj.fps = formatDict['fps']
            if 'acodec' in formatDict:
                format_obj.acodec = formatDict['acodec']
            if 'vcodec' in formatDict:
                format_obj.vcodec = formatDict['vcodec']
            if 'asr' in formatDict:
                format_obj.asr = formatDict['asr']
            if 'tbr' in formatDict:
                format_obj.tbr = formatDict['tbr']
            if 'container' in formatDict:
                format_obj.container = formatDict['acodec']

            if 'format_note' not in formatDict and formatDict['height']>0:
                format_obj.format_note = "%dp" % formatDict['height']

            format_obj.save()

        return format_obj










    @staticmethod
    def getOrCreateFormatUrl(video, format_video, formatDict) -> Format_urls:
        try:
            format_url = Format_urls.objects.get(url=formatDict['url'], video=video)
        except Format_urls.DoesNotExist:
            format_url = Format_urls(format_video=format_video, video=video, url=formatDict['url'])
            format_url.save()
        return format_url




    @staticmethod
    def getOrCreateThumbnail(video, thumbnail) -> Thumbnails:
        url = thumbnail['url']
        try:
            thumb = Thumbnails.objects.get(url=url, video=video)
        except Thumbnails.DoesNotExist:

            thumb = Thumbnails(url=url, video=video)

            fp = urllib.request.urlopen(url)
            image_data = fp.read()
            fp.close()

            thumb.content = image_data

            image = Image.open(io.BytesIO(image_data))

            thumb.width = thumbnail['width'] if "width" in thumbnail else image.width
            thumb.height = thumbnail['height'] if "height" in thumbnail else image.height


            thumb.save()

        return thumb




    @staticmethod
    def getOrCreateTag(value) -> Tags:
        try:
            tag = Tags.objects.get(value=value)
        except Tags.DoesNotExist:
            tag = Tags(value=value)
            tag.save()
        return tag





    @staticmethod
    def getOrCreateStat(video, viewCount=0, commentCount=0, repostCount=0, likeCount=0, dislikeCount=0) -> Statistique:
        stat = Statistique.objects.filter(video=video, views=viewCount, commentaires=commentCount, 
            reposts=repostCount, likes=likeCount, dislikes=dislikeCount).last()
        if not stat:
            stat = Statistique(video=video, views=viewCount, commentaires=commentCount, 
                reposts=repostCount, likes=likeCount, dislikes=dislikeCount)
            stat.save()

        return stat




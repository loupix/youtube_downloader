from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from math import *

from django.conf import settings
from django.core import serializers
from django.core.exceptions import *
from django.db.models import Count, Sum

from .libraries import *
from .models import * 


import json
from datetime import datetime, timedelta
import yt_dlp as youtube_dl


import logging
logger = logging.getLogger("views")


MAX_VIDEOS_HOME = 20



def error_response(message, status, error=None):
    response = dict()
    response["error"] = error
    response["status"] = status
    response["detail"] = message

    return JsonResponse(response, status=status)




def check_url(request):
	if request.method != "POST":raise ValidationError({"Method":"not post"})
	if "video_id" not in request.POST:raise ValidationError({"POST":"video_id"})
	return JsonResponse({'check':YoutubeCrud.check_youtube_url(request.post.get("video_id"))})
	return






def videos(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "number_per_page" not in data:
			raise FieldDoesNotExist("number_per_page")
		if "page_number" not in data:
			raise FieldDoesNotExist("page_number")
		if "filter_order" not in data:
			raise FieldDoesNotExist("filter_order")

		limit = data.get("number_per_page")
		offset = data.get("page_number")*limit
		filter_order = data.get("filter_order")

		nbVideos = Videos.objects.count()
		if filter_order=="lastDownloaded":
			videos = Videos.objects.order_by("-created_at")
		elif filter_order=="lastPublished":
			videos = Videos.objects.order_by("-published_at")
		elif filter_order=="mostDownloaded":
			videos = Videos.objects.annotate(sum_downloads=Sum("downloads__number_download")).order_by("-sum_downloads")
		videos = videos.annotate(nb_thumbnails=Count("thumbnails")).exclude(nb_thumbnails=0).all()
		videos = videos[offset:offset+limit]
		
		videos = list(map(lambda d:d.json(facials=False, stats=True), videos))

		dataTable = {'page_number':data['page_number'], 'number_per_page':data['number_per_page'], 
			'total_page':ceil(nbVideos/limit), 'data':videos}

		return JsonResponse(dataTable, safe=False)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return HttpResponse(e, status=400)
	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)







def infos(request):
	formats = []
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "url" not in data:
			raise FieldDoesNotExist("url")

		ydl_opts = {
			'nocheckcertificate': True,
			'quiet': True,
			'noplaylist': True,
			'nopart': False,
			"simulate": True,
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info_dict = ydl.extract_info(data['url'], download=False)
			upDate = datetime.strptime(info_dict['upload_date'],"%Y%m%d")
			info_dict['upload_date'] = upDate.timestamp()			

		return JsonResponse(info_dict, safe=False)

	except youtube_dl.utils.DownloadError as e:
		logger.error(e)
		return HttpResponse(e, status=502)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return HttpResponse(e, status=400)
	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)









def statistics_videos(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "video_id" not in data:
			raise FieldDoesNotExist("video_id")

		try:
			video = Videos.objects.get(id=data.get("video_id"))
		except Videos.DoesNotExist:
			return error_response("Video not exist", status=404)


		now = datetime.utcnow().replace(tzinfo=utc)
		deltaTime = now - timedelta(days=nb_days)

		statistiques = video.statistics.filter(created_at__lte = deltaTime).order_by("-created_at")
		stats = list(map(lambda s:s.json(), statistiques.all()))
		return JsonResponse(stats, safe=False)

	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response(e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response(e, status=500)









def statistics_channels(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "channel_id" not in data:
			raise FieldDoesNotExist("channel_id")


		try:
			channel = Channels.objects.get(id=data.get("channel_id"))
		except Channels.DoesNotExist:
			return error_response("Channel not exist", status=404)


		now = datetime.utcnow().replace(tzinfo=utc)
		deltaTime = now - timedelta(days=nb_days)

		statistiques = channel.statistics.filter(created_at_lte = deltaTime).order_by("-created_at")
		stats = list(map(lambda s:s.json(), statistiques.all()))
		return JsonResponse(stats, safe=False)

	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response(e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response(e, status=500)





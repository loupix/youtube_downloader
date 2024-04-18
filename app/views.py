from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from math import *

from django.conf import settings

from django.core import serializers
from django.core.exceptions import *
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.db.models import Count, Sum, Max, Avg

from django.views.decorators.csrf import csrf_exempt

from django.utils.translation import activate, get_language


from app.libraries import VisitorCrud, QueueCrud, LocationCrud, DownloadCrud
from app.tasks import *
from app.models import Downloaded

from videos.libraries import VideoCrud
from videos.models import Videos 


import json
from datetime import datetime, timedelta


import logging
logger = logging.getLogger("views")



def on_raw_message(body):
    print(body)





def home(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

		delete_video_downloaded.apply_async()
		download_video_none.apply_async()

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)

		limit = 8
		videos = Videos.objects.order_by("-created_at")
		videos = videos.annotate(nb_thumbnails=Count("thumbnails")).exclude(nb_thumbnails=0).all()
		videos = videos[:limit]


		return render(request, 'pages/home.html', 
			{'header': {'controller':'homeCtrl', 'class':'home'} ,
			'navbar':{'visitor':v, "queue":q},
			'videos':videos,
			'nbLoadVideos':range(limit)})
	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)







def top10(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)

		return render(request, 'pages/top10.html',
			{'header': {'controller':'topCtrl', 'class':'top text-white', 'title':'Top 10 - Youtube Downloader'},
		 	'navbar':{'visitor':v, "queue":q},
		 	'nTemp':range(10)})
	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)






def history(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)

		return render(request, 'pages/historique.html', 
			{'header': {'controller':'historyCtrl', 'class':'history', 'title':'History - Youtube Downloader'},
			'navbar':{'visitor':v, "queue":q}})

	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)










def statistique(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)

		return render(request, 'pages/statistique.html', 
			{'header': {'controller':'statistiqueCtrl', 'class':'statistique'},
			'navbar':{'visitor':v, "queue":q}})

	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)









def video(request, video_id):


	if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

	try:
		visitor = VisitorCrud.create(request)
		queue = QueueCrud.create(request)
		video = VideoCrud.read(video_id)

		frame_list = []
		nb_by_frame = 6
		for i in range(0, video.frames.count(), nb_by_frame):
			frame_list.append([f for f in video.frames.all()[i:i+nb_by_frame]])
		


		return render(request, 'pages/video.html', 
			{'header': {'controller':'videoCtrl', 'class':'video', 'title':video.title},
			'navbar':{'visitor':visitor, "queue":queue},
			'frame_list':frame_list,
			'video':video})

	except (ObjectDoesNotExist, FieldDoesNotExist) as e:
		return render(request, 'pages/video.html', 
			{'header': {'controller':'videoCtrl', 'class':'video'},
			'navbar':{'visitor':visitor, "queue":queue},
			'video':None, 'error':str(e)})

	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)












def audio(request, video_id):

	if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

	try:
		visitor = VisitorCrud.create(request)
		queue = QueueCrud.create(request)
		video = VideoCrud.read({'video_id':video_id})
		


		return render(request, 'pages/video.html', 
			{'header': {'controller':'videoCtrl', 'class':'video', 'title':video.title},
			'navbar':{'visitor':visitor, "queue":queue},
			'ntemp': 10,
			'video':video.json()})

	except (ObjectDoesNotExist, FieldDoesNotExist) as e:
		return render(request, 'pages/video.html', 
			{'header': {'controller':'videoCtrl', 'class':'video'},
			'navbar':{'visitor':visitor, "queue":queue},
			'video':None, 'error':str(e)})

	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)













def change_lang(request, lang = None, * args, ** kwargs):
	cur_language = get_language()
	try:
		activate(lang)
		request.LANGUAGE_CODE = get_language()
		request.session['django_language'] = lang
		request.session.save()
	finally:
		activate(cur_language)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





















###################################
##############  API   #############
###################################














def getHistory(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "number_per_page" not in data:
			raise FieldDoesNotExist("number_per_page")
		if "page_number" not in data:
			raise FieldDoesNotExist("page_number")

		visitor_id = request.session.get("visitor_id")
		try:
			visitor = Visitors.objects.get(id=visitor_id)
		except Visitors.DoesNotExist:
			raise ObjectDoesNotExist("visitor")
			
		values = Downloaded.objects.filter(visitors_in=visitor).all().order_by("-created_at").exclude(video__isnull=True)

		return JsonResponse(list(map(lambda d:d.json(), values)), safe=False)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return HttpResponse(e, status=400)
	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)













def getTop(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "limit" not in data:
			limit = 3
		else:
			limit = data.get("limit")


		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)

		visitor_id = request.session.get("visitor_id")
		values = Downloaded.objects.filter(created_at__gte=(datetime.now() - timedelta(days=7))).all()
		values = values.values("video_id").annotate(total=Count('id')).order_by('-total')


		videos = Videos.objects.filter(id__in=list(map(lambda d:d['video_id'], values))).all()

		rep = []
		videos_id = []
		video_queue_ids = list(map(lambda d:d.video_id, q.downloads.all()))
		for value in values.values():
			if not value['video_id']:continue
			video = videos.filter(id=value['video_id'])

			if video.count()==0:continue
			video = video.first()

			if video.id in videos_id:
				rep[videos_id.index(video.id)]['total'] += value['total']
			else:
				videos_id.append(video.id)
				video = video.json()
				video['total'] = value['total']
				video['download'] = False
				video['downloaded'] = video['id'] in video_queue_ids
				rep.append(video)
		rep.sort(key=lambda v:v['total'], reverse=True)

		if len(rep)>=limit:
			rep = rep[:limit]

		return JsonResponse(list(rep), safe=False)
	except Exception as e:
		logger.error(e)













def getStats(request):
	try:
		return JsonResponse()
	except Exception as e:
		return(409)







###################################
###########  Queue Api   ##########
###################################





def getQueue(request):
	try:
		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)
		return JsonResponse(q.json(), safe=False)

	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return HttpResponse(e, status=400)
	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)













def addQueue(request):
	try:
		data = json.loads(request.body.decode('utf-8'))

		fields = ['format_type','filename','youtube_id']
		for f in fields:
			if f not in data: raise FieldDoesNotExist(f)

		format_type = data.get("format_type")
		filename = data.get("filename")
		youtube_id = data.get("youtube_id")

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)


		if format_type=="audio":
			format_file = "bestaudio"
			format_type = Downloaded.Format.AUDIO
		elif format_type=="video":
			format_file = "best"
			format_type = Downloaded.Format.VIDEO
		else:
			format_file = "best"

		downloaded = DownloadCrud.create({
			'percent': 0,
			'filename': filename,
			'youtube_id': youtube_id,
			'path': settings.MEDIA_ROOT+filename,
			'visitor_id': request.session.get("visitor_id"),
			'format_file':format_file,
			'format_type':format_type,
			'status': Downloaded.Status.PENDING,
		})

		downloaded.video = Videos.objects.filter(youtube_id=youtube_id).first()
		downloaded.save()

		q.downloads.add(downloaded)
		q.save()

		return JsonResponse(downloaded.json(), safe=False)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return HttpResponse(e, status=400)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return HttpResponse(e, status=404)
	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)
import json
from datetime import datetime, timedelta
from math import *

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.utils.translation import activate, get_language
from django.contrib.auth.decorators import login_required, permission_required


from django.conf import settings

from django.core import serializers
from django.core.exceptions import *

from app.libraries import VisitorCrud, QueueCrud, LocationCrud, DownloadCrud
from videos.models import Videos
from .models import *

import logging
logger = logging.getLogger("views")






def error_response(message, status, error=None):
    response = dict()
    response["error"] = error
    response["status"] = status
    response["detail"] = message

    return JsonResponse(response, status=status)




@login_required
def index(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])



		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)


		ids = Faces.objects.all().values("video_id").distinct()
		ids = list(map(lambda d:d['video_id'], ids))
		videos = Videos.objects.filter(id__in=ids).order_by("-published_at").all()
		# videos = list(map(lambda v:v.json(), videos))

		return render(request, 'index.html', 
			{'header': {'controller':'facialCtrl', 'class':'history'},
			'body':{'videos':videos},
			'navbar':{'visitor':v, "queue":q}})

	except Exception as e:
		print(e)
		logger.error(e)
		return HttpResponse(e, status=500)










def videos(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "number_per_page" not in data:
			raise FieldDoesNotExist("number_per_page")
		if "page_number" not in data:
			raise FieldDoesNotExist("page_number")


		limit = data['number_per_page']
		offset = data['page_number'] * data['number_per_page']


		ids = Sequences.objects.all().values("video_id").distinct()
		ids = list(map(lambda d:d['video_id'], ids))
		nbVideos = Videos.objects.filter(id__in=ids).count()
		videos = Videos.objects.filter(id__in=ids).order_by("-published_at").all()[offset:offset+limit]
		videos = list(map(lambda d:d.json(facials=True), videos))

		dataTable = {'page_number':data['page_number'], 'number_per_page':data['number_per_page'], 
			'total_page':ceil(nbVideos/limit), 'data':videos}

		return JsonResponse(dataTable, safe=False)

	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)








def removeVideo(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "video_id" not in data:
			raise FieldDoesNotExist("video_id")

		for seq in Sequences.objects.filter(video_id=data.get('video_id')).all():
			for face in seq.faces.all():
				try:
					face.delete()
				except:pass
			try:
				seq.delete()
			except:pass

	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)
















def sequences(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "number_per_page" not in data:
			raise FieldDoesNotExist("number_per_page")
		if "page_number" not in data:
			raise FieldDoesNotExist("page_number")
		if "video_id" not in data:
			raise FieldDoesNotExist("video_id")


		limit = data['number_per_page']
		offset = data['page_number'] * data['number_per_page']


		try:
			video = Videos.objects.get(id=data['video_id'])
		except Videos.DoesNotExist as e:
			raise FieldDoesNotExist("Video Object")

		nbSequences = Sequences.objects.filter(video=video).count()
		sequences = Sequences.objects.filter(video=video).all()[offset:offset+limit]
		sequences = list(map(lambda d:d.json(), sequences))

		dataTable = {'page_number':data['page_number'], 'number_per_page':data['number_per_page'], 
			'total_page':ceil(nbSequences/limit), 'data':sequences}

		return JsonResponse(dataTable, safe=False)

	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)








def removeSequence(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "visitor_id" not in request.session:
			raise FieldDoesNotExist("visitor_id")
		if "sequence_id" not in data:
			raise FieldDoesNotExist("sequence_id")

		sequence = Sequences.objects.get(id=data.get("sequence_id"))
		for face in sequence.faces.all():
			try:
				face.delete()
			except:pass
		try:
			sequence.delete()
		except:pass

	except Sequences.DoesNotExist:
		return error_response("Sequence Not Found", status=404)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)





















def tags(request):
	tags = list(map(lambda t:t.json(), Tags.objects.filter(show=True).all()))
	return JsonResponse(tags, safe=False)








def newTags(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "tag_value" not in data:
			raise FieldDoesNotExist("tag_value")

		try:
			tag = Tags.objects.get(value=data['tag_value'])
			tag.show = True
			tag.save()
		except Tags.DoesNotExist:
			tag = Tags(value=data['tag_value'])
			tag.save()


		return JsonResponse(tag.json(), safe=False)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)





def addTags(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "sequence_id" not in data:
			raise FieldDoesNotExist("sequence_id")
		if "tag_value" not in data:
			raise FieldDoesNotExist("tag_value")

		try:
			tag = Tags.objects.get(value=data['tag_value'])
			if not tag.show:
				tag.show = True
				tag.save()
		except Tags.DoesNotExist:
			tag = Tags(value=data['tag_value'])
			tag.save()

		try:
			sequence = Sequences.objects.get(id=data['sequence_id'])
		except Tags.DoesNotExist:
			raise FieldDoesNotExist("Sequence Object")

		if tag not in sequence.tags.all():
			sequence.tags.add(tag)
			sequence.save()

		return JsonResponse({'error':False})
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)










def delTags(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if "sequence_id" not in data:
			raise FieldDoesNotExist("sequence_id")
		if "tag_value" not in data:
			raise FieldDoesNotExist("tag_value")

		try:
			tag = Tags.objects.get(value=data['tag_value'])
			if not tag.show:
				tag.show = True
				tag.save()
		except Tags.DoesNotExist:
			tag = Tags(value=data['tag_value'])
			tag.save()


		try:
			sequence = Sequences.objects.get(id=data['sequence_id'])
		except Tags.DoesNotExist:
			raise FieldDoesNotExist("Sequence Object")

		if tag in sequence.tags.all():
			sequence.tags.remove(tag)
			sequence.save()

		return JsonResponse({'error':False})


		return
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)





def removeTags(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		if 'tag_id' not in data:raise FieldDoesNotExist("tag_id")
		tag_id = data.get("tag_id")
		tag = Tags.objects.get(id=tag_id)
		tag.show = False;
		tag.save()
		return JsonResponse(tag.json(), safe=False)
	except Tags.DoesNotExist as e:
		logger.warning("Tags DoesNotExist %s" % e)
		return error_response("Tags DoesNotExist %s" % e, status=404)
	except FieldDoesNotExist as e:
		logger.warning("FieldDoesNotExist %s" % e)
		return error_response("FieldDoesNotExist %s" % e, status=400)
	except Exception as e:
		logger.error(e)
		return error_response("%s" % e, status=500)














def groups(request):
	groupes = list(map(lambda g:g.json(), Groups.objects.all()))
	return JsonResponse(groupes, safe=False)




def newGroups(request):
	data = json.loads(request.body.decode('utf-8'))
	if "group_value" not in data:return error_response("group_value DoesNotExist", status=400)
	group_value = data.get("group_value")

	try:
		group = Groups.objects.get(value=group_value)
	except Groups.DoesNotExist:
		group = Groups(value=group_value)
		group.save()

	return JsonResponse(group.json(), safe=False)




def addGroups(request):
	data = json.loads(request.body.decode('utf-8'))
	if "group_id" not in data:return error_response("group_id DoesNotExist", status=400)
	if "tag_id" not in data:return error_response("tag_id DoesNotExist", status=400)
	
	group_id = data.get("group_id")
	tag_id = data.get("tag_id")

	try:
		group = Groups.objects.get(id=group_id)
		tag = Tags.objects.get(id=tag_id)
		if tag not in group.tags.all():
			group.tags.add(tag)
			group.save()

		return JsonResponse(group.json(), safe=False)
	except Groups.DoesNotExist:
		return error_response("group not found", status=404)
	except Tags.DoesNotExist:
		return error_response("tag not found", status=404)





def delGroups(request):
	data = json.loads(request.body.decode('utf-8'))
	if "group_id" not in data:return error_response("group_id DoesNotExist", status=400)
	if "tag_id" not in data:return error_response("tag_id DoesNotExist", status=400)
	
	group_id = data.get("group_id")
	tag_id = data.get("tag_id")

	try:
		group = Groups.objects.get(id=group_id)
		tag = Tags.objects.get(id=tag_id)
		if tag in group.tags.all():
			group.tags.remove(tag)
			group.save()

		return JsonResponse(group.json(), safe=False)
	except Groups.DoesNotExist:
		return error_response("group not found", status=404)
	except Tags.DoesNotExist:
		return error_response("tag not found", status=404)






def removeGroups(request):
	data = json.loads(request.body.decode('utf-8'))
	if "group_id" not in data:return error_response("group_id DoesNotExist", status=400)

	group_id = data.get("group_id")

	try:
		group = Groups.objects.filter(id=group_id).first()
		for tag in group.tags.all():
			group.tags.remove(tag)
		group.save()
		group.delete()
		return JsonResponse(True, safe=False)
	except Groups.DoesNotExist:
		return error_response("group not found", status=404)
	except Tags.DoesNotExist:
		return error_response("tag not found", status=404)



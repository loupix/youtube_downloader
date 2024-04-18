from django.shortcuts import render

# Create your views here.



def index(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)

		return render(request, 'pages/vocals.html', 
			{'header': {'controller':'vocalCtrl', 'class':'vocal'},
			'navbar':{'visitor':v, "queue":q}})

	except Exception as e:
		print(e)
		return HttpResponse(e, status=500)
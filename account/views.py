from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.translation import activate, get_language

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from app.libraries import VisitorCrud, QueueCrud
from .admin import UserCreationForm

import os, sys, json

import logging
logger = logging.getLogger("views")



def login(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)

		if request.method == "POST":
			form = AuthenticationForm(request, data=request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				if user is not None:
					login(request, user)
					messages.info(request, f"You are now logged in as {username}.")
					return redirect("main:homepage")
				else:
					messages.error(request,"Invalid username or password.")
			else:
				messages.error(request,"Invalid username or password.")

		return render(request, 'login.html', 
			{'header': {'controller':'loginCtrl', 'class':'login', 'title':"Login - Youtube Downloader"},
			'form':{'login':AuthenticationForm(), 'registration':UserCreationForm()},
			'navbar':{'visitor':v, "queue":q}})

	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)










def register(request):
	try:
		if 'django_language' in request.session:
			request.LANGUAGE_CODE = request.session['django_language'];
			activate(request.session['django_language'])

		v = VisitorCrud.create(request)
		q = QueueCrud.create(request)


		if request.method == "POST":
			print(request.GET)
			print(request.POST)
			print(json.loads(request.read(), strict=False))
			print(request.readline())
			form = UserCreationForm(request.body)
			print(form)
			print(form.is_valid())
			print(form.clean_password2())
			if form.is_valid():
				user = form.save()
				if user is not None:
					login(request, user)
					messages.info(request, f"You are now logged in as {username}.")
					return redirect("main:homepage")
				else:
					messages.error(request,"Invalid username or password.")
			else:
				messages.error(request,"Invalid username or password.")

		return render(request, 'register.html', 
			{'header': {'controller':'registerCtrl', 'class':'register'},
			'form':{'login':AuthenticationForm(), 'registration':UserCreationForm(MyUser())},
			'navbar':{'visitor':v, "queue":q}})

	except Exception as e:
		logger.error(e)
		return HttpResponse(e, status=500)







def logout(request):
	request.session.clear()
	request.session.flush()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


from django.urls import include, path, re_path

import facials.views
import vocals.views

from . import views
from .channels import *

urlpatterns = [
    path('', views.home, name='home'),
    path('v/<str:video_id>', views.video, name='video'),
    path('a/<str:video_id>', views.audio, name='audio'),
    path('top10/', views.top10, name='top10'),
    path('history/', views.history, name='history'),
    path('statistique/', views.statistique, name='statistique'),
    path('facials/', facials.views.index, name='facials'),
    path('vocals/', vocals.views.index, name='vocals'),
    path('change_lang/<str:lang>', views.change_lang, name='change_lang'),

    path('api/', include([
        path('getHistory/', views.getHistory, name='getHistory'),
        path('getTop/', views.getTop, name='getTop'),
        path('getStats/', views.getStats, name='getStats'),
        path('addQueue/', views.addQueue, name='addQueue'),
        path('getQueue/', views.getQueue, name='getQueue'),
    ])),
]


websocket_urlpatterns = [
    # path(r'^ws/chat/(?P<room_code>\w+)/$', AppChannels.as_asgi()),
    # path('ws/test/', TestConsumer.as_asgi()),
    path('ws/downloads/', DownloadChannels.as_asgi()),
]
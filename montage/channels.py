from django.conf import settings
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.consumer import SyncConsumer

import json, sys, re, os
import youtube_dl
import urllib

import logging
logger = logging.getLogger("channels")
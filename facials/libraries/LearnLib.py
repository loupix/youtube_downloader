import json, sys, re, os, io
from datetime import datetime, timedelta, date
from math import *

import yt_dlp as youtube_dl
import cv2

import logging
logger = logging.getLogger("libraries")

from youtubeDownload.settings import BASE_DIR
from videos.models import Videos
from facials.models import *


class LearnLib:
	_now = datetime.now()


	def allTagsSample():
		sample = []
		for seq in Sequences.objects.all():
			for tag in seq.tags.all():
				sample.extends([{'tag':tag.value, 'face':np.fromstring(face.contentDecoded, np.uint8)} for face in seq.faces.all()])
		return sample



	def getTagsSample(tag_id):
		try:
			tag = Tags.objects.get(tag_id)
			sample = []
			for tag in seq.tags.all():
				sample.extends([{'tag':tag.value, 'face':np.fromstring(face.contentDecoded, np.uint8)} for face in seq.faces.all()])
			return sample
		except Tags.DoesNotExist:
			return []


	@staticmethod
	def allGroupsFaces():
		groupSample = []
		for group in Groups.objects.all():
			sample = []
			for tag in group.tags.all():
				for tag in tag.sequences.all():
					sample.extends([{'tag':tag.value, 'face':np.fromstring(face.contentDecoded, np.uint8)} for face in seq.faces.all()])
			groupSample.append({'group_label':group.label, "sample":sample})
		return groupSample



	@staticmethod
	def getGroupsFaces(groupe_id):
		try:
			group = Groups.objects.get(id=group_id)
			sample = []
			for tag in group.tags.all():
				for tag in tag.sequences.all():
					sample.extends([{'tag':tag.value, 'face':np.fromstring(face.contentDecoded, np.uint8)} for face in seq.faces.all()])
			return sample
		except Groups.DoesNotExist:
			return []



	@staticmethod
	def genModel(sample):
		recognizer = cv2.face.LBPHFaceRecognizer_create()
		recognizer.train(faceSamples, np.array(Ids))

		return recognizer.save()



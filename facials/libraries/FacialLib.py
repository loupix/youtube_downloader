import json, sys, re, os, io
from datetime import datetime, timedelta, date
from math import *
import yt_dlp as youtube_dl
import cv2

import logging
logger = logging.getLogger("libraries")

from django.db import transaction, IntegrityError


from youtubeDownload.settings import BASE_DIR
from videos.models import Videos
from facials.models import *

VIDEO_DIR = os.path.join(str(BASE_DIR),"tmp","videos")
FACE_DIR = os.path.join(str(BASE_DIR),"tmp","faces")
HAAR_DIR = os.path.join(str(BASE_DIR),"opencv","data","haarcascades")


class FacialLib:
	_now = datetime.now()

	if not os.path.exists(VIDEO_DIR):os.makedirs(VIDEO_DIR)
	if not os.path.exists(FACE_DIR):os.makedirs(FACE_DIR)
	if not os.path.exists(HAAR_DIR):sys.exit("No OpenCV Directory")







	"""
		Download Video File
		:param  String youtube_id
		:return String video_file

		:throws Throwable
	"""
	@staticmethod
	def download(url):
		try:
			ydl_opts = {
				'outtmpl': os.path.join(VIDEO_DIR, '%(id)s_%(format_id)s.%(ext)s'),
				'nocheckcertificate': True,
				'quiet': True,
				'noplaylist': True,
				'nopart': False,

				# "simulate": True,
				# 'ignoreerrors': True,
				'format': "bestvideo[ext=webm][height<=720]",
				# 'logger': MyLogger(self, self.socket, self.downloaded),
				# 'progress_hooks': [self._my_hook],
				# 'print_json': True
			}


			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.cache.remove()
				info_dict = ydl.extract_info(url, download=False)
				ydl.prepare_filename(info_dict)
				ydl.download([url])

			video_file = os.path.join(VIDEO_DIR, "%s_%s.%s" % (info_dict['id'], info_dict['format_id'], info_dict['ext']))
			
			return video_file

		except youtube_dl.utils.DownloadError as e:
			raise Exception(str(e))
		except Exception as e:
			raise Exception(str(e))









	"""
		Extract faces & Save BDD
		:param  String video_file
		:param  Videos video
		:return Array face_dbs
		:return Integer nbNewFaces

		:throws Throwable
	"""
	@staticmethod
	def extractFaces(video_file, video):
		face_cascade = cv2.CascadeClassifier(os.path.join(HAAR_DIR,'haarcascade_frontalface_default.xml'))

		vidcap = cv2.VideoCapture(video_file)
		fps = vidcap.get(cv2.CAP_PROP_FPS)

		width  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)

		calc_timestamps = 0.0
		nbNewFaces = 0

		now = datetime.now()

		face_dbs = []
		face_to_db = []
		# face_in_db = Faces.objects.filter(video=video).all()
		# face_in_db_ann = list(map(lambda f:(f.x, f.y, f.width, f.height, f.time_at), face_in_db))
		while vidcap.isOpened():
			success,image = vidcap.read()

			if not success:break
			if (datetime.now() - now).total_seconds() >= (30*60):break


			timestamp = datetime.utcfromtimestamp(vidcap.get(cv2.CAP_PROP_POS_MSEC)/1000)
			timestamp = timestamp.time()
			calc_timestamps = calc_timestamps + 1000/fps

			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			for (x,y,w,h) in faces:
				roi_color = image[y:y+h, x:x+w]
				image_bytes = cv2.imencode('.jpg', roi_color)[1].tobytes()

				# Save BDD
				# if (x,y,w,h,timestamp) in face_in_db_ann:
				# 	faceObj = face_in_db[face_in_db_ann.index.index((x,y,w,h,timestamp))]
				# 	continue

				try:
					faceObj = Faces.objects.get(video=video, x=x, y=y, width=w, height=h, time_at=timestamp)
				except Faces.DoesNotExist:
					faceObj = Faces(video=video, 
						x=x, y=y, width=w, height=h, 
						x_rel=(x*100/width), y_rel=(y*100/height), width_rel=(w*100/width), height_rel=(h*100/height), 
						time_at=timestamp, content=image_bytes)
					face_to_db.append(faceObj)
					nbNewFaces+=1

				face_dbs.append(faceObj)

			
			with transaction.atomic():
				for faceObj in face_to_db:faceObj.save()
				face_to_db = []

			# sys.stdout.write("\r%s - %d Faces - %d New - Success %s" % ((datetime.now() - FacialLib._now), len(face_dbs), nbNewFaces, success))

		vidcap.release()
		return face_dbs, nbNewFaces














	"""
		Générate séquences from facials & Save BDD
		:param  Array face_dbs
		:param  Videos video
		:return Array sequence_dbs

		:throws Throwable
	"""
	@staticmethod
	def extractSequences(face_dbs, video):

		video_file = os.path.join(VIDEO_DIR, "%s.%s" % (video.youtube_id, "webm"))

		vidcap = cv2.VideoCapture(video_file)
		fps = vidcap.get(cv2.CAP_PROP_FPS)

		width  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)


		# Init First Face
		last_time = face_dbs[0].time_at
		same_faces = [
			{'time':last_time, 'faces':[face_dbs[0]]}
		]

		# Boucle le reste
		for face in face_dbs[1:]:
			if last_time == face.time_at:
				same_faces[-1]['faces'].append(face)
			else:
				same_faces.append({'time':face.time_at, 'faces':[face]})
				last_time = face.time_at

		# import pprint
		# pprint.pprint(same_faces)


		###  Creation des séquences ###


		nbNewSequences = 0
		nbFaces = 0

		max_diff_time = 250
		max_distance = 5
		max_distance_rel = 1

		sequences = []
		sequence_dbs = []

		## Init first séquence

		last_faces = same_faces[0]
		last_sequences = []
		for face in last_faces['faces']:
			seq = Sequences.objects.filter(faces__in=[face]).last()
			if not seq:
				seq = Sequences.objects.create(video=video,
					startTime=last_faces['faces'][0].time_at,
					endTime=last_faces['faces'][0].time_at)
				seq.faces.add(face)
			sequence_dbs.append(seq)
			last_sequences.append(seq)
			nbFaces+=1

		with transaction.atomic():
			for seq in last_sequences:seq.save()


		## Load other séquences

		for dict_faces in same_faces[1:]:

			start = datetime.combine(date.today(), last_faces['time'])
			end = datetime.combine(date.today(), dict_faces['time'])

			td = end - start
			diff_time = (td.microseconds + (td.seconds + td.days * 24 * 3600))

			nbFaces+=len(dict_faces['faces'])

			if diff_time/1000>max_diff_time:
				last_faces = dict_faces
				continue

			new_last_sequences = []
			for fIdx in range(len(last_faces['faces'])):
				face = last_faces['faces'][fIdx]
				x, y, w, h = face.x, face.y, face.width, face.height

				# Find Sequence in previous faces
				# If not, break & add to previous faces

				trouve=[False for i in dict_faces['faces']]
				centre = ((x+w)/2, (y+h)/2)

				for fSeqIdx in range(len(dict_faces['faces'])):
					if trouve[fSeqIdx]:continue
					if len(last_sequences)<=fSeqIdx:break

					last_face = dict_faces['faces'][fSeqIdx]
					last_sequence = last_sequences[fSeqIdx]

					x1, y1, w1, h1 = last_face.x, last_face.y, last_face.width, last_face.height
					ann = [x1, y1, w1, h1]
					centre1 = ((x1+w1)/2, (y1+h1)/2)
					distance = sqrt(pow(centre[0]-centre1[0], 2) + pow(centre[1]-centre1[1], 2))
					distance_rel = sqrt(pow((centre[0]-centre1[0])*100/width, 2) + pow((centre[1]-centre1[1])*100/height, 2))
					

					# Si la distance relative < 0.5%
					# Et si la difference de temps et < 200ms 
					# Alors ont peut rajouter le face à la séquence

					if distance_rel<=max_distance_rel:
						last_sequence.faces.add(face)
						last_sequence.endTime = face.time_at
						new_last_sequences.append(last_sequence)
						trouve[fSeqIdx] = True

			with transaction.atomic():
				for seq in new_last_sequences:seq.save()

			last_faces = dict_faces
			last_sequences = []
			last_sequences_to_save = []
			fSeqIdx_new=0
			for fSeqIdx in range(len(trouve)):
				if not trouve[fSeqIdx]:
					seq = Sequences.objects.filter(faces__in=[last_faces['faces'][fSeqIdx]]).last()
					if not seq:
						seq = Sequences.objects.create(video=video,
							startTime=last_faces['faces'][fSeqIdx].time_at,
							endTime=last_faces['faces'][fSeqIdx].time_at)
						seq.faces.add(last_faces['faces'][fSeqIdx])
						seq.endTime = last_faces['faces'][fSeqIdx].time_at
						last_sequences_to_save.append(seq)
						nbNewSequences+=1
					sequence_dbs.append(seq)
					last_sequences.append(seq)
				else:
					seq = new_last_sequences[fSeqIdx_new]
					last_sequences.append(seq)
					fSeqIdx_new+=1

			with transaction.atomic():
				for seq in last_sequences_to_save:seq.save()

			# sys.stdout.write("\r%s - %.2f%% - %d Sequences - %d New" % ((datetime.now() - FacialLib._now), (nbFaces*100/len(face_dbs)), len(sequence_dbs), nbNewSequences))

		return sequence_dbs









	"""
		Remove faces not in sequances
		:param  Array face_dbs
		:param  Array sequence_dbs
		:return Integer nb_faces_delete

		:throws Throwable
	"""
	@staticmethod
	def removeFacesSequences(video, face_dbs, sequence_dbs):
		faces_in_seq = []
		for seq in sequence_dbs:faces_in_seq.extend(seq.faces.all())
		faces_id_in_seq = [face.id for face in faces_in_seq]

		faces_not_in_db = Faces.objects.filter(video=video).exclude(id__in=faces_id_in_seq)

		nb_faces_delete = faces_not_in_db.count()
		faces_not_in_db.delete()

		return nb_faces_delete















	"""
		Extend séquences < 500ms
		:param  Array sequences_db
		:return Integer ecart_milisecond

		:throws Throwable
	"""
	@staticmethod
	def extendSequences(sequences_db, ecart_milisecond=250):
		sequences_db_removed = []
		for i in range(1, len(sequences_db)):
			seq_db_prev = sequences_db[i-1]
			seq_db = sequences_db[i]

			start_prev = datetime.combine(date.today(), seq_db_prev.startTime)
			end_prev = datetime.combine(date.today(), seq_db_prev.endTime)
			start_next = datetime.combine(date.today(), seq_db.startTime)
			end_next = datetime.combine(date.today(), seq_db.endTime)

			if (start_next-end_prev).total_seconds() * 1000<=ecart_milisecond:
				seq_db_prev.endTime = seq_db.endTime
				for face in seq_db.faces.all():
					try:
						seq_db_prev.faces.add(face)
						seq_db.faces.remove(face)
					except:pass
				try:
					seq_db_prev.save()
					seq_db.delete()
					sequences_db_removed.append(seq_db)
				except:pass
		return list(filter(lambda seq:seq not in sequences_db_removed, sequences_db))








	"""
		Remove séquences nb faces < nbFaces
		:param  Array sequences_db
		:return Integer nb_faces

		:throws Throwable
	"""
	@staticmethod
	def removeSmallSequences(sequence_dbs, max_nb_faces=5):
		nb_sequences = 0
		nb_faces = 0
		for seq in sequence_dbs:
			if seq.faces.count()<=max_nb_faces:
				try:
					for face in seq.faces.all():
						try:
							face.delete()
							nb_faces += 1
						except Exception as e:
							pass
					seq.delete()
					nb_sequences += 1
				except Exception as e:
					pass
		return nb_sequences, nb_faces








	"""
		Remove séquences nb faces < 3
		:param  String youtube_id
		:return Integer nb_faces

		:throws Throwable
	"""
	@staticmethod
	def removeSmallSequencesByYtId(youtube_id, nb_faces=3):
		try:
			video = Videos.objects.get(youtube_id=youtube_id)
		except Videos.DoesNotExist:
			raise Exception("Video not found")

		for seq in video.sequences.all():
			if seq.faces.count()<=nb_faces:
				try:
					for face in seq.faces.all():
						try:
							face.delete()
						except:pass
					seq.delete()
				except:pass













	"""
		Copie les tags de la video dans tags facials
		:param  Videos video

		:throws Throwable
	"""
	@staticmethod
	def copyTags(video):
		n=0

		for tag in video.tags.all():
			try:
				Tags.objects.get(value=tag.value)
			except Tags.DoesNotExist:
				t = Tags(value=tag.value)
				t.save()
				n+=1
		return n









	"""
		Supprime toutes les faces & séquences
		:param  String youtube_id

		:throws Throwable
	"""
	@staticmethod
	def removeSequences(video):
		for seq in video.sequences.all():
			for face in seq.faces.all():
				try:
					seq.faces.remove(face)
					face.delete()
				except Exception as e:
					logger.warning("%s" % e)
					pass

			try:
				seq.delete()
			except Exception as e:
				logger.warning("%s" % e)
				pass

				
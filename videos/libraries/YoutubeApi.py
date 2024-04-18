import os, sys
import inspect
from datetime import datetime

# from django.conf import settings
# from django.conf.settings import BASE_DIR
from django.contrib.sessions.backends.db import SessionStore

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import logging
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)








# quotas_exceeded = False
# quotas_exceeded_time = datetime.now()

# limit_quotas_sec = 20



# @staticmethod
# def get_quotas_exceeded():
# 	if YoutubeApi.quotas_exceeded:
# 		td = datetime.now() - YoutubeApi.quotas_exceeded_time
# 		if td.total_seconds()>=YoutubeApi.limit_quotas_sec:
# 			YoutubeApi.quotas_exceeded = False
# 			return False
# 		else:
# 			return True
# 	else:
# 		return False



# @staticmethod
# def set_quotas_exceeded(status=True):
# 	if YoutubeApi.quotas_exceeded != status:
# 		YoutubeApi.quotas_exceeded = status
# 		YoutubeApi.quotas_exceeded_time = datetime.now() if status else False



# @staticmethod
# def get_quotas_exceeded_time():
# 	return YoutubeApi.quotas_exceeded_time


# @staticmethod
# def set_quotas_exceeded_time(value):
# 	YoutubeApi.quotas_exceeded_time = value


	

class YoutubeApi:

	SCOPES = ['https://www.googleapis.com/auth/youtube']
	# currentPath = str(settings.BASE_DIR)+"/youtube/libraries"
	token = None
	client_api_key = "AIzaSyC9EaPb94u91HZYtVmqV1izSOVBQmQLs98"
	youtube=build('youtube','v3', developerKey=client_api_key)




	# def __init__(self, regionCode = "FR", videoCategoryId = 10, maxResults = 30):
	# 	self.credentials = self.getToken()






	# @staticmethod
	# def getToken():
	# 	"""Shows basic usage of the Docs API.
	# 	Prints the title of a sample document.
	# 	"""

	# 	creds = None
	# 	# The file token.json stores the user's access and refresh tokens, and is
	# 	# created automatically when the authorization flow completes for the first
	# 	# time.

	# 	if os.path.exists(YoutubeApi.currentPath+'/token.json'):
	# 		print("Access Token")
	# 		creds = Credentials.from_authorized_user_file(YoutubeApi.currentPath+'/token.json', YoutubeApi.SCOPES)
	# 		YoutubeApi.token = creds.to_json()
	# 	# If there are no (valid) credentials available, let the user log in.

	# 	if not creds or not creds.valid:
	# 		if creds and creds.expired and creds.refresh_token:
	# 			print("Refresh Token")
	# 			creds.refresh(Request())
	# 		else:
	# 			print("Install Token")
	# 			flow = InstalledAppFlow.from_client_secrets_file(
	# 				YoutubeApi.currentPath+'/credentials.json' , 
	# 				# response_type=code,
	# 				# refresh_token="",
	# 				scopes = YoutubeApi.SCOPES,
	# 				# approval_prompt=force,
	# 			)
	# 			# auth_url, _ = flow.authorization_url(prompt='consent')
	# 			# print(auth_url)
	# 			creds = flow.run_local_server(approval_prompt = "force", port=8000)
	# 		# Save the credentials for the next run
	# 		with open(YoutubeApi.currentPath+'/token.json', 'w') as token:
	# 			token.write(creds.to_json())

	# 	YoutubeApi.token = creds.to_json()
	# 	return creds








	@staticmethod
	def getInfosVideos(videoId):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.getToken()

			# youtube = build('youtube','v3', credentials=Credentials(YoutubeApi.token))
			req = YoutubeApi.youtube.videos().list(part="snippet,contentDetails", id=videoId)
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])







	@staticmethod
	def getInfosVideosMulti(videoIds = []):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.getToken()

			# youtube = build('youtube','v3', credentials=Credentials(YoutubeApi.token))
			req = YoutubeApi.youtube.videos().list(part="snippet,contentDetails", id=",".join(videoIds), maxResults=len(videoIds))
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])









	@staticmethod
	def getStatsVideos(videoId=""):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.getToken()

			# youtube = build('youtube','v3', credentials=Credentials(YoutubeApi.token))
			req = YoutubeApi.youtube.videos().list(part="statistics", id=videoId)
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])






	@staticmethod
	def getStatsVideos_multi(videoIds=[]):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.getToken()

			# youtube = build('youtube','v3', credentials=Credentials(YoutubeApi.token))
			req = YoutubeApi.youtube.videos().list(part="statistics", id=",".join(videoIds))
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])





	@staticmethod
	def getInfosChannels(channelId):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.token = YoutubeApi.getToken()

			youtube=build('youtube','v3', developerKey=YoutubeApi.client_api_key)
			req = YoutubeApi.youtube.channels().list(part="snippet,contentDetails", id=channelId)
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])






	@staticmethod
	def getInfosChannelSections(channelId):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.token = YoutubeApi.getToken()

			youtube=build('youtube','v3', developerKey=YoutubeApi.client_api_key)
			req = YoutubeApi.youtube.channelSections().list(part="snippet,contentDetails", channelId=channelId)
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])






	@staticmethod
	def getInfosChannelSectionsId(channelId):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.token = YoutubeApi.getToken()

			youtube=build('youtube','v3', developerKey=YoutubeApi.client_api_key)
			req = YoutubeApi.youtube.channelSections().list(part="snippet,contentDetails", id=channelId)
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])






	@staticmethod
	def getVideosChannel(channelId, maxResults=20):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.token = YoutubeApi.getToken()

			youtube=build('youtube','v3', developerKey=YoutubeApi.client_api_key)
			req = YoutubeApi.youtube.search().list(part="id", channelId=channelId, order="date", maxResults=maxResults)
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])








	@staticmethod
	def getInfosPlaylist(playlistId):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.token = YoutubeApi.getToken()

			youtube=build('youtube','v3', developerKey=YoutubeApi.client_api_key)
			req = YoutubeApi.youtube.playlistItems().list(part="snippet,contentDetails", id=playlistId)
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])






	@staticmethod
	def getStatsChannels(videoIds=[]):
		try:
			# if YoutubeApi.token is None:
			# 	YoutubeApi.getToken()

			# youtube = build('youtube','v3', credentials=Credentials(YoutubeApi.token))
			req = YoutubeApi.youtube.channels().list(part="statistics", id=",".join(videoIds))
			return req.execute()
		except HttpError as e:
			if e.status_code == 403:
				# YoutubeApi.set_quotas_exceeded(True)
				raise Exception("%s - Erreur de Quotas" % inspect.stack()[0][3])
			raise Exception("%s - Http Erreur Code %s" % (inspect.stack()[0][3], e.status_code))
		except:raise Exception("%s - Erreur Inconnus" % inspect.stack()[0][3])



#######   TESTING ########

if __name__ == "__main__":
	import pprint
	pp = pprint.PrettyPrinter(indent=4)

	youtube_id = "ix1OXzR1HXo"
	channel_id = "UCcC2EUpXdKgmDizj6WIIm3Q"

	try:
		snippet = YoutubeApi.getInfosVideos(youtube_id)['items'][0]
		pp.pprint(snippet)

		# snippet = YoutubeApi.getInfosChannels(channel_id)['items'][0]['snippet']
		# pp.pprint(YoutubeApi.getInfosChannels(channel_id))
	except HttpError as e:
		print("{} - {}".format(datetime.now(), e))
	finally:pass

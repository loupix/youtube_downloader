from django.core.exceptions import *
from django.db import DatabaseError
from app.exceptions import CrudError

import logging
logger = logging.getLogger("db")


"""
 Model CRUD des sons dans la database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""


class VocalCrud():


	"""
		Create downloaded data
		:param  Request
		:return File

		:throws Throwable
	"""
	@staticmethod
	def create(data = {}):
		return
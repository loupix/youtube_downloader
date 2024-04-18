from django.test import Client, TestCase, SimpleTestCase
from django.test.client import RequestFactory
import unittest

from app.models import Visitors
from app.libraries import VisitorCrud
from app.exceptions import CrudError

class VisitorTest(TestCase):

	_factory = RequestFactory()
	_request = _factory.get("/", HTTP_USER_AGENT='Mozilla/5.0')
	
	def setUp(self):
		return

	def test_create(self):
		try:
			self._request.session = self.client.session 	# Créer la session dans Request
			visitor = VisitorCrud.create(self._request)
			self.visitor_id = visitor.id
			self.assertIsInstance(visitor, Visitors)
		except CrudError as e:
			self.fail(e)
		finally:pass





	def test_read(self):
		try:
			visitor = VisitorCrud.read(self._request)
			self.assertIsInstance(visitor, Visitors)
		except CrudError as e:
			self.fail(e)
		finally:pass





	def test_delete(self):
		try:
			visitor = VisitorCrud.delete(self._request)
			self.assertIsInstance(visitor, Visitors)
		except CrudError as e:
			self.fail(e)
		finally:pass


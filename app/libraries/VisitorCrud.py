

"""
 Model CRUD des visiteurs in database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""


from app.models import Visitors
from .LocationCrud import LocationCrud
from django.core.exceptions import *
from django.db import DatabaseError
from app.exceptions import CrudError

import inspect
import pytest
from user_agents import parse

import logging
logger = logging.getLogger("db")

import random, string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




class VisitorCrud():

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip






    """
       Create visitor
     :param  Request
     :return Visitor
     
     :throws Throwable
    """
    @staticmethod
    def create(request):
        try:
            # request.session.flush()
            if 'visitor_id' in request.session:
                request.POST = request.POST.copy().update({'visitor_id':Visitors.objects.filter(id=request.session.get('visitor_id')).first().id})
                return VisitorCrud.update(request)
            # elif Visitors.objects.filter(address_ip=VisitorCrud.get_client_ip(request)).count()>0:
            #     request.POST = request.POST.copy().update({'visitor_id':Visitors.objects.filter(address_ip=VisitorCrud.get_client_ip(request)).first().id})
            #     return VisitorCrud.update(request)
            else:
                visitor = Visitors(id=id_generator(7))
                visitor.address_ip = VisitorCrud.get_client_ip(request)

                user_agent = parse(request.headers.get('User-Agent'))

                visitor.kind = user_agent.device.family
                visitor.brand = user_agent.device.brand
                visitor.platform = user_agent.os.family
                visitor.platform_version = user_agent.os.version_string
                visitor.browser = user_agent.browser.family
                visitor.browser_version = user_agent.browser.version_string
                visitor.is_bot = user_agent.is_bot

                visitor.location = LocationCrud.create(visitor)

                visitor.save()
                request.session.update({'visitor_id': visitor.id})
                request.session.save()

                logger.info("Visitor %s created" % visitor.id)
                return visitor
        except DatabaseError as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), 409)
        except CrudError as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), e.code)
        except Exception as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e))






    """
       Read visitor
     :param  Request
     :return Visitor
     
     :throws Throwable
    """
    @staticmethod
    def read(request):
        try:
            if "visitor" in request.session:return request.session.get("visitor")

            if 'visitor_id' in request.session:
                visitor = Visitors.objects.get(id=request.session["visitor_id"])
                if visitor is not None:return visitor
                raise ObjectDoesNotExist("Visitor")
            # elif Visitors.objects.filter(address_ip=VisitorCrud.get_client_ip(request)).count()>0:
            #     visitor = Visitors.objects.get(address_ip=VisitorCrud.get_client_ip(request))
            #     if visitor is not None:
            #         request.session['visitor_id'] = visitor.id
            #         request.session.save()
            #         return visitor
            #     raise ObjectDoesNotExist("Visitor")

            if "visitor_id" not in request.POST:
                raise FieldDoesNotExist("visitor_id")

            if Visitors.objects.filter(id=request.POST.get("visitor_id")).count()==0:
                raise ObjectDoesNotExist("visitor")

            visitor = Visitors.objects.get(id=request.POST.get("visitor_id"))
            request.session['visitor_id'] = visitor.id
            request.session.save()
            return visitor


        except FieldDoesNotExist as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), 401)
        except ObjectDoesNotExist as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), 404)
        except DatabaseError as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), 409)
        except Exception as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e))






    """
       Update visitor
     :param  Request
     :return Visitor
     
     :throws Throwable
    """
    @staticmethod
    def update(request):
        try:
            visitor = VisitorCrud.read(request)
            visitor.address_ip = VisitorCrud.get_client_ip(request)

            user_agent = parse(request.headers.get('User-Agent'))

            visitor.kind = user_agent.device.family
            visitor.brand = user_agent.device.brand
            visitor.platform = user_agent.os.family
            visitor.platform_version = user_agent.os.version_string
            visitor.browser = user_agent.browser.family
            visitor.browser_version = user_agent.browser.version_string
            visitor.is_bot = user_agent.is_bot

            visitor.location = LocationCrud.create(visitor)

            visitor.save()
            logger.info("Visitor %s updated" % visitor.id)
            return visitor

        except DatabaseError as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), 409)
        except FieldDoesNotExist:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], "Field not present", 401)
        except ObjectDoesNotExist:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], "Visitor not found", 404)
        except CrudError as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), e.code)
        except Exception as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e))






    """
       Delete visitor
     :param  Request
     :return Visitor
     
     :throws Throwable
    """
    @staticmethod
    def delete(request):
        try:

            visitor = VisitorCrud.read(request)

            visitor.delete()
            request.session.pop('visitor_id')
            logger.info("Visitor %s deleted" % visitor.id)
            return visitor
        except DatabaseError as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), 409)
        except CrudError as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e), e.code)
        except Exception as e:
            raise CrudError(VisitorCrud.__name__, inspect.stack()[0][3], str(e))
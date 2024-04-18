
"""
 Model CRUD des fichiers in database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""


from app.models import Downloaded, Visitors
from . import VisitorCrud
from videos.libraries import VideoCrud, YoutubeCrud
from django.core.exceptions import *
from django.db import DatabaseError
from app.exceptions import CrudError

import logging
logger = logging.getLogger("db")


import random, string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))





class DownloadCrud():



    """
       Create downloaded data
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def create(data = {}):
        try:
            fields = ['status','percent','format_file', 'format_type','visitor_id', 'path', 'filename', 'thumbnail', 'url', 'url_id']
            for f in fields:
                if f not in data: raise FieldDoesNotExist(f)

            try:
                visitor = Visitors.objects.get(id=data.get("visitor_id"))
            except Visitors.DoesNotExist:
                raise ObjectDoesNotExist("Visitor")

            format_file = VideoCrud.getOrCreateFormat(data.get("format_file"))

            down = Downloaded.objects.filter(url = data.get("url"), format_file=format_file, format_type=data.get("format_type")).first()
            if not down:
                filename = data.get("filename").encode('ascii', 'xmlcharrefreplace').decode("utf-8")
                down = Downloaded(id = id_generator(14), status = data.get("status"), percent = data.get("percent"), 
                    path = data.get("path"), url = data.get("url"), url_id = data.get("url_id"),
                    thumbnail = data.get("thumbnail"), format_file = format_file, format_type = data.get("format_type"),
                    filename = filename)
            else:
                down.number_download += 1

            down.save()
            if visitor not in down.visitors.all():
                down.visitors.add(visitor)
                down.save()

            return down

        except DatabaseError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), 409)
        except FieldDoesNotExist as e:
            raise CrudError(DownloadCrud.__class__.__name__, "Field %s does not exist" % e, 404)
        except ObjectDoesNotExist as e:
            raise CrudError(DownloadCrud.__class__.__name__, "Object %s does not exist" % e, 404)
        except CrudError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e))







    """
       Read downloaded data
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def read(request):
        try:
            return

        except DatabaseError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e))







    """
       Update downloaded data
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def update(request):
        try:
            return

        except DatabaseError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e))








    """
       Delete downloaded data
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def delete(request):
        try:
            return

        except DatabaseError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(DownloadCrud.__class__.__name__, str(e))


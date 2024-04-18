

"""
 Model CRUD des files d'attente in database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""



from app.models import Queue, Downloaded, Visitors
from app.libraries.VisitorCrud import VisitorCrud
from django.core.exceptions import *
from django.db import DatabaseError
from app.exceptions import CrudError

import logging
logger = logging.getLogger("db")

import random, string
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



class QueueCrud():



    """
       Create file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def create(request):
        try:
            if "queue_id" in request.session:
                return Queue.objects.get(id=request.session.get("queue_id"))

            visitor = Visitors.objects.get(id=request.session.get("visitor_id"))
            if visitor is None: raise ObjectDoesNotExist("Visitor")

            queue = Queue(id=id_generator(7))
            queue.visitor = visitor
            queue.save()
            request.session.update({'queue_id': queue.id})
            request.session.modified = True
            logger.info("Queue %s created" % queue.id)
            return queue

        except DatabaseError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e))







    """
       Read file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def read(session):
        try:
            if "queue" in session:return session.get("queue")
            if "queue_id" in session:
                q = Queue.objects.get(id=session.get("queue_id"))
                if not q:raise ObjectDoesNotExist("Queue")
                return q

            if "id" not in request.POST:
                raise FieldDoesNotExist("Id")

            if Queue.objects.filter(id=request.POST.get("id")).count()==0:
                raise ObjectDoesNotExist("Queue")

            return Queue.objects.filter(id=request.POST.get("id")).first()

        except FieldDoesNotExist:
            raise CrudError(QueueCrud.__class__.__name__, "Field not present", 401)
        except ObjectDoesNotExist:
            raise CrudError(QueueCrud.__class__.__name__, "Visitor not found", 404)
        except DatabaseError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), 409)
        except Exception as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e))







    """
       Update file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def update(request):
        try:
            queue = QueueCrud.read(request)
            queue.save()

            request.session.update({'queue_id': queue.id})
            logger.info("Queue %s updated" % queue.id)
            return queue

        except DatabaseError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e))








    """
       Delete file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def delete(request):
        try:
            queue = QueueCrud.read(request)
            queue.delete()

            request.session.pop('queue_id')
            logger.info("Queue %d updated" % queue.id)
            return queue

        except DatabaseError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e))






    """
       Add download file
     :param  Queue
     :param  Downloaded
     :return Queue
     
     :throws Throwable
    """
    @staticmethod
    def add(queue, downloaded):
        try:
            if not downloaded in queue.downloads.all():
                queue.downloads.add(downloaded)
                queue.save()
            logger.info("Queue %s add video %s" % (queue.id, downloaded.id))
            return queue

        except DatabaseError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e))






    """
       Remove download file
     :param  Queue
     :param  Downloaded
     :return Queue
     
     :throws Throwable
    """
    @staticmethod
    def remove(queue, downloaded):
        try:
            if downloaded in queue.downloads.all():
                queue.downloads.remove(downloaded)
                queue.save()
            logger.info("Queue %s remove video %s" % (queue.id, downloaded.id))
            return queue

        except DatabaseError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(QueueCrud.__class__.__name__, str(e))




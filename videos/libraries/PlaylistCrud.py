from app.models import Downloaded
from videos.models import Videos
from django.core.exceptions import *
from django.db import DatabaseError
from app.exceptions import CrudError

import logging
logger = logging.getLogger("db")

"""
 Model CRUD des playlists youtube in database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""


class PlaylistCrud():



    """
       Create file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def create(request):
        try:
            return

        except DatabaseError as e:
            raise CrudError(self.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(self.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(self.__class__.__name__, str(e))







    """
       Read file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def read(request):
        try:
            return


        except DatabaseError as e:
            raise CrudError(self.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(self.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(self.__class__.__name__, str(e))







    """
       Update file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def update(request):
        try:
            return


        except DatabaseError as e:
            raise CrudError(self.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(self.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(self.__class__.__name__, str(e))








    """
       Delete file
     :param  Request
     :return File
     
     :throws Throwable
    """
    @staticmethod
    def delete(request):
        try:
            return


        except DatabaseError as e:
            raise CrudError(self.__class__.__name__, str(e), 409)
        except CrudError as e:
            raise CrudError(self.__class__.__name__, str(e), e.code)
        except Exception as e:
            raise CrudError(self.__class__.__name__, str(e))



"""
 Model CRUD des locations in database
 Create ; Read ; Update ; Delete
 :author Loïc Daniel <loicdaniel.fr>
"""


from app.models import Location
from django.core.exceptions import *
from django.db import DatabaseError
from app.exceptions import CrudError
from django.conf import settings

import geoip2.database
import inspect
import urllib
from PIL import Image
import base64
import os
import math

from base64 import b64encode, b64decode
from io import BytesIO, StringIO

import logging
logger = logging.getLogger("db")




class LocationCrud():
    _DB_FILE = str(settings.BASE_DIR)+"/GeoLite2-City.mmdb"

    _lat = 0
    _lng = 0
    _zoom = 5


    @staticmethod
    def get_location(addresse_ip):
        if addresse_ip == "127.0.0.1" or addresse_ip[:10]=="192.168.1.":addresse_ip="89.159.124.25"

        with geoip2.database.Reader(LocationCrud._DB_FILE) as reader:
            response = reader.city(addresse_ip)
            return {
                "pays": response.country.name,
                "region": response.subdivisions.most_specific.name,
                "ville": response.city.name,
                "code_postal": response.postal.code,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
            }


    @staticmethod
    def getXY():
        """
            Generates an X,Y tile coordinate based on the latitude, longitude 
            and zoom level
            Returns:    An X,Y tile coordinate
        """
        
        tile_size = 128

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << LocationCrud._zoom

        # Find the x_point given the longitude
        point_x = (tile_size/ 2 + LocationCrud._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(LocationCrud._lat * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1+sin_y)/(1-sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)




    @staticmethod
    def generateImage(**kwargs):
        """
            Generates an image by stitching a number of google map tiles together.
            
            Args:
                start_x:        The top-left x-tile coordinate
                start_y:        The top-left y-tile coordinate
                tile_width:     The number of tiles wide the image should be -
                                defaults to 5
                tile_height:    The number of tiles high the image should be -
                                defaults to 5
            Returns:
                A high-resolution Goole Map image.
        """

        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 5)
        tile_height = kwargs.get('tile_height', 5)
        map_size = kwargs.get('map_size', 256)

        # Check that we have x and y tile coordinates
        if start_x == None or start_y == None :
            start_x, start_y = LocationCrud.getXY()

        # Determine the size of the image
        width, height = map_size * tile_width, map_size * tile_height

        #Create a new image of the size require
        map_img = Image.new('RGB', (width,height))

        for x in range(0, tile_width):
            for y in range(0, tile_height) :
                url = 'https://mt1.google.com/vt?x='+str(start_x+x)+'&y='+str(start_y+y)+'&z='+str(LocationCrud._zoom)

                current_tile = str(x)+'-'+str(y)
                urllib.request.urlretrieve(url, current_tile)
            
                im = Image.open(current_tile).convert('L')
                map_img.paste(im, (x*map_size, y*map_size))
              
                os.remove(current_tile)

        return map_img

    





    """
       Create visitor
     :param  Request
     :return Visitor
     
     :throws Throwable
    """
    @staticmethod
    def create(Visitor):
        try:
            location = LocationCrud.get_location(Visitor.address_ip)
            l = Location.objects.filter(latitude=location['latitude'], longitude=location['longitude'])
            if l.count()>0:
                Visitor.location = l.first()
                Visitor.save()
                return l.first()

            loc = Location(pays = location['pays'], region = location['region'], 
                ville = location['ville'], code_postal = location['code_postal'],
                latitude = location['latitude'], longitude = location['longitude'])

            # download picture google map

            LocationCrud._lat = location['latitude']
            LocationCrud._lng = location['longitude']
            try:
                image = LocationCrud.generateImage(tile_width=5, tile_height=5, 
                    map_size=128)

                stream = BytesIO()
                image.save(stream, format="PNG")
                loc.picture = stream.getvalue()
            except:pass

            loc.save()

            return loc



        except RequestAborted as e:
            raise CrudError(LocationCrud.__name__, inspect.stack()[0][3], str(e), 403)
        except DatabaseError as e:
            raise CrudError(LocationCrud.__name__, inspect.stack()[0][3], str(e), 409)
        except CrudError as e:
            raise CrudError(LocationCrud.__name__, inspect.stack()[0][3], str(e), e.code)
        except Exception as e:
            raise CrudError(LocationCrud.__name__, inspect.stack()[0][3], str(e))

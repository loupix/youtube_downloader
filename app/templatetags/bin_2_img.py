from base64 import b64encode, b64decode
from django import template
import io
from PIL import Image

register = template.Library()

@register.filter
def bin_2_img(_bin):
    if _bin is not None: return b64encode(_bin).decode()

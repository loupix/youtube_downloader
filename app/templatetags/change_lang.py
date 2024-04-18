from django.template import Library
from django.urls import resolve, reverse
from django.utils.translation import activate, get_language

register = Library()

@register.simple_tag(takes_context = True)
def change_lang(context, lang = None, * args, ** kwargs):

    path = context['request'].path
    url_parts = resolve(path)

    cur_language = get_language()


    try:
        activate(lang)
        url = reverse(url_parts.view_name, kwargs = url_parts.kwargs)
        print(url_parts.view_name, url_parts.kwargs, get_language(), url)
    finally:
        activate(cur_language)

    print(url_parts.view_name, url_parts.kwargs, get_language(), url)

    return '%s' % url


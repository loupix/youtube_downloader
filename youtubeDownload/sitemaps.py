from django.contrib import sitemaps
from django.urls import reverse
from videos.models import Videos

class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'always'
    priority = 0.8
    protocol = "https"

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)



class VideoSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.6
    protocol = "https"

    def items(self):
        return Videos.objects.order_by('created_at')[:10]

    def lastmod(self, obj):
        return obj.created_at

    def location(self, video):
        return "/v/%s" % video.id

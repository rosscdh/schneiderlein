import os
import untangle
import urlparse

from models import Page


class Sitemap(object):
    sitemap_file = None
    parsed_sitemap = None
    urls = []

    def __init__(self, sitemap):
        self.sitemap_file = sitemap
        self.parsed_sitemap = untangle.parse(sitemap)
        self.urls = self.parse(self.parsed_sitemap)

        for i in self.urls:
            url = i
            p = urlparse.urlparse(i)

            fileName, fileExtension = os.path.splitext(p.path)
            if fileExtension == '.xml':
                new_urls = self.parse(untangle.parse(url))
                if len(new_urls) > 0:
                    for u in new_urls:
                        self.urls.append(u)


    def __unicode__(self):
        return '<Sitemap %s>' % (self.sitemap_file, )

    def parse(self, parsed_xml):
        urls = []
        try:
            if parsed_xml.sitemapindex:
                for c in parsed_xml.sitemapindex.sitemap:
                    urls.append(c.loc.cdata)
        except IndexError:
            try:
                if parsed_xml.urlset:
                        for c in parsed_xml.urlset.url:
                            urls.append(c.loc.cdata)
            except IndexError:
                urls = []

        return urls

    def get_set_pages(self):
        for u in self.urls:
            Page.objects.get_or_create(url=u, slug=u,defaults={'parent': None,})

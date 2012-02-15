import os
import untangle
import urlparse
from django.template.defaultfilters import slugify
from models import Page


class Sitemap(object):
    sitemap_file = None
    parsed_sitemap = None
    url_tree = dict({})

    def __init__(self, sitemap):
        self.sitemap_file = sitemap
        self.parsed_sitemap = untangle.parse(sitemap)
        urls = self.parse(self.parsed_sitemap)

        for i in urls:
            url = i
            p = urlparse.urlparse(i)
            fileName, fileExtension = os.path.splitext(p.path)
            if fileExtension == '.xml':

                if url not in self.url_tree:
                    self.url_tree[url] = []

                new_urls = self.parse(untangle.parse(url))

                if len(new_urls) > 0:
                    for u in new_urls:
                        self.url_tree[url].append(u)


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
        for key,value_list in self.url_tree.iteritems():

            p = urlparse.urlparse(key)
            fileName, fileExtension = os.path.splitext(p.path)

            parent, is_created = Page.objects.get_or_create(url=key, slug=slugify(fileName))
            if is_created == False:
                parent.save()
            for u in value_list:
                p = urlparse.urlparse(u)
                fileName, fileExtension = os.path.splitext(p.path)

                child, is_created = Page.objects.get_or_create(url=u, slug=slugify(fileName), defaults={'parent': parent,})
                if is_created == False:
                    child.save()

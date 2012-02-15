#from django.conf import settings
from django.template.defaultfilters import slugify
from needle.cases import NeedleTestCase

NEEDLE_TOLERANCE  = 2.5#getattr(settings, 'NEEDLE_TOLERANCE', 0.5)

class SchneiderleinTest(NeedleTestCase):
    """ Generic test for schniderlein """
    def test_generic(self, url=None, elements=None):
        #url = 'http://www.sedo.com/us/home/getting-started/?tracked=&partnerid=&language=us'
        url = 'http://www.sedo.com/us/about-us/press/press-downloads'
        elements = ['div#col3_content']

        """ method to test a url and specific elements on that url"""
        if len(elements) > 0:
            self.driver.get( url )
            for e in elements:
                c = 0
                e_name = slugify(e)
                blocks = self.driver.find_elements_by_css_selector( e )

                if len(blocks) > 0:
                    for b in blocks:
                        c = c + 1
                        self.assertScreenshot(b, '%s-%02d' % (e_name, c, ), NEEDLE_TOLERANCE)

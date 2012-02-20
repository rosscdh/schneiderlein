import os
import simplejson as json
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.core.management import call_command

from optparse import make_option
from needle.spindle import Spindle

from apps.page.models import Page

NEEDLE_TOLERANCE  = 2.5#getattr(settings, 'NEEDLE_TOLERANCE', 0.5)
OUTPUT_PATH = getattr(settings, 'NEEDLE_OUTPUT_PATH', os.path.abspath('./cutting_room/') + '/')

import logging
logger = logging.getLogger('tailor.workshop')

from datetime import datetime
import time
today = datetime.today()
now = time.time()


class Command(BaseCommand):
    args = '<page_id page_id ...>'
    help = 'Generate screenshots for a list of Page objects'
    option_list = BaseCommand.option_list + (
        make_option('--generate',
            action='store',
            dest='generate',
            default=False,
            help='Genereate Screenshot for specified Page'),
        make_option('--all',
            action='store',
            dest='all',
            default=False,
            help='Perform action on All Pages'),
    )

    needle = None

    def handle(self, *args, **options):
        self.build_id = 'build-%s' % now

        generate_screenshot = True if options['generate'] in ['True',True] else False
        all_pages = True if options['all'] in ['True',True] else False

        num_pages_ids = len(args)
        logger.debug('num num_pages_ids %d' % num_pages_ids)

        if all_pages in ['False',False] and num_pages_ids == 0:
            raise CommandError('Please specify page_id(s) to test in form: tailor_page_url <id> <id> <id> ...')

        self.needle = Spindle(capture=generate_screenshot, output_path=OUTPUT_PATH)

        if all_pages == True:
            args = []
            for page in Page.objects.all():
                self.test_page(url=page.url, elements_list=page.test_layout_elements.all(), page=page)
        else:
            for page_id in args:
                try:
                    page = Page.objects.get(pk=int(page_id))
                except Page.DoesNotExist:
                    raise CommandError('Page "%s" does not exist' % page_id)

                self.test_page(url=page.url, elements_list=page.test_layout_elements.all(), page=page)

    def test_page(self, url, elements_list=None, page=None):
        """ selenium test the url using needle """

        # init page path if not exists
        call_command('tailor_cutting_room', str(page.pk), initialize=True)

        # get needle driver url
        logger.info('Loading Test Url: %s' % url)
        self.needle.driver.get( url )

        elements = []
        if not elements_list or len(elements_list) == 0:
            logger.info('No Elements Found for "%s" (%d): Using default (html)' % (url, page.pk,))
            elements.append('html')
        else:
            for e in elements_list:
                e = e.name.strip()
                logger.debug('Require Element: %s' % e)
                elements.append( e )

        # set needle output path
        self.needle.output_path =  '%s%s/' % (OUTPUT_PATH, page.pk,)
        logger.info('Output path: %s' % self.needle.output_path)

        # if the dir does not exist make it.. make it good
        if not os.path.exists(self.needle.output_path):
            logger.warning('Output path Did not exist creating: %s' % self.needle.output_path)
            os.makedirs(self.needle.output_path)

        # loop over provided elements
        for e in elements:
            c = 0
            e_name = slugify(e)

            logger.info('Selenium find "%s"' % e)
            blocks = self.needle.driver.find_elements_by_css_selector( e )

            num_blocks = len(blocks)
            logger.info('%d Blocks Found for element "%s"\n' % (num_blocks, e,))

            if num_blocks > 0:
                for b in blocks:
                    c = c + 1
                    element_name = '%s-%02d' % (e_name, c,)
                    try:
                        self.needle.assertScreenshot(b, element_name, NEEDLE_TOLERANCE)
                    except AssertionError as error:
                        # this would trigger a failed test - Element Layout No Match
                        logger.error('ElementLayoutNoMatch - Element Layout does not match its baseline: %s' % error)
            else:
                # this would trigger a failed test - Element not found
                logger.error('ElementNotFound - No Blocks Found for Element "%s"' % e)



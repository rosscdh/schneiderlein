import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.core.management import call_command

from optparse import make_option
from needle.spindle import Spindle

from apps.page.models import Page

NEEDLE_TOLERANCE  = 2.5#getattr(settings, 'NEEDLE_TOLERANCE', 0.5)
OUTPUT_PATH = getattr(settings, 'NEEDLE_OUTPUT_PATH', os.path.abspath('./cutting_room/') + '/')


class Command(BaseCommand):
    args = '<page_id page_id ...>'
    help = 'Generate screenshots for a list of Page objects'
    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all_pages',
            default=False,
            help='Test All Pages'),
        make_option('--generate',
            action='store_true',
            dest='generate_screenshot',
            default=False,
            help='Generate a baseline screenshot for future comparison tests'),
        )

    needle = None

    def handle(self, *args, **options):

        generate_screenshot = options['generate_screenshot']
        all_pages = options['all_pages']

        if all_pages == False and len(args) == 0:
            raise CommandError('Please specify page_id(s) to test in form: tailor_page_url <id> <id> <id> ...')

        self.needle = Spindle(capture=generate_screenshot, output_path=OUTPUT_PATH)

        if all_pages == True:
            args = []
            for page in Page.objects.all():
                self.test_page(page.url, page.test_layout_elements.all(), page=page)
        else:
            for page_id in args:
                try:
                    page = Page.objects.get(pk=int(page_id))
                except Page.DoesNotExist:
                    raise CommandError('Page "%s" does not exist' % page_id)

                self.test_page(page.url, page.test_layout_elements.all(), page=page)

    def test_page(self, url, elements_list=None, page=None):
        """ selenium test the url using needle """

        # init page path if not exists
        call_command('tailor_cutting_room', str(page.pk), initialize=True)

        elements = []
        if not elements_list or len(elements_list) == 0:
            self.stdout.write('No Elements Found for "%s" (%d): Using default\n' % (url,page.pk,))
            elements.append('html')
        else:
            for e in elements_list:
                elements.append( e.name.strip() )

        # get needle driver url
        #url = 'http://www.sedo.com/us/about-us/careers/our-departments'
        self.needle.driver.get( url )

        # set needle output path
        self.needle.output_path =  '%s%s/' % (OUTPUT_PATH, page.pk,)

        # if the dir does not exist make it.. make it good
        if not os.path.exists(self.needle.output_path):
            os.makedirs(self.needle.output_path)

        # loop over provided elements
        for e in elements:
            c = 0
            e_name = slugify(e)

            self.stdout.write('Trying "%s"\n' % (e,))
            blocks = self.needle.driver.find_elements_by_css_selector( e )
            num_blocks = len(blocks)

            self.stdout.write('%d Blocks Found for element "%s"\n' % (num_blocks, e,))

            if num_blocks > 0:
                for b in blocks:
                    c = c + 1
                    element_name = '%s-%02d' % (e_name, c,)
                    #try:
                    self.needle.assertScreenshot(b, element_name, NEEDLE_TOLERANCE)
                    #except AssertionError:
                    #    self.log_error(page, element_name)
            else:
                self.stdout.write('No Blocks Found for element "%s"\n' % e)

    def log_error(self, page, element):
        pass
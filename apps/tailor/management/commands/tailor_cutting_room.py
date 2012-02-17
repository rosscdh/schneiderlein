import os
import shutil
import inspect

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option

from apps.page.models import Page

NEEDLE_TOLERANCE  = 2.5#getattr(settings, 'NEEDLE_TOLERANCE', 0.5)
OUTPUT_PATH = getattr(settings, 'NEEDLE_OUTPUT_PATH', './cutting_room/')

class Command(BaseCommand):
    args = '<page_id page_id ...>'
    help = 'Manage the Cuttingroom Floor: --delete'
    option_list = BaseCommand.option_list + (
        make_option('--initialize',
            action='store_true',
            dest='initialize',
            default=False,
            help='Specify the command to run'),
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Specify the command to run'),
        make_option('--clean_up',
            action='store_true',
            dest='clean_up',
            default=False,
            help='Specify the command to run'),
        make_option('--all-pages',
            action='store_true',
            dest='all_pages',
            default=False,
            help='For All Pages'),
        )

    needle = None

    def handle(self, *args, **options):

        self.all_pages = options['all_pages']

        if options['initialize'] != False:
            self.initialize(args)
        if options['delete'] != False:
            self.delete_page(args)
        if options['clean_up'] != False:
            self.clean_up()

        #inspect.ismethod(inst1.f1)
    def initialize(self, page_ids):
        for page_id in page_ids:
            f = os.path.join(
                OUTPUT_PATH,
                page_id
                )
            fail_path = os.path.join(
                f,
                'fail'
                )
            paths = [f, fail_path]
            for p in paths:
                if not os.path.exists(p):
                    os.makedirs(p)

    def delete_page(self, page_ids=None):
        if self.all_pages == True:
            # delete all <page_id> folders in cutting_room
            page_ids = []
            for page in Page.objects.filter(is_active=False).all():
                page_ids.append(page.pk)
        else:
            # delete specified ids
            if len(page_ids) == 0:
                raise CommandError('Please specify page_id(s) to delete i.e. manage.py cutting_room --delete <page_id> <page_id> ...')

        for page in page_ids:
            f = os.path.join(
                OUTPUT_PATH,
                page
                )

            if os.path.exists(f):
                shutil.rmtree(f)
                print "Deleted %s" % f
            else:
                print "Does not exist: %s" % f

    def clean_up(self):
        delete_ids = []

        for page in Page.objects.filter(is_active=False).all():
            delete_ids.append(page.pk)

        if len(delete_ids) > 0:
            self.delete_page(delete_ids)
        else:
            raise CommandError('No Pages are In-active and thus there is nothing to clean_up')


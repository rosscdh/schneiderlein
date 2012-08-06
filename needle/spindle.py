from django.conf import settings
from diff import ImageDiff
from driver import NeedleWebDriver
import os, sys
from PIL import Image
from needle.watermark import watermark
from datetime import datetime
import time

today = datetime.today()
now = time.time()

SELENIUM_BROWSER_CAPABILITIES  = getattr(settings, 'SELENIUM_BROWSER_CAPABILITIES', dict({
    'browserName': 'firefox',
}))


class Spindle(object):
    """
    Object which provides tools for testing CSS with Selenium.
    """
    #: An instance of :py:class:`~needle.driver.NeedleWebDriver`, created when 
    #: each test is run.
    driver = None

    driver_command_executor = 'http://127.0.0.1:4444/wd/hub'
    driver_desired_capabilities = SELENIUM_BROWSER_CAPABILITIES
    driver_browser_profile = None

    capture = False
    output_path = None

    def __init__(self, *args, **kwargs):
        self.driver = self.get_web_driver()
        self.capture = kwargs['capture'] if 'capture' in kwargs else False
        self.output_path = kwargs['output_path'] if 'output_path' in kwargs else os.path.dirname(__file__)

    def __call__(self, *args, **kwargs):
        super(Spindle, self).__call__(*args, **kwargs)
        self.driver.close()

    def get_web_driver(self):
        return NeedleWebDriver(
            self.driver_command_executor,
            self.driver_desired_capabilities,
            self.driver_browser_profile
        )

    def getPageHTML(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def assertScreenshot(self, element, name, threshold=0.1):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.
        
        :param element: Either a CSS selector as a string or a 
                        :py:class:`~needle.driver.NeedleWebElement` object that 
                        represents the element to capture.
        :param name: A name for the screenshot, which will be appended with 
                     ``.png``.
        :param threshold: The threshold for triggering a test failure.
        """
        if isinstance(element, basestring):
            element = self.driver.find_element_by_css_selector(element)
        if isinstance(name, basestring):
            filename = os.path.join(
                self.output_path,
                '%s.png' % name
            )
        else:
            # names can be filehandles for testing. This sucks - we
            # should write out files to their correct location
            filename = name

        if self.capture:
            element.get_screenshot().save(filename)
        else:
            if not os.path.exists(filename):
                element.get_screenshot().save(filename)

            image = Image.open(filename)

            # now take another screenshot and re open it (yea i know) but there were issues wth colours
            compare_shot_filename = filename.replace('.png','-compare.png')
            screenshot = element.get_screenshot().save(compare_shot_filename)

            screenshot = Image.open(compare_shot_filename)

            try:
                diff = ImageDiff(screenshot, image)
                distance = abs(diff.get_distance())
                if distance > threshold:
                    raise AssertionError("The saved screenshot for '%s' did not match "
                                         "the screenshot captured (by a distance of %.2f)" 
                                         % (name, distance))
                else:
                    self.remove_screenshot(compare_shot_filename)
            except:
                # Generate watermarked difference file
                comparison_filename = filename.replace('.png','-%s-fail.png' % (now, ))
                fail_path, filename = os.path.split(comparison_filename)
                comparison_filename = '%s/%s/%s' % (fail_path, 'fail', filename)

                watermark(image, screenshot, 'tile', 0.3).save(comparison_filename)

                self.remove_screenshot(compare_shot_filename)

                raise AssertionError("The Base Screenshot differs from the Comparison Screenshot")


    def remove_screenshot(self, screenshot_path):
        # remove compare file
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)



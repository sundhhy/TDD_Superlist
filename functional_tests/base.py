#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

import sys
import platform

from pyvirtualdisplay import Display
#下面两种写法都可以
#chromedriver = "/usr/local/share/chromedriver"

print(platform.platform())
if 'Windows' not in platform.platform():
    display = Display(visible=0, size=(800, 800))
    display.start()
chromedriver = '../../../tools/chromedriver'

#class NewVisitorTest(LiveServerTestCase):
class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]

                return
            super().setUpClass()
            cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome(chromedriver)
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        #self.assertTrue(
        #    any(row.text == '1:Buy peacock feathers' for row in rows), "New to-do item did not appear in table -- its text was:\n{}".format(table.text)
        #)






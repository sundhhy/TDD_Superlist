from django.test import TestCase
from .views import home_page
from django.http import HttpRequest
#from django.core.urlresolvers import  resolve
from django.urls import reverse
# Create your tests here.
class Homepage(TestCase):
    def test_root_url_resolves_to_home_page(self):
        found = reverse('home')
        #self.assertEqual(found.func, home_page)
        #django 2.01已经不支持resolve了
        print('test resolves')
        self.assertEqual(found, '/')

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        print('res ' + html)
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        #html.strip().endswith 增加了strip是为了把空白字符给排除在判断之外
        self.assertTrue(html.strip().endswith('</html>'))
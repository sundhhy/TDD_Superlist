from django.test import TestCase
from .views import home_page
from django.http import HttpRequest
#from django.core.urlresolvers import  resolve
from django.urls import reverse
from django.template.loader import render_to_string
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
        expected_html = render_to_string('home.html')
        self.assertEqual(html.strip(), expected_html)

    def test_use_home_templates(self):
        response = self.client.get('/')
        self.assertEqual(response.content.decode('utf8'),render_to_string('home.html'))

    def test_hone_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
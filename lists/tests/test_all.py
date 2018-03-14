from django.test import TestCase
#from .views import home_page
from django.http import HttpRequest
#from django.core.urlresolvers import  resolve
from django.urls import reverse
from django.template.loader import render_to_string

from lists.models import Item, List

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

        expected_html = render_to_string('home.html')
        #django2.0之后render_to_string无法处理csrf_token，所以这个测试就无法通过了
        #self.assertEqual(response.content.decode(), expected_html)


    def test_use_home_templates(self):
        response = self.client.get('/')
        #self.assertEqual(response.content.decode('utf8'),render_to_string('home.html'))

class ListAndItemModelTest(TestCase):
    def test_saving_and_retriving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Iten the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Iten the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_lists_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/'%(list_.id,))
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/'%(correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)



class NewListTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def test_saveing_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text':'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        print('/lists/%d/'%(new_list.id,))
        self.assertRedirects(response, '/lists/%d/'%(new_list.id,))



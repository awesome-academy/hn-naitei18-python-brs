from django.test import TestCase
from django.urls import reverse

from review.models import Category, Book

DEFAULT_IMAGE = 'media/book_pics/book1.jpeg'

class BooksListViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    # Create 13 authors for pagination tests
    number_of_books = 7
    category = Category.objects.create(name='Novel')
    for book_id in range(number_of_books):
      Book.objects.create(
        title=f'The Giver {book_id}',
        category=category,
        author=f'Lois Lowry {book_id}',
        vote=5.0,
        desc='This is test',
        image=DEFAULT_IMAGE
      )
          
  def test_view_url_exists_at_desired_location(self):
    response = self.client.get('/review/books')
    self.assertEqual(response.status_code, 200)
          
  def test_view_url_accessible_by_name(self):
    response = self.client.get(reverse('books'))
    self.assertEqual(response.status_code, 200)
      
  def test_view_uses_correct_template(self):
    response = self.client.get(reverse('books'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'books/books.html')
      
  def test_pagination_is_six(self):
    response = self.client.get(reverse('books'))
    self.assertEqual(response.status_code, 200)
    self.assertTrue('is_paginated' in response.context)
    self.assertTrue(response.context['is_paginated'] == True)
    self.assertTrue(len(response.context['book_list']) == 6)

  def test_lists_all_books(self):
    # Get second page and confirm it has (exactly) remaining 3 items
    response = self.client.get(reverse('books')+'?page=2')
    self.assertEqual(response.status_code, 200)
    self.assertTrue('is_paginated' in response.context)
    self.assertTrue(response.context['is_paginated'] == True)
    self.assertTrue(len(response.context['book_list']) == 1)

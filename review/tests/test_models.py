from django.test import TestCase
from review.models import Category, Book, Rating
from django.contrib.auth.models import User

class BookModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    # Set up non-modified objects used by all test methods
    category = Category.objects.create(name='Novel')
    Book.objects.create(title='The Giver', category=category, author='Lois Lowry', vote=4.0, desc="This is test")

  def test_title_label(self):
    book = Book.objects.get(id=1)
    field_label = book._meta.get_field('title').verbose_name
    self.assertEquals(field_label, 'title')

  def test_category_label(self):
    book = Book.objects.get(id=1)
    field_label = book._meta.get_field('category').verbose_name
    self.assertEquals(field_label, 'category')

  def test_author_label(self):
    book = Book.objects.get(id=1)
    field_label = book._meta.get_field('author').verbose_name
    self.assertEquals(field_label, 'author')

  def test_vote_label(self):
    book = Book.objects.get(id=1)
    field_label = book._meta.get_field('vote').verbose_name
    self.assertEquals(field_label, 'vote')

  def test_desc_label(self):
    book = Book.objects.get(id=1)
    field_label = book._meta.get_field('desc').verbose_name
    self.assertEquals(field_label, 'desc')

  def test_get_absolute_url(self):
    book = Book.objects.get(id=1)
    self.assertEquals(book.get_absolute_url(), '/review/books/1')

  def test_get_str(self):
    book = Book.objects.get(id=1)
    self.assertEquals(book.__str__(), 'The Giver')

  def test_get_vote(self):
    book = Book.objects.get(id=1)
    self.assertEquals(book.get_vote(), 4)

  def test_get_actual_rating(self):
    book = Book.objects.get(id=1)
    self.assertEquals(book.actual_rating, [0,1,2,3])
  
  def test_get_hidden_rating(self):
    book = Book.objects.get(id=1)
    self.assertEquals(book.hidden_rating, [0])

class RatingModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username = 'chikyuu291', password='1234Abcd@@')
    category = Category.objects.create(name='Novel')
    book = Book.objects.create(title='The Giver', category=category, author='Lois Lowry', vote=4.0, desc="This is test")
    Rating.objects.create(user=user, star=5, book=book, review='So good')

  def test_get_str(self):
    rating = Rating.objects.get(id=1)
    self.assertEquals(rating.__str__(), 'chikyuu291 reviewed The Giver')
  
  def test_get_actual_rating(self):
      rating = Rating.objects.get(id=1)
      self.assertEquals(rating.actual_rating, [0,1,2,3,4])
    
  def test_get_hidden_rating(self):
    rating = Rating.objects.get(id=1)
    self.assertEquals(rating.hidden_rating, [])

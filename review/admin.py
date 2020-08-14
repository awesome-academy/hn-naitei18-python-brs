from django.contrib import admin
from .models import (
  Book,
  Category,
  Rating,
  BookMark,)

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  # list_display = ('name',)
  # fields = ('name', )
  pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  # list_display = ('title', 'author', 'image', 'desc', 'category')
  # fields = ('title', 'author', 'image', 'description', 'category')
  # search_fields = ['title']
  pass

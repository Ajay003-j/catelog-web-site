from django.contrib import admin
from .models import Genre, Book

admin.site.register(Genre)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')
    list_filter = ('author',)
    search_fields = ('title', 'isbn')

# @admin.register(User)
# class SiginAdmin(admin.ModelAdmin):
#     list_display = ('username',)
#     list_filter = ('username',)
from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Publisher, Contributor, Book, BookContributor, Review

admin.site.register(Publisher)
admin.site.register(Contributor)
admin.site.register(BookContributor)
admin.site.register(Review)
admin.site.register(Book)
admin.site.site_title = 'Booky Administration'
admin.site.site_header = 'Booky Admin'


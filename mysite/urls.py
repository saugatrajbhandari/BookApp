
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import AdminSite


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path('api/', include('reviews.api.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "mysite.views.page_not_found_view"
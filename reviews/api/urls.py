from django.urls import path

from . import views

from rest_framework import routers
from rest_framework.authtoken import views as auth_views

router = routers.SimpleRouter()
router.register(r'books', views.BookModelViewSet, basename='books')
router.register(r'publisher', views.PublisherModelViewSet, basename='publishers')


urlpatterns = [
    path('contributors/', views.ContributorView.as_view(), name='contributors'),

    path('login/', auth_views.obtain_auth_token)

]

urlpatterns += router.urls
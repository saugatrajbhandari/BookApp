from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>', views.book_detail, name='book_detail'),
    path('book-search', views.book_search, name='book_search'),
    path('publishers/<int:pk>', views.publisher_edit, name='publisher_edit'),
    path('publishers/new', views.publisher_edit, name='publisher_create'),
    path('review-edit/<int:book_pk>/<int:review_pk>', views.review_edit,name='review_edit'),
    path('books/<int:pk>/media/', views.book_media, name='book_media'),
    path('bookcreate/', views.book_create, name='book_create'),
    path('bookupdate/<int:pk>', views.book_update, name='book_update'),

    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup')
]


from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authv_views

from . import views as user_views


urlpatterns = [

    path('index/', user_views.home, name='home'),
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),
    path('user/books/', user_views.all_user_books, name='all_user_books'),
    path('user/archive/', user_views.user_archive, name="user_archive"),
    path('<str:username>/home/', user_views.user_home, name='user_home'),
    path('books/<str:category>/', user_views.book_cat_list, name='book_cat_list'),
    path('books/view/<int:book_id>/', user_views.per_book, name="per_book"),
    path('book/add/', user_views.add_book, name='add_book')

    #path('<int:question_id>/', views.details, name='detail'),

]
from django.urls import path
from . import views


urlpatterns = [     
    path("home/", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("books/", views.get_books, name="books"),
    path("genres/", views.get_genres, name="genres"),
    path('get_book/<int:book_id>/', views.get_specific_book, name="get_book"),
    # path("genres/", views.genres, name="genres")
]
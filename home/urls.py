from django.urls import path
from . import views


urlpatterns = [     
    path("home/", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("update_user/", views.update_user, name="update_user"),
    path("books/", views.get_books, name="books"),
    path("genres/", views.get_genres, name="genres"),
    path('get_book/<int:book_id>/', views.get_specific_book, name="get_book"),
    path("download_book/<int:book_id>", views.download_pdf,name="download_book"),
    path('get_book_content/<int:book_id>', views.get_book_content, name="get_book_content"),
    path('get_book_page/<int:book_id>/page/<int:page_number>/', views.get_book_page, name="get_book_page"),
    path('collection/', views.collection, name="collection"),
]
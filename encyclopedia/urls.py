from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("addnewpage/", views.add_entry, name="add_newpage"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit_entry"),
    path('random_page/', views.random_page, name='random_page')
]

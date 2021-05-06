from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/<str:title>", views.get, name="get"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("randomPage", views.randomPage, name="randomPage")
]
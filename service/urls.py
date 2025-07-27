from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-url", views.create_url, name="edit-url"),
    path("edit-url", views.edit_url, name="edit_url"),
    path("url/<str:url_name>/", views.visit_url, name="visit_url")
]
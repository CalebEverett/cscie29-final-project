from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:applicationquestion_id>/", views.detail, name="detail"),
    path("<int:applicationquestion_id>/results/", views.results, name="results"),
]
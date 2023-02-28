from . import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path("process/", views.process_picture, name="process_picture"),
]
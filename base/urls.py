from django.urls import path
from .views import base, tools

urlpatterns = [
    path("", base.home, name="home"),
    path("import_persons/", tools.import_persons, name="import_persons"),
]

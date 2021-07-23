from django.urls import path

from cdbmeta.api import views

urlpatterns = [
    path("create-record/", views.CreateMetaRecordAPI.as_view(), name="create-record"),
]

from django.urls import path
from .views import triage, hospitals
urlpatterns=[path('triage/',triage),path('hospitals/',hospitals)]

from django.urls import path

from . import views

urlpatterns = [
    path('reporters/', views.reporters_collection, name='reporters_collection'),
    path('issues/', views.issues_collection, name='issues_collection'),
]

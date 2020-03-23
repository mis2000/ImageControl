from django.urls import path
from rest_framework import routers
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('photo/', views.index, name='index'),
    path(r'checkFile', views.checkFileExists.as_view()),
    path(r'checkAlternativeFile', views.checkAlternativeFileExists.as_view()),
    path('alternativeImage/', views.alternativeImage, name='alternativeImage')
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='match-home'),
    path('about/', views.about, name='match-about'),
    # path('match/', views.find, name='match-find')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='match-home'),
    path('match', views.matchAlgorithm, name='matchAlgorithm'),
]

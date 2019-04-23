from django.urls import path
from . import views
from .views import (
    # GroupListView,
    GroupDetailView,
    GroupCreateView,
    GroupUpdateView,
    GroupDeleteView
)

urlpatterns = [
    path('', views.home, name='match-home'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('group/new/', GroupCreateView.as_view(), name='group-create'),
    path('group/<int:pk>/update/', GroupUpdateView.as_view(), name='group-update'),
    path('group/<int:pk>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    path('about/', views.about, name='match-about'),
    path('match/', views.find_match, name='match-find'),
]

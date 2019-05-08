from django.urls import path
from . import views
from .views import (
    # GroupListView,
    GroupDetailView,
    GroupCreateView,
    GroupUpdateView,
    GroupDeleteView,
    PrefsDetailView,
    PrefsCreateView,
    PrefsUpdateView,
)

urlpatterns = [
    path('', views.home, name='match-home'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('group/new/', GroupCreateView.as_view(), name='group-create'),
    path('group/<int:pk>/update/', GroupUpdateView.as_view(), name='group-update'),
    path('group/<int:pk>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    path('about/', views.about, name='match-about'),
    path('faq/', views.faq, name='match-faq'),
    path('match/', views.match_all, name='match-all'),
    path('match/group/<int:pk>/', views.match_group, name='match-group'),
    path('preferences/<int:pk>/', PrefsDetailView.as_view(), name='prefs-detail'),
    path('preferences/new/', PrefsCreateView.as_view(), name='prefs-create'),
    path('preferences/<int:pk>/update/', PrefsUpdateView.as_view(), name='prefs-update')
]

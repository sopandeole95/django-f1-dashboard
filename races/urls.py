from .views import LastRaceResultsView
from django.urls import path
from .views import (
    RaceListView, RaceCreateView,
    RaceUpdateView, RaceDeleteView
)

urlpatterns = [
    path('races/', RaceListView.as_view(), name='race-list'),
    path('races/add/', RaceCreateView.as_view(), name='race-add'),
    path('races/<int:pk>/edit/', RaceUpdateView.as_view(), name='race-edit'),
    path('races/<int:pk>/delete/', RaceDeleteView.as_view(), name='race-delete'),
    path('races/last/',  LastRaceResultsView.as_view(), name='race-last'),
]



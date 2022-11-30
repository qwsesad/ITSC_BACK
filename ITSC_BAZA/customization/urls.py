from django.urls import path, include
from . import views

urlpatterns = [
    path('api/cards/', views.CardsListGet.as_view()),
    path('api/cards/commandMembers/', views.CommandListGet.as_view()),
    path('api/cards/guests/', views.GuestsListGet.as_view()),
]
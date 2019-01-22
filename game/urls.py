"""my_project_name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URL
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import DeckListView, DeckCreateView, DeckDetailView, DeckUpdateView

urlpatterns = [
    path('', views.home, name="game-home"),
    path('deck/', DeckListView.as_view(), name="game-decks"),
    path('deck/<int:pk>/', DeckDetailView.as_view(), name="game-deck"),
    path('deck/create/', DeckCreateView.as_view(), name="game-decks-create"),
    path('deck/update/<int:pk>/', DeckUpdateView.as_view(), name="game-decks-update"),
    path('play/', views.play, name="game-play"),
    path('card/buy/', views.buy, name="game-buy"),
    path('start/', views.startgameform, name="game-start-form"),
    path('join/', views.joingameform, name="game-join-form"),
    path('play/turn/', views.gameboard, name="game-turn"),
    path('play/join/', views.joingame, name="game-turn"),
    path('play/start/', views.startgame, name="game-start"),
]

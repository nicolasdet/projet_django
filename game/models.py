from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .manager import CardManager
from django.contrib.postgres.fields import JSONField


class Card(models.Model):
    title = models.CharField(max_length=100)
    effect = models.TextField(default=" ".join([]))
    element = models.TextField(default="normal")
    type = models.TextField(default="terrain")
    cost = models.IntegerField(default=2)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = CardManager()

    def __str__(self):
        return self.title


class Deck(models.Model):
    title = models.CharField(max_length=100)
    date_create = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, related_name="cards")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("game-deck", kwargs={'pk': self.pk})


class Game(models.Model):
    player_one = models.TextField(max_length=100)
    deck_one = models.TextField(max_length=100)
    bot = models.BooleanField(null=True)
    player_two = models.TextField(max_length=100, null=True)
    deck_two = models.TextField(max_length=100, null=True)
    state = models.TextField(max_length=999999, null=True)
    date_create = models.DateTimeField(default=timezone.now)

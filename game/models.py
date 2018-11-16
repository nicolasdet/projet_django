from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Deck(models.Model):
    title = models.CharField(max_length=100)
    date_create = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Card(models.Model):
    title = models.CharField(max_length=100)
    effect = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class CardOnwership(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

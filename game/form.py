from django import forms
from django.core.exceptions import ValidationError
from .models import Deck, Card, Game
from django.contrib.auth.models import User


class DeckForm(forms.ModelForm):
    cards = forms.ModelMultipleChoiceField(
        queryset=Card.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DeckForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Deck
        fields = ['title', 'cards']

    def clean_cards(self):
        cards = self.cleaned_data['cards']
        if cards.count() <= 20:
            raise ValidationError("un deck doit contenir au minimum 20 cartes")
        return cards

class GameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Game
        fields = ['deck_one']

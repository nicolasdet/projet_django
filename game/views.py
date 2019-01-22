import json
import pprint

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Deck, Card, Game
from .form import DeckForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Count
from django.db import models
import random

from django.http import HttpResponse


def debug(object):
    return HttpResponse("<br>".join([str(g) + " : " + str(object.__getattribute__(g)) for g in object.__dict__]))


def debug_g(object):
    return HttpResponse(object)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        else:
            return None


class GameInstance:
    def __init__(self, game=None):
        self.game = game
        self.player_1 = -1
        self.player_2 = -1
        self.turn = 1  # random.randint(1, 2)
        self.player_turn = 0
        self.player_1_zone = self.player_2_zone = {
            'hand': [],
            'deck': [],
            'cemetery': [],
            'monster_1': [],
            'monster_2': [],
            'monster_3': [],
            'monster_4': [],
            'terrain_1': [],
            'terrain_2': [],
            'terrain_3': [],
            'terrain_4': []
        }
        return None

    def get_game_id(self):
        return self.game

    def get_player_turn(self):
        return self.player_turn

    def save(self):
        if self.game is not None:
            game = Game.objects.filter(id=self.game).first()
            data = self.__dict__
            for k in ["player_1_zone", "player_2_zone"]:
                d = []
                for i in data[k]:
                    d.append([j.save() for j in data[k][i]])
                data[k] = d
            game.state = json.dumps(data, ensure_ascii=False)
            game.save()
            # return json.dumps(data, ensure_ascii=False)
        return self

    def load(self):
        if self.game is None:
            return False
        game = Game.objects.filter(id=self.game).first()
        if game.state is None:
            game.state = "{}"
        state = json.loads(game.state)
        for k in ["player_1_zone", "player_2_zone"]:
            d = []
            if k in state:
                for i in range(0, len(state[k])):
                    d.append([CardInstance.load(j) for j in state[k][i]])
        self.__dict__ = {**state, **self.__dict__}
        return self.__dict__

    def join(self, player, deck):
        self.player_2 = player
        data = [CardInstance(i) for i in Deck.objects.filter(id=deck).first().cards.all()]
        self.player_2_zone['deck'] = data
        self.player_turn = 2
        self.load()
        # player 1 draw 4
        # player_2_draw_5
        return self

    def create(self, player, deck):
        self.game = Game.objects.create(player_one=player, deck_one=deck, bot=0).id
        self.player_1 = player
        data = [CardInstance(i) for i in Deck.objects.filter(id=deck).first().cards.all()]
        self.player_2_zone['deck'] = data
        self.player_turn = 1
        return self

    def draw(self):
        card = self.player_1_zone["deck"].pop()
        if not card:
            self.end()
        self.player_1_zone["hand"].append(card)
        return self

    def shuffle_deck(self):
        return self

    def end(self):
        return self

    def shuffle_deck_1(self):
        return self

    def shuffle_deck_2(self):
        return self

    def get_player_zone(self):
        if self.player_turn == "1":
            return self.player_1_zone
        return self.player_2_zone

    def get_opponent_zone(self):
        if self.player_turn == "1":
            return self.player_2_zone
        return self.player_1_zone


class CardInstance:
    def __init__(self, card=None):
        if card is not None:
            self.type = card.type
            self.effect = card.effect.split(' ')
            self.element = card.element
            self.cost = card.cost
            self.attack = card.attack
            self.defense = card.defense
            self.title = card.title
        return None

    def save(self):
        return self.__dict__

    @staticmethod
    def load(data):
        c = CardInstance()
        c.__dict__ = data
        return c

    def is_monster(self):
        return self.type == 'monster'

    def is_terrain(self):
        return self.type == 'terrain'

    def is_magic(self):
        return self.type == 'magic'

    def get_cost(self):
        if self.is_terrain():
            return False
        return self.cost

    def get_element(self):
        return self.element

    def get_attack(self):
        if not self.is_monster():
            return False
        return self.attack

    def get_defense(self):
        if not self.is_monster():
            return False
        return self.defense

    def get_strengh(self):
        if not self.is_magic():
            return False
        return self.attack


def home(request):
    return render(request, 'game/home.html')


def play(request):
    return render(request, 'game/play.html')


class DeckListView(ListView):
    model = Deck

    def get_queryset(self):
        decks = Deck.objects.filter(owner=self.request.user)
        return decks


class DeckDetailView(DetailView):
    model = Deck


class DeckUpdateView(UpdateView):
    model = Deck
    form_class = DeckForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class DeckCreateView(CreateView):
    model = Deck
    form_class = DeckForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


def buy(request, pk=""):
    data = request.get_full_path().split("/")[-1]
    count = 0
    if data == "bronze":
        count = 3
    if data == "silver":
        count = 7
    if data == "gold":
        count = 15
    Card.objects.create_card(request.user)
    return render(request, 'game/buy.html')


def startgameform(request):
    return render(request, 'game/create_form.html', {
        'decks': Deck.objects.filter(owner=request.user),
    })


def joingameform(request):
    return render(request, 'game/join_form.html', {
        'decks': Deck.objects.filter(owner=request.user),
        'games': [{"id": i.id, "title": User.objects.filter(id=i.player_one).first().username} for i in
                  Game.objects.filter(player_two__isnull=True)]
    })


def startgame(request):
    deck = request.GET.get("deck")
    if deck is None:
        return HttpResponse("<br>".join(request.POST.__dict__.keys()))

    bot = request.GET.get("bot")
    g = GameInstance()
    g.create(request.user.id, deck)
    request.session["game_id"] = g.get_game_id()
    request.session["player_turn"] = g.get_player_turn()
    return render(request, 'game/waiting.html', {})


def joingame(request):
    p1 = request.GET.get("game")
    deck = request.GET.get("deck")
    g = GameInstance(p1)
    g.join(request.user.id, deck)
    request.session["game_id"] = g.get_game_id()
    request.session["player_turn"] = g.get_player_turn()
    g.draw()
    g.draw()
    g.draw()
    g.draw()
    g.save()
    return render(request, 'game/gameboard.html', {
        "player_hand": g.get_player_zone()[0],
        "opponent": g.get_opponent_zone()
    })


def gameboard(request):
    g = GameInstance(request.session["game_id"])
    return render(request, 'game/gameboard.html', {
        "player_hand": g.get_player_zone().hand,
        "opponent": g.get_opponent_zone()
    })

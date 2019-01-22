from django.db import models
import random


class CardManager(models.Manager):
    def create_card(self, user):
        types = [
            "terrain",
            "magic",
            "monster"
        ]
        type = random.choice(types)
        attack = 0
        defense = 0
        cost = random.randint(0, 3)
        element = random.choice([
            "fire",
            "water",
            "air",
            "earth",
            "life",
            "death"
        ])
        effect = ""
        if type == "monster":
            title = "Monster Card"
            effects = [
                "piercing",
                "freezing",
                "flight",
                "double-attack",
                "direct-attack",
                "no-death-attack",
                "no-death-defense",
            ]
            effect = " ".join([random.choice(effects), random.choice(effects)])
            attack = random.randint(0, 25)
            defense = random.randint(0, 25)
        if type == "magic":
            effects = random.choice([
                "freezing",
                "damage",
                "heal",
                "heal-monster"
            ])
            effect = [random.choice(effects)]
            attack = random.randint(0, 25)
            title = "".join(effect) + str(attack)
        if type == "terrain":
            attack = random.randint(0, 3)
            title = "terrain - " + element + " - " + str(attack)

        card = self.create(
            title=title,
            effect=effect,
            element=element,
            type=type,
            owner=user,
            cost=cost,
            attack=attack,
            defense=defense
        )
        return card

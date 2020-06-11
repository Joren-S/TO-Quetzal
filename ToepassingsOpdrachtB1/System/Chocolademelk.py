import time
import random
from System import Chocoladeshot
from System import Marshmallow

class Chocolademelk:
    def __init__(self, prijs=2.0):
        self.prijs = prijs
        self.id = int(time.time() + random.randint(0, 10000000))
        self.ingredients = []
        self.workload = 5

    def setPrijs(self, newprijs):
        self.prijs = newprijs

    def getPrijs(self):
        return self.prijs

    def getID(self):
        return self.id

    def setID(self, newID):
        self.id = newID

    def getWorkload(self):
        return self.workload

    def getIngredients(self):
        return self.ingredients

    def addShotWit(self, shot):
        self.ingredients.append((shot, "shot_wit"))
        self.prijs += shot.getPrijs()
        self.workload += 1
        return True

    def addShotMelk(self, shot):
        self.ingredients.append((shot, "shot_melk"))
        self.prijs += shot.getPrijs()
        self.workload += 1
        return True

    def addShotBruin(self, shot):
        self.ingredients.append((shot, "shot_bruin"))
        self.prijs += shot.getPrijs()
        self.workload += 1
        return True

    def addShotZwart(self, shot):
        self.ingredients.append((shot, "shot_zwart"))
        self.prijs += shot.getPrijs()
        self.workload += 1
        return True

    def addHoning(self, honing):
        self.ingredients.append((honing, "honing"))
        self.prijs += honing.getPrijs()
        self.workload += 1
        return True

    def addMarshmallow(self, marshmallow):
        self.ingredients.append((marshmallow, "marshmallow"))
        self.prijs += marshmallow.getPrijs()
        self.workload += 1
        return True

    def addChili(self, chilipeper):
        self.ingredients.append((chilipeper, "chili"))
        self.prijs += chilipeper.getPrijs()
        self.workload += 1
        return True


import time

from ADTs    import Queue
from wrapper import *


class stock:
    def __init__(self):
        '''
        Maakt een stock aan dat alle sub-stocks voor de opgeslagen producten bevat.
        Initieel zijn alle stocks leeg.
        '''
        self.shot_wit = Wrapper(ADT_TYPE.DubbelGelinkteKetting)
        self.shot_melk = Wrapper(ADT_TYPE.DubbelGelinkteKetting)
        self.shot_bruin = Wrapper(ADT_TYPE.DubbelGelinkteKetting)
        self.shot_zwart = Wrapper(ADT_TYPE.DubbelGelinkteKetting)
        self.honing = Wrapper(ADT_TYPE.DubbelGelinkteKetting)
        self.marshmallow = Wrapper(ADT_TYPE.DubbelGelinkteKetting)
        self.chili = Wrapper(ADT_TYPE.DubbelGelinkteKetting)




     # Toevoegen van ingrediënten (bij aankoop)

    def addShotWit(self, shot):
        '''
        Voeg een shot object toe aan de bijhorende stock en geeft terug of dit gelukt is.
        '''
        return self.shot_wit.insert(shot.getVervaldatum(), shot)

    def addShotMelk(self, shot):
        '''
        Voeg een shot object toe aan de bijhorende stock en geeft terug of dit gelukt is.
        '''
        return self.shot_melk.insert(shot.getVervaldatum(), shot)

    def addShotBruin(self, shot):
        '''
        Voeg een shot object toe aan de bijhorende stock en geeft terug of dit gelukt is.
        '''
        return self.shot_bruin.insert(shot.getVervaldatum(), shot)

    def addShotZwart(self, shot):
        '''
        Voeg een shot object toe aan de bijhorende stock en geeft terug of dit gelukt is.
        '''
        return self.shot_zwart.insert(shot.getVervaldatum(), shot)

    def addHoning(self, honing):
        '''
        Voeg een honing object toe aan de bijhorende stock en geeft terug of dit gelukt is.
        '''
        return self.honing.insert(honing.getVervaldatum(), honing)

    def addMarshmallow(self, marshmallow):
        '''
        Voeg een marshmallow object toe aan de bijhorende stock en geeft terug of dit gelukt is.
        '''
        return self.marshmallow.insert(marshmallow.getVervaldatum(), marshmallow)

    def addChili(self, chili):
        '''
        Voeg een chili object toe aan de bijhorende stock en geeft terug of dit gelukt is.
        '''
        return self.chili.insert(chili.getVervaldatum(), chili)







    # Stock-functies voor het toevoegen van een ingredient aan een chocolademelk

    
    def removeShotWit(self):
        '''
        Verwijderd het shot object met de eerstkomende vervaldatum uit de bijhorende stock en geeft dit object terug en of dit gelukt is.
        Return is van de vorm (shot, boolean)
        '''
        items = self.shot_wit.traverse()
        if (not items):
            return (None, False)
        return (items[0], self.shot_wit.delete(items[0].getVervaldatum()))

    def removeShotMelk(self):
        '''
        Verwijderd het shot object met de eerstkomende vervaldatum uit de bijhorende stock en geeft dit object terug en of dit gelukt is.
        Return is van de vorm (shot, boolean)
        '''
        items = self.shot_melk.traverse()
        if (not items):
            return (None, False)
        return (items[0], self.shot_melk.delete(items[0].getVervaldatum()))

    def removeShotBruin(self):
        '''
        Verwijderd het shot object met de eerstkomende vervaldatum uit de bijhorende stock en geeft dit object terug en of dit gelukt is.
        Return is van de vorm (shot, boolean)
        '''
        items = self.shot_bruin.traverse()
        if (not items):
            return (None, False)
        return (items[0], self.shot_bruin.delete(items[0].getVervaldatum()))

    def removeShotZwart(self):
        '''
        Verwijderd het shot object met de eerstkomende vervaldatum uit de bijhorende stock en geeft dit object terug en of dit gelukt is.
        Return is van de vorm (shot, boolean)
        '''
        items = self.shot_zwart.traverse()
        if (not items):
            return (None, False)
        return (items[0], self.shot_zwart.delete(items[0].getVervaldatum()))

    def removeHoning(self):
        '''
        Verwijderd het honing object met de eerstkomende vervaldatum uit de bijhorende stock en geeft dit object terug en of dit gelukt is.
        Return is van de vorm (honing, boolean)
        '''
        items = self.honing.traverse()
        if (not items):
            return (None, False)
        return (items[0], self.honing.delete(items[0].getVervaldatum()))

    def removeMarshmallow(self):
        '''
        Verwijderd het marshmallow object met de eerstkomende vervaldatum uit de bijhorende stock en geeft dit object terug en of dit gelukt is.
        Return is van de vorm (marshmallow, boolean)
        '''
        items = self.marshmallow.traverse()
        if (not items):
            return (None, False)
        return (items[0], self.marshmallow.delete(items[0].getVervaldatum()))

    def removeChili(self):
        '''
        Verwijderd het chili object met de eerstkomende vervaldatum uit de bijhorende stock en geeft dit object terug en of dit gelukt is.
        Return is van de vorm (chili, boolean)
        '''
        items = self.chili.traverse()
        if (not items):
            return (None, False)
        return (items[0], self.chili.delete(items[0].getVervaldatum()))







    # Stock beheer: info + purgen van individuele (of alle) stocks.


    def getStockCount(self, type):
        '''
        Geeft terug hoeveel ingrediënten er in de sub-stock (die bij 'type' hoort) zitten.
        '''
        if type == 'shot_wit':
            return self.shot_wit.getSize()
        elif type == 'shot_melk':
            return self.shot_melk.getSize()
        elif type == 'shot_bruin':
            return self.shot_bruin.getSize()
        elif type == 'shot_zwart':
            return self.shot_zwart.getSize()
        elif type == 'honing':
            return self.honing.getSize()
        elif type == 'marshmallow':
            return self.marshmallow.getSize()
        elif type == 'chili':
            return self.chili.getSize()

    def setPrice(self, type, price):
        '''
        Verandert de prijs van een product in de stock.
        '''
        adt = None
        if type == 'shot_wit':
            adt = self.shot_wit
        elif type == 'shot_melk':
            adt = self.shot_melk
        elif type == 'shot_bruin':
            adt = self.shot_bruin
        elif type == 'shot_zwart':
            adt = self.shot_zwart
        elif type == 'honing':
            adt = self.honing
        elif type == 'marshmallow':
            adt = self.marshmallow
        elif type == 'chili':
            adt = self.chili

        items = adt.traverse()
        if (items is not None):
            for i in items:
                i.setPrijs(price)

    def purgeIndividual(self, stock_to_purge):
        '''
        Controleert een sub-stock en verwijderd producten waarvan de vervaldatum is verstreken.
        Geeft terug hoeveel items er zijn verwijderd.
        '''
        items_purged = 0
        stock_items = stock_to_purge.traverse()
        if stock_items is not None:
            for i in stock_items:
                if i.getVervaldatum() < time.time():
                    items_purged += 1
                    stock_to_purge.delete(i.getVervaldatum())
        return items_purged

    def purge(self):
        '''
        Controleert alle sub-stocks en verwijderd producten waarvan de vervaldatum is verstreken.
        Geeft terug hoeveel items er zijn verwijderd.
        '''
        items_purged = 0
        items_purged += self.purgeIndividual(self.shot_bruin)
        items_purged += self.purgeIndividual(self.shot_melk)
        items_purged += self.purgeIndividual(self.shot_wit)
        items_purged += self.purgeIndividual(self.shot_zwart)
        items_purged += self.purgeIndividual(self.honing)
        items_purged += self.purgeIndividual(self.marshmallow)
        items_purged += self.purgeIndividual(self.chili)
        return items_purged


    def isIngredientValid(self, ingredientInfo):
        #ingredientInfo = (ingredientobject, string_type)
        f = getattr(ingredientInfo[0], "getVervaldatum", None)
        if callable(f):
            if ingredientInfo[1] == 'shot_wit':
                retInfo = self.shot_wit.retrieve(ingredientInfo[0].getVervaldatum())
                return retInfo[1]
            elif ingredientInfo[1] == 'shot_melk':
                retInfo = self.shot_melk.retrieve(ingredientInfo[0].getVervaldatum())
                return retInfo[1]
            elif ingredientInfo[1] == 'shot_bruin':
                retInfo = self.shot_bruin.retrieve(ingredientInfo[0].getVervaldatum())
                return retInfo[1]
            elif ingredientInfo[1] == 'shot_zwart':
                retInfo = self.shot_zwart.retrieve(ingredientInfo[0].getVervaldatum())
                return retInfo[1]
            elif ingredientInfo[1] == 'honing':
                retInfo = self.honing.retrieve(ingredientInfo[0].getVervaldatum())
                return retInfo[1]
            elif ingredientInfo[1] == 'marshmallow':
                retInfo = self.marshmallow.retrieve(ingredientInfo[0].getVervaldatum())
                return retInfo[1]
            elif ingredientInfo[1] == 'chili':
                retInfo = self.chili.retrieve(ingredientInfo[0].getVervaldatum())
                return retInfo[1]

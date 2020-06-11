import time
import random

class Gebruiker:
    def __init__(self, voornaam, naam, email, timeID):
        self.naam = (voornaam + " " + naam)
        self.email = email
        self.id = int(time.time() + random.randint(0, 10000000))
        self.bestellingCount = 0
        self.bestellingen = []
        self.time_id = timeID

    def getNaam(self):
        return self.naam

    def setNaam(self, voornaam, naam):
        self.naam = voornaam + " " + naam

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email

    def getID(self):
        return self.id

    def setID(self, newID):
        self.id = newID

    def getTimeID(self):
        return self.time_id

    def setTimeID(self, newID):
        self.time_id = newID

    def getBestellingen(self):
        return self.bestellingen

    def getBestellingCount(self):
        return self.bestellingCount

    def addBestelling(self, bestelling):
        self.bestellingen.append(bestelling)
        self.bestellingCount += 1

    def annuleerBestellingen(self):
        self.bestellingen = []
        self.bestellingCount = 0
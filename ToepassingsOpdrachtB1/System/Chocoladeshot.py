class Chocoladeshot:
    def __init__(self, shotType, vervaldatum, prijs=1.0):
        self.shotType = None
        self.vervaldatum = vervaldatum
        self.prijs = prijs
        self.setType(shotType)

    def getType(self):
        # shot_wit shot_melk shot_bruin shot_zwart
        return self.shotType

    def setType(self, shotType):
        self.shotType = shotType

    def getPrijs(self):
        return self.prijs

    def setPrijs(self, newprijs):
        self.prijs = newprijs

    def getVervaldatum(self):
        return self.vervaldatum

    def setVervaldatum(self, datum):
        self.vervaldatum = datum



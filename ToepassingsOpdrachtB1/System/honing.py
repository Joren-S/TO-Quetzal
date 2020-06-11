class honing:

    def __init__(self, vervaldatum, prijs=0.5):
        self.vervaldatum = vervaldatum
        self.prijs = prijs

    def getPrijs(self):
        return self.prijs

    def setPrijs(self, newprijs):
        self.prijs = newprijs

    def getVervaldatum(self):
        return self.vervaldatum

    def setVervaldatum(self, datum):
        self.vervaldatum = datum


class chili:

    def __init__(self, vervaldatum, prijs=0.25):
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


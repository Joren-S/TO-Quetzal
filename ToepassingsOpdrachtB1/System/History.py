class History:
    _registry = []

    def __init__(self, time_id, stack, nieuwebestelling, wBestellingen, stock, processingTimeLeft, werknemers):
        History._registry.append(self)
        self.Time_id = time_id
        self.Stack = stack
        self.Nieuwebestelling = nieuwebestelling
        self.WachtendeBestellingen = wBestellingen
        self.Stock = stock
        self.processingTimeLeft = processingTimeLeft
        self.werknemers = werknemers

    def getRegistry():
        try:
            return History._registry
        except:
            return []

    def getTijdstip(self):
        try:
            return self.Time_id
        except:
            return []

    def getStack(self):
        try:
            return self.Stack
        except:
            return []

    def getStockCount(self, type):
        try:
            return self.Stock[type]
        except:
            return ""

    def getNieuweBestelling(self):
        try:
            return self.Nieuwebestelling
        except:
            return ""

    def getWachtendeBestellingen(self):
        try:
            return self.WachtendeBestellingen
        except:
            return []

    def getBestellingTimeRemaining(self):
        try:
            return self.processingTimeLeft
        except:
            return 0

    def getWerknemers(self):
        try:
            return self.werknemers
        except:
            return []
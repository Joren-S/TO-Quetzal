import time
import random

class Werknemer:
    def __init__(self, voornaam, naam, workload, timeID):
        self.naam = voornaam + " " + naam
        self.workload = workload
        self.maxWorkload = workload
        self.id = int(time.time() + random.randint(0, 10000000))
        self.time_id = timeID

    def getNaam(self):
        return self.naam

    def setNaam(self, voornaam, naam):
        self.naam = voornaam + " " + naam

    def getMaxWorkload(self):
        return self.maxWorkload

    def setMaxWorkload(self, workload):
        self.maxWorkload = int(workload)

    def getID(self):
        return self.id

    def setID(self, newID):
        self.id = newID

    def getTimeID(self):
        return self.time_id

    def setTimeID(self, newID):
        self.time_id = newID

    def restoreWorkload(self):
        self.workload = int(self.maxWorkload)

    def doWork(self, workload):
        if workload <= self.workload:
            self.workload -= workload
            self.workload = int(self.workload)
            return True
        else:
            return False

    def getWorkload(self):
        return self.workload
import time
import random

class ORDER_STATE:
    Idle, Processing, Finished, Aborted = range(4)

class bestelling:
    def __init__(self, email, chocoID, time_id, state: ORDER_STATE = ORDER_STATE.Idle):
        self.tijd = time.time() + (random.randint(0, 99) * 0.001)
        self.email = email
        self.chocoID = chocoID
        self.status = state
        self.time_id = time_id
        self.time_remaining = -1
        self.worker_id = -1
        
    def getTijd(self):
        return self.tijd

    def setTijd(self, newtijd):
        self.tijd = newtijd

    def getTimeID(self):
        return self.time_id

    def setTimeID(self, newId):
        self.time_id = newId

    def getWorker(self):
        return self.worker_id

    def setWorker(self, new_workerid):
        self.worker_id = new_workerid

    def getTimeRemaining(self):
        return self.time_remaining

    def setTimeRemaining(self, time_r):
        self.time_remaining = time_r

    def getEmail(self):
        return self.email

    def setEmail(self, newemail):
        self.email = newemail

    def getChocolademelk(self):
        return self.chocoID

    def setChocolademelk(self, chocoID):
        self.chocoID = chocoID

    def getStatus(self):
        return self.status

    def setStatus(self, newStatus: ORDER_STATE):
        self.status = newStatus

    def getStatusAsString(self):
        if (self.status == ORDER_STATE.Idle):
            return "Queued"
        elif (self.status == ORDER_STATE.Processing):
            return "Busy"
        elif (self.status == ORDER_STATE.Finished):
            return "Finished"
        elif (self.status == ORDER_STATE.Aborted):
            return "Cancelled"

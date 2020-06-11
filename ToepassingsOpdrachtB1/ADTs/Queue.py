''' 
Python file for the implementation of queue for TO GA&S.

Author:     Max Van Houcke

'''

class queue:
    def __init__(self, items = []):
        self.items = items
        self.size = 0

    def isEmpty(self):
        """
        kijkt of queue leeg is
        :return: true als de queue leeg is, false zoniet
        """
        if self.items == []:
            return True
        else:
            return False

    def enqueue(self, newItem):
        """
        zet een nieuw item in de queue
        :param newItem: het item dat in de queue moet worden gezet
        :return: True als het is gelukt
        """
        self.items.append(newItem)
        self.size += 1
        return True

    def dequeue(self):
        """
        verwijdert de kop van de queue
        :return: true als het is gelukt, false zoniet
        """
        if not self.isEmpty():
            self.items.pop(0)
            self.size -= 1
            return True
        else:
            return False

    def getFront(self):
        """
        geeft de kop van de queue terug
        :return: de kop van de queue, None indien leeg
        """
        if not self.isEmpty():
            return self.items[0]
        else:
            return None

    def print(self):
        """
        hulpfunctie die de queue in volgorde uitprint
        :return: leeg
        """
        for i in self.items:
            print(i)

    def traverse(self):
        """
        hulpfunctie die de queue in volgorde teruggeeft
        :return: lijst met waarden
        """
        ret = []
        for i in self.items:
            ret.append(i)
        return ret

    def getSize(self):
        return self.size

    def getLast(self):
        """
        geeft de het laatste element van de queue terug
        :return: het laatste element van de queue, None indien leeg
        """
        if not self.isEmpty():
            return self.items[-1]
        else:
            return None
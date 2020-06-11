''' 
Python file for the implementation of the double linked chain for TO GA&S.

Author:     Joren Servotte

'''

class DGK_Node:
    def __init__(self, zoeksleutel, waarde):
        """ Maakt een nieuwe node aan. """
        self.searchkey = zoeksleutel
        self.value = waarde
        self.prev = None
        self.next = None

    def getZoeksleutel(self):
        """ Returned de zoeksleutel in de node. """
        return self.searchkey

    def getWaarde(self):
        """ Returned de waarde in de node. """
        return self.value

    def getPrev(self):
        """ Returned het vorige object in de ketting. """
        return self.prev

    def getNext(self):
        """ Returned het volgende object in de ketting. """
        return self.next

    def setPrev(self, newPrev):
        """ Veranderd het vorige object in de ketting naar 'newPrev'. """
        self.prev = newPrev

    def setNext(self, newNext):
        """ Veranderd het volgende object in de ketting naar 'newNext'. """
        self.next = newNext



class DGK:
    def __init__(self):
        """ Initialiseert de ketting, zonder nodes. """
        self.head = None
        self.ok = False

    def insert(self, zoeksleutel, waarde):
        """ Insert de waarde, in een nieuwe node, op de juiste plaats in de ketting. """
        try:
            tmpNode = DGK_Node(zoeksleutel, waarde)
            if (self.isEmpty()):
                self.head = tmpNode
            else:                
                if (self.head.getZoeksleutel() == tmpNode.getZoeksleutel()):
                    return False
                elif (tmpNode.getZoeksleutel() < self.head.getZoeksleutel()):
                    tmpNode.setNext(self.head)
                    self.head.setPrev(tmpNode)
                    self.head = tmpNode
                else:
                    if (self.head.getNext() is None):
                        tmpNode.setPrev(self.head)
                        self.head.setNext(tmpNode)
                    else:
                        srchNode = self.head
                        while (srchNode.getNext() is not None):
                            if (tmpNode.getZoeksleutel() > srchNode.getZoeksleutel()):
                                srchNode = srchNode.getNext()
                            else:
                                break

                        tmpNode.setNext(srchNode)
                        tmpNode.setPrev(srchNode.getPrev())
                        tmpNode.getNext().setPrev(tmpNode)
                        tmpNode.getPrev().setNext(tmpNode)
            return True
        except:
            return False

    def delete(self, node):
        """ Delete de node 'node' (node is een node, geen waarde) uit de ketting. """
        try:
            if (node.getPrev() is not None):
                if (node.getNext() is None):
                    node.getPrev().setNext(None)
                else:
                    node.getPrev().setNext(node.getNext())
            if (node.getNext() is not None):
                if (node.getPrev() is None):
                    node.getNext().setPrev(None)
                    self.head = node.getNext()
                else:
                    node.getNext().setPrev(node.getPrev())
            else:
                # tree is empty after deletion, we're deleting the only node.
                self.head = None

            return True
        except:
            return False

    def isEmpty(self):
        """ Returned of de ketting leeg is. """
        return self.head == None

    def getLength(self):
        """ Returned de lengte van de ketting (aantal nodes). """
        if (self.isEmpty()):
            return 0
        try:
            count = 1
            srchNode = self.head
            while (srchNode.getNext() != None):
                count = count + 1
                srchNode = srchNode.getNext()
            return count
        except:
            return 0

    def retrieve(self, zoeksleutel):
        """ Zoekt de node met zoeksleutel 'zoeksleutel' en returned deze in een tuple met een bool of de operatie is gelukt (node, bool). """
        if (self.isEmpty()):
            return (None, False)
        else:
            srchNode = self.head
            while True:
                if (srchNode is None):
                    break
                if (srchNode.getZoeksleutel() == zoeksleutel):
                    return (srchNode, True)
                srchNode = srchNode.getNext()
            return (None, False)

    def inorderTraverse(self):
        values = []
        srchNode = self.head
        for i in range(0, self.getLength()):
            values.append(srchNode.getWaarde())
            srchNode = srchNode.getNext()
        return values

    def createDOT(self):
        """ Maakt een DOT-bestand 'DGK-dot.dot' aan. """
        with open('DGK-dot.dot', 'w') as f:
            print("digraph G {", file=f)
            items = "\t"
            arrows = ""
            node = self.head
            while (node is not None):
                items += str(node.getZoeksleutel()) + ","
                if (node.getPrev() is not None):
                     arrows += "\t" + str(node.getPrev().getZoeksleutel()) + " -> " + str(node.getZoeksleutel()) + "\n"
                     arrows += "\t" + str(node.getZoeksleutel()) + " -> " + str(node.getPrev().getZoeksleutel()) + "\n"
                node = node.getNext()
            items = items[:-1]
            items += " [style=\"solid\"]"
            arrows += "}"
            print(items, file=f)
            print(arrows, file=f)


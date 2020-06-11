''' 
Python file for the implementation of the stack for TO GA&S.

Author:     Joren Servotte

'''

class StackNode:
    def __init__(self, waarde, vorig = None):
        """ Maakt een nieuwe node aan. """
        self.value = waarde
        self.prev = vorig

    def getWaarde(self):
        """ Geeft de waarde in de node terug. """
        return self.value
          
    def getPrev(self):
        """ Geeft de vorige node terug. """
        return self.prev

class Stack:
    def __init__(self):
        self.createStack()
          
    def createStack(self):
        """ Maakt een lege stack. """
        self.top = None

    def destroyStack(self):
        """ Wist een stack. """
        self.top = None

    def isEmpty(self):
        """ Geeft terug of de stack leeg is. """
        return self.top == None

    def push(self, waarde):
        """ Voegt 'waarde' toe in een nieuwe node op de top van de stack. """
        tmpNode = StackNode(waarde, self.top)
        self.top = tmpNode
        return self.top == tmpNode

    def pop(self):
        """ Geeft de waarde van de node op de top van de stack terug. Verwijderd vervolgens deze node """
        if self.isEmpty():
            retval = -1
            success = False
        else:
            retval = self.top.getWaarde()
            self.top = self.top.getPrev()
            success = True
        return (retval, success)

    def getTop(self):
        """ Geeft de waarde van de node op de top van de stack terug. """
        if self.isEmpty():
            retval = -1
            success = False
        else:
            retval = self.top.getWaarde()
            success = True
        return (retval, success)

    def traverse(self):
        items = []
        if self.isEmpty() is False:
            node = self.top
            while (node is not None):
                items.append(node.getWaarde())
                node = node.getPrev()
        return items

    def createDOT(self):
        """ Maakt een DOT bestand 'stack-dot.dot' aan. """
        with open('stack-dot.dot', 'w') as f:
            print("digraph G {", file=f)
            items = "\t"
            arrows = ""
            node = self.top
            while (node is not None):
                items += str(node.getWaarde()) + ","
                if (node.getPrev() is not None):
                        arrows += "\t" + str(node.getWaarde()) + " -> " + str(node.getPrev().getWaarde()) + "\n"
                node = node.getPrev()
            items = items[:-1]
            items += " [style=\"solid\"]"
            arrows += "}"
            print(items, file=f)
            print(arrows, file=f)

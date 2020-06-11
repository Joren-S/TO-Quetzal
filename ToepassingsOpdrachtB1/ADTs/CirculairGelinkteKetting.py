''' 
Python file for the implementation of the circular linked chain for TO GA&S.

Author:     Max Van Houcke

'''

class node:
    def __init__(self, data, pointer):
        self.data = data
        self.pointer = pointer


class circularlinkedchain:
    def __init__(self, items = []):
        self.items = items

    def __del__(self):
        self.items = []

    def IsEmpty(self):
        """
        kijkt of de ketting leeg is
        :return: true als de ketting leeg is, false zoniet
        """
        if self.items == []:
            return True
        else:
            return False

    def getLength(self):
        """
        geeft de lengte van de ketting
        :return: int lengte van de ketting
        """
        return len(self.items)

    def insert(self, data, index):
        """
        zet een nieuw item in de ketting
        :param data: de gegevens dat het item bevat
        :param index: de index waar het item moet worden gezet
        :return: geeft true als het inserten is gelukt, false zoniet
        """
        if 0 <= index <= self.getLength():   #
            if self.getLength() == 0:
                newnode = node(data, None)
                self.items.append(newnode)
                newnode.pointer = self.items[0]
                return True
            else:
                self.items.append(None)
                for i in range(self.getLength()-2, index-1, -1):
                    self.items[i+1] = self.items[i]
                if index == self.getLength()-1:
                    newnode = node(data, self.items[0])
                    self.items[index] = newnode
                    self.items[index-1].pointer = self.items[index]
                    return True
                elif index == 0:
                    newnode = node(data, self.items[index + 1])
                    self.items[index] = newnode
                    self.items[self.getLength()-1].pointer = self.items[0]
                    return True
                else:
                    newnode = node(data, self.items[index+1])
                    self.items[index] = newnode
                    self.items[index-1].pointer = self.items[index]
                    return True
        else:
            return False

    def delete(self, index):
        """
        verwijdert een item uit de ketting
        :param index: index van het item dat verwijderd moet worden
        :return: true als het deleten is gelukt, false zoniet
        """
        if 0 <= index < self.getLength():
            if index == 0 or index == self.getLength()-1:
                self.items.pop(index)
                self.items[self.getLength()-1].pointer = self.items[0]
                return True
            else:
                self.items.pop(index)
                self.items[index-1].pointer = self.items[index]
                return True
        else:
            return False

    def retrieve_by_index(self, index):
        """
        geeft een item terug uit de lijst
        :param index: index van het item dat moet worden teruggegeven
        :return: het item samen met true als het is gelukt, false zoniet
        """
        if 0 <= index < self.getLength():
            dataItem = self.items[index].data
            return dataItem, True
        else:
            return False

    def retrieve(self, searchkey):
        """
        Zoekt een item met een bepaalde searchkey.
        :param searchkey: searchkey van de te zoeken node
        :return: item, None als het niet gelukt is
        """
        items = self.traverse()
        print(items)
        for i in items:
            if i[0][0] == searchkey:
                return i[0][1]
        return None

    def traverse(self):
        """
        hulpfunctie die de ketting in volgorde teruggeeft
        :return: leeg
        """
        if self.IsEmpty():
            return []

        buffer = []
        result = []
        for i in self.items:
            buffer.append(i.data[0])
            print(buffer)
            buffer.sort()
        for sk in buffer:
            ret = self.retrieve_by_index(self.get_id_for_searchkey(sk))
            if ret is not False:
                result.append(ret)
        return result

    def traverse_unsort(self):
        """
        hulpfunctie die de ketting teruggeeft
        :return: leeg
        """
        list = []
        for i in self.items:
            list.append(i.data)
        return list

    def get_id_for_searchkey(self, searchkey):
        index = -1
        items = self.traverse_unsort()
        for i in items:
            index += 1
            if i[0] == searchkey:
                return index
        return index
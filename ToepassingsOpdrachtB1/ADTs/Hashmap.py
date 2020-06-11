''' 
Python file for the implementation of the hashmap for TO GA&S.

Author:     Max Van Houcke

'''

class tableitem:
    def __init__(self, item, key, next = None, previous = None):
        self.item = item
        self.key = key
        self.next = next
        self.previous = previous

    def __del__(self):
        self.item = None
        self.key = None
        self.next = None
        self.previous = None

class hashmap:
    def __init__(self, size, collisiontype):
        self.size = size
        self.length = 0
        self.collisiontype = collisiontype
        self.list = self.initializelist()

    def __del__(self):
        self.size = 0
        self.length = 0
        self.list = []

    def tableLength(self):
        """
        returns the amount of items stored in the table
        :return: amount of items stored in the table
        """
        return self.length

    def tableInsert(self, item):
        """
        inserts a given item into the table
        :param item: the given item, of type tableitem
        :return: bool true if successful, false if not
        """
        if self.tableRetrieve(item.key):
            return False

        #hash function
        position = item.key % self.size

        #insertion
        if self.list[position] is None:
            self.list[position] = item
            self.length += 1
            return True

        #collision
        else:
            #linear probing
            if self.collisiontype == "linprob":
                for i in range(1, self.size):
                    newposition = (position + i) % self.size
                    if self.list[newposition] is None:
                        self.list[newposition] = item
                        self.length += 1
                        return True

            #quadratic probing
            elif self.collisiontype == "quadprob":
                for i in range(1, self.size):
                    newposition = (position + i**2) % self.size
                    if self.list[newposition] is None:
                        self.list[newposition] = item
                        self.length += 1
                        return True

            #separate chaining, linked chain (double)
            elif self.collisiontype == "sepchain":
                laatstenode = self.list[position]
                while laatstenode.next != None:
                    laatstenode = laatstenode.next
                laatstenode.next = item
                item.previous = laatstenode
                self.length += 1
                return True
        return False

    def tableRetrieve(self, key):
        """
        finds an item in the table with a given key and returns it, together with a bool success
        :param key: search key of item
        :return: the item with the given search key, bool true if successful, false if not
        """
        #hash function
        position = key % self.size

        #if position out of hash function gives the right element, found it
        if self.list[position] is not None:
            if self.list[position].key == key:
                    return self.list[position], True

        #linear probing
        if self.collisiontype == "linprob":
            for i in range(1, self.size):
                newposition = (position + i) % self.size
                if self.list[newposition] is not None:
                    if self.list[newposition].key == key:
                        return self.list[newposition], True

        #quadratic probing
        elif self.collisiontype == "quadprob":
            for i in range(1, self.size):
                newposition = (position + i**2) % self.size
                if self.list[newposition] is not None:
                    if self.list[newposition].key == key:
                        return self.list[newposition], True

        #separate chaining
        elif self.collisiontype == "sepchain":
            if self.list[position] is not None:
                huidigenode = self.list[position]
                while huidigenode.next != None and huidigenode.key != key:
                    huidigenode = huidigenode.next
                if huidigenode.key == key:
                    return huidigenode, True

        return False

    def tableDelete(self, key):
        """
        deletes an item from the table with a given search key and returns a bool success
        :param key: search key of item
        :return: bool true if successful, false if not
        """
        #hash function
        position = key % self.size

        #if the element is not in the table, return false
        if self.tableRetrieve(key) == False:
            return False

        # linear probing
        elif self.collisiontype == "linprob":
            #element is in the position from the hash function
            if self.list[position] is not None:
                if self.list[position].key == key:
                    self.list[position] = None
                    self.length -= 1
                    return True
            #not in the first position so search by linear probing
            for i in range(1, self.size):
                newposition = (position + i) % self.size
                if self.list[newposition] is not None:
                    if self.list[newposition].key == key:
                        self.list[newposition] = None
                        self.length -= 1
                        return True

        # quadratic probing
        elif self.collisiontype == "quadprob":
            # element is in the position from the hash function
            if self.list[position] is not None:
                if self.list[position].key == key:
                    self.list[position] = None
                    self.length -= 1
                    return True
            # not in the first position so search by quadratic probing
            for i in range(1, self.size):
                newposition = (position + i ** 2) % self.size
                if self.list[newposition] is not None:
                    if self.list[newposition].key == key:
                        self.list[newposition] = None
                        self.length -= 1
                        return True

        # separate chaining
        elif self.collisiontype == "sepchain":
            if self.list[position] is not None:
                huidigenode = self.list[position]
                #element is the first of the chain, rearrange and delete
                if huidigenode.key == key:
                    next = huidigenode.next
                    self.list[position] = next
                    if next != None:
                        next.previous = None
                    self.length -= 1
                    return True
                #else find the element in the chain
                while huidigenode.next != None and huidigenode.key != key:
                    huidigenode = huidigenode.next
                #rearrange the chain
                if huidigenode.key == key:
                    huidigenode.previous.next = huidigenode.next
                    if huidigenode.next != None:
                        huidigenode.next.previous = huidigenode.previous
                    huidigenode.__del__
                    self.length -= 1
                    return True

        return False

    def changeHashFunction(self, size):
        """
        changes the hash function used for the insert, which is dependent of the size
        this function changes the size and the hash function becomes: H(x)= x % size
        :param size: the new size
        :return: True for success
        """
        while self.size > size:
            self.list.pop(self.size-1)
            self.size -= 1
        while self.size < size:
            self.list.append(None)
            self.size += 1
        return True

    def changeCollisionType(self, type):
        """
        changes how collision is dealt with: either linear probing, quadratic probing or separate chaining
        :param type: the new type of collision resolution
        :return: True if successful, false if not
        """
        if type == "linprob" or type == "quadprob" or type == "sepchain":
            if type != self.collisiontype:
                self.collisiontype = type
                return True
        return False

    def print(self):
        """
        prints the table like a python list
        does not show any linked chains
        :return:
        """
        print("[", end="")
        for i in range(self.size):
            if self.list[i] is None:
                print(None, end="")
            else:
                print(self.list[i].key, end="")
            if i != self.size-1:
                print(", ", end="")

        print("]")

    def printalt(self):
        """
        prints the table, any linked chain is visible
        :return:
        """
        print("________")
        for i in range(self.size):
            if i < 10:
                print(i, "  ", end="")
            else:
                print(i, " ", end="")
            if self.list[i] is None:
                print(None)
            else:
                print(self.list[i].key, end="")
                next = self.list[i].next
                while next != None:
                    print(" -> ", end="")
                    print(next.key, end="")
                    next = next.next

                print()

        print("________")


    def initializelist(self):
        """
        initializes the table by making a list with None in it
        :return:
        """
        list = [None] * self.size
        return list

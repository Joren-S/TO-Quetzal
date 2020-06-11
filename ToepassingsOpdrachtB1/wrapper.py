# Author: Joren Servotte
from ADTs import RedBlackTree
from ADTs import DubbelGelinkteKetting

# Author: Max Van Houcke
from ADTs import Hashmap
from ADTs import CirculairGelinkteKetting

# Author: Lars Houtman
from ADTs import TweeDrieBoom
from ADTs import BinaireZoekboom



# ADT's not used by wrapper, but used elsewhere.
from ADTs import Queue
from ADTs import Stack




class ADT_TYPE:
    '''
    Class for all the different ADTs.
    '''
    RoodZwartBoom, DubbelGelinkteKetting, Hashmap, CirculairGelinkteKetting, TweeDrieBoom, BinaireZoekboom = range(6)



class Wrapper:

    def __init__(self, type: ADT_TYPE):
        '''
        Initializes an ADT with the specified type.
        '''
        self.adt_type = type
        self.adt = None
        self.initADT()


    def insert(self, zoeksleutel, waarde):
        '''
        Inserts into the ADT based on the type specified when initializing the wrapper.
        Returns if the insert succeeded or not.
        '''
        if (self.adt_type == ADT_TYPE.RoodZwartBoom): # ✓
            return self.adt.insert(zoeksleutel, waarde)

        elif (self.adt_type == ADT_TYPE.DubbelGelinkteKetting): # ✓
            return self.adt.insert(zoeksleutel, waarde)

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            node = BinaireZoekboom.object(zoeksleutel, waarde)
            return self.adt.insert(node)

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            node = TweeDrieBoom.object(zoeksleutel, waarde)
            self.adt.insert(node)
            return True
    
        elif (self.adt_type == ADT_TYPE.CirculairGelinkteKetting):
            return self.adt.insert((zoeksleutel, waarde), self.adt.getLength())


    def delete(self, zoeksleutel):
        '''
        Deletes a value from the ADT based on the type specified when initializing the wrapper.
        Returns if the delete succeeded or not.
        '''
        if (self.adt_type == ADT_TYPE.RoodZwartBoom): # ✓
            return self.adt.delete(zoeksleutel)

        elif (self.adt_type == ADT_TYPE.DubbelGelinkteKetting): # ✓
            retrieval = self.adt.retrieve(zoeksleutel)
            if (retrieval[1] is True):
                return self.adt.delete(retrieval[0])
            return False

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            return self.adt.delete(zoeksleutel)

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            return self.adt.delete(zoeksleutel)
    
        elif (self.adt_type == ADT_TYPE.CirculairGelinkteKetting):
            return self.adt.delete(self.adt.get_id_for_searchkey(zoeksleutel))



    def retrieve(self, zoeksleutel):
        '''
        Looks for 'waarde' in the ADT based on the type specified when initializing the wrapper.
        Returns the value in the node associated to the searchkey (if found) and if retrieving was succesful (in a tuple: (value, boolean)).
        '''
        if (self.adt_type == ADT_TYPE.RoodZwartBoom): # ✓
            search = self.adt.search(zoeksleutel)
            if search[1] is True:
                return (search[0].value, search[1])
            return (None, search[1])

        elif (self.adt_type == ADT_TYPE.DubbelGelinkteKetting): # ✓
            search = self.adt.retrieve(zoeksleutel)
            if search[1] is True:
                return (search[0].getWaarde(), search[1])
            return (None, search[1])

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            search = self.adt.getItem(zoeksleutel)
            if (search is not False):
                return (search.restvalue, True)
            return (None, False)

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            search = self.adt.getItem(zoeksleutel)
            if (search is not False):
                return (search.restvalue, True)
            return (None, False)
    
        elif (self.adt_type == ADT_TYPE.CirculairGelinkteKetting):
            search = self.adt.retrieve(zoeksleutel)
            if (search is not None):
                return (search, True)
            return (None, False)


    def getSize(self):
        '''
        Returns the amount of nodes/elements in the ADT. (Integer)
        '''
        if (self.adt_type == ADT_TYPE.RoodZwartBoom): # ✓
            return self.adt.getSize()

        elif (self.adt_type == ADT_TYPE.DubbelGelinkteKetting): # ✓
            return self.adt.getLength()

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            return self.adt.getSize()

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            return self.adt.getSize()
    
        elif (self.adt_type == ADT_TYPE.CirculairGelinkteKetting):
            return self.adt.getLength()

        return 0


    def isEmpty(self):
        '''
        Returns if the ADT is empty or not. (Boolean)
        '''
        if (self.adt_type == ADT_TYPE.RoodZwartBoom): # ✓
            return self.adt.isEmpty()

        elif (self.adt_type == ADT_TYPE.DubbelGelinkteKetting): # ✓
            return self.adt.isEmpty()

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            return self.adt.empty()

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            return self.adt.empty()
    
        elif (self.adt_type == ADT_TYPE.CirculairGelinkteKetting):
            return self.adt.IsEmpty()

        return True


    def traverse(self):
        '''
        Traverses the ADT in the specified type (TRAVERSE_TYPE) and returns it in a list.
        Returns None if the tree is empty.
        '''
        if (self.adt_type == ADT_TYPE.RoodZwartBoom): # ✓
            return self.adt.inorderTraverse()

        elif (self.adt_type == ADT_TYPE.DubbelGelinkteKetting): # ✓
            return self.adt.inorderTraverse()

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            return self.adt.getList()

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            return self.adt.getList()
    
        elif (self.adt_type == ADT_TYPE.CirculairGelinkteKetting):
            fixed = []
            trav = self.adt.traverse()
            for i in trav:
                fixed.append(i[0][1])
            return fixed

        return []


    def makeDOT(self):        
        '''
        Builds a DOT file named ADT_TYPE.dot. Only works for tree-based ADT's.
        '''        
        if (self.adt_type == ADT_TYPE.RoodZwartBoom): # ✓
            return self.adt.make_dot("bzb.dot")

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            return self.adt.make_dot("bzb.dot")

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            return self.adt.make_dot("23b.dot")

        print("DOT Files are only available for tree-based ADT's!")
        return False

    # DEPENDENCIES

    def initADT(self):
        '''
        Function used when initalizing the ADT to create the proper ADT object.
        Not meant to be used standalone.
        '''
        if (self.adt_type == ADT_TYPE.RoodZwartBoom):
            self.adt = RedBlackTree.RBT()
            
        elif (self.adt_type == ADT_TYPE.DubbelGelinkteKetting): # ✓
            self.adt = DubbelGelinkteKetting.DGK()

        elif (self.adt_type == ADT_TYPE.BinaireZoekboom): # ✓
            self.adt = BinaireZoekboom.binarySearchTree()

        elif (self.adt_type == ADT_TYPE.TweeDrieBoom):
            self.adt = TweeDrieBoom.ttTree()
    
        elif (self.adt_type == ADT_TYPE.CirculairGelinkteKetting):
            self.adt = CirculairGelinkteKetting.circularlinkedchain()

class object:
    def __init__(self, key, restvalue):
        self.key = key
        self.restvalue = restvalue

class ttTree:
    class node:
        def __init__(self, parent=None, obj_1=None, obj_2=None, child_1=None, child_2=None, child_3=None):
            self.parent = parent
            self.obj_1 = obj_1
            self.obj_2 = obj_2
            self.obj_3 = None       # This object location should always be empty, except during an insert operation
            self.child_1 = child_1
            self.child_2 = child_2
            self.child_3 = child_3
            self.child_4 = None     # This child location should also be empty, except during an insert operation

        def sortObj(self):
            """
            This function is performed on a node. It puts their objects in their correct places, sorted by key.
            After sorting, if the node contains 3 objects (which isn't possible in 2-3 trees),
            it calls the function .split()
            """

            # If the object is in place 2 and there's none in place 1, put it back in place 1.
            if not self.obj_1 and self.obj_2 and not self.obj_3:
                self.obj_1 = self.obj_2
                self.obj_2 = None

            # If the node has two objects, compare them and, if their order was wrong, put them in their correct spot
            if self.obj_1 and self.obj_2 and not self.obj_3:
                if self.obj_1.key > self.obj_2.key:
                    temp = self.obj_2
                    self.obj_2 = self.obj_1
                    self.obj_1 = temp

            # If the node has three objects, comparison had too many cases, so this works as follows:
            # Make a list 'order', fill the list with every available object key. Sort the list,
            # and make three temporary objects in the right order of the list. Fill the original node with the temp objects;
            # they are now in their right order.
            if self.obj_1 and self.obj_2 and self.obj_3:
                #zet ze eerst in juiste volgorde
                order = []
                order.append(self.obj_1.key)
                order.append(self.obj_2.key)
                order.append(self.obj_3.key)
                order.sort()

                if order[0] == self.obj_1.key:
                    temp_1 = self.obj_1
                if order[0] == self.obj_2.key:
                    temp_1 = self.obj_2
                if order[0] == self.obj_3.key:
                    temp_1 = self.obj_3

                if order[1] == self.obj_1.key:
                    temp_2 = self.obj_1
                if order[1] == self.obj_2.key:
                    temp_2 = self.obj_2
                if order[1] == self.obj_3.key:
                    temp_2 = self.obj_3

                if order[2] == self.obj_1.key:
                    temp_3 = self.obj_1
                if order[2] == self.obj_2.key:
                    temp_3 = self.obj_2
                if order[2] == self.obj_3.key:
                    temp_3 = self.obj_3

                self.obj_1 = temp_1
                self.obj_2 = temp_2
                self.obj_3 = temp_3

                self.split()
                return True

        def merge(self, nodeToMergeWith):
            """
            This function is performed on the node in the tree that will get the new value on an insert.
            The 'nodeToMergeWith' is a subtree that needs to be merged, on a new insert this is a newly generated node.
            :param nodeToMergeWith: New (root of) subtree that needs to be merged in the original tree.
            """

            # If this new subtree has children, point their parents to the node called upon
            if nodeToMergeWith.hasChildren():
                if nodeToMergeWith.child_1:
                    nodeToMergeWith.child_1.parent = self
                if nodeToMergeWith.child_2:
                    nodeToMergeWith.child_2.parent = self
                if nodeToMergeWith.child_3:
                    nodeToMergeWith.child_3.parent = self
                if nodeToMergeWith.child_4:
                    nodeToMergeWith.child_4.parent = self

            # Effectively move the children by setting the children_ of the node called upon
                if not self.child_1:
                    if nodeToMergeWith.child_1:
                        self.child_1 = nodeToMergeWith.child_1
                    if nodeToMergeWith.child_2:
                        self.child_2 = nodeToMergeWith.child_2
                    self.sortChildren()

                elif self.child_1 and not self.child_2:
                    if nodeToMergeWith.child_1:
                        self.child_2 = nodeToMergeWith.child_1
                    if nodeToMergeWith.child_2:
                        self.child_3 = nodeToMergeWith.child_2
                    self.sortChildren()

                elif self.child_1 and self.child_2 and not self.child_3:
                    if nodeToMergeWith.child_1:
                        self.child_3 = nodeToMergeWith.child_1
                    if nodeToMergeWith.child_2:
                        self.child_4 = nodeToMergeWith.child_2
                    self.sortChildren()

            # If the node called upon doesn't have a second object, take the one from the node that's given
            if not self.obj_2:
                self.obj_2 = nodeToMergeWith.obj_1

            # If it does have a second object, and it doesn't have a third (which it shouldn't),
            elif not self.obj_3:
                self.obj_3 = nodeToMergeWith.obj_1

            # Now, sort the objects so the new object perfectly fits in. First sort the children though, because the
            # sortObj míght call a .split().
            self.sortChildren()
            self.sortObj()

        def split(self):
            """
            This function splits a node; it's called upon if a node has 3 objects. It creates a subtree (one 'root',
            two children. The left child has object 1 and child 1 and 2, the right child has object 3 and child 3 and 4.
            The root is left with object 2 (which is moved from spot 2 to spot 1)
            """
            # Create the two children using object 1 and 3. If the node called upon had children, they will be moved,
            # they will be moved accordingly.
            left_child = ttTree.node(self, self.obj_1)
            right_child = ttTree.node(self, self.obj_3)
            if self.hasChildren():
                if self.child_1:
                    self.child_1.parent = left_child
                    left_child.child_1 = self.child_1
                if self.child_2:
                    self.child_2.parent = left_child
                    left_child.child_2 = self.child_2
                if self.child_3:
                    self.child_3.parent = right_child
                    right_child.child_1 = self.child_3
                if self.child_4:
                    self.child_4.parent = right_child
                    right_child.child_2 = self.child_4

            # Using the 2 newly made nodes, create a subtree with the original node as root.
            self.child_1 = left_child
            self.child_2 = right_child
            self.child_3 = None
            self.child_4 = None
            self.obj_1 = self.obj_2
            self.obj_2 = None
            self.obj_3 = None

            # If the original node had a parent (which is always, except if the node to split was the root),
            if self.parent:
                # Remove the node as a child of its parent
                if self.parent.child_1:
                    if self.parent.child_1 == self:
                        self.parent.child_1 = None
                if self.parent.child_2:
                    if self.parent.child_2 == self:
                        self.parent.child_2 = None
                if self.parent.child_3:
                    if self.parent.child_3 == self:
                        self.parent.child_3 = None
                if self.parent.child_4:
                    if self.parent.child_4 == self:
                        self.parent.child_4 = None
                # Now sort the parent's children
                self.parent.sortChildren()
                # Merge the node with its parent. This is the 'pushing up' of the middle node. This cán create a
                # node with 3 objects: in that case, merge will call .split() again on that node. This will be done
                # recursively untill the problem is finished (which it always is after splitting the root)
                self.parent.merge(self)
            else:
                # If the node had no parents, just tell the new left- and right child their parent is the node
                # called upon.
                left_child.parent = self
                right_child.parent = self

            self.sortChildren()

        def sortChildren(self):
            """
            This function is called upon a node, and sorts its children based on their value in obj_1.key.
            """
            # In case of only one child: you can't compare, it just needs to be in spot 1.
            if self.amountOfChildren() == 1:
                # In this case, it' already in the right spot
                if self.child_1 and not self.child_2 and not self.child_3 and not self.child_4:
                    pass

                # In this case, move it from spot 2 to spot 1
                if not self.child_1 and self.child_2 and not self.child_3 and not self.child_4:
                    self.child_1 = self.child_2
                    self.child_2 = None

                # In this case, move it from spot 3 to spot 1
                if not self.child_1 and not self.child_2 and self.child_3 and not self.child_4:
                    self.child_1 = self.child_3
                    self.child_3 = None

                # Moving from spot 4 to spot 1 never happens, because spot 4 is only used in case all previous three
                # are already occupied.


            # In case of two children:
            # If they should always be in spot 1 and 2. If that's not the case, make it happen.
            elif self.amountOfChildren() == 2:
                if not self.child_1 and self.child_2 and self.child_3 and not self.child_4:
                    self.child_1 = self.child_2
                    self.child_2 = self.child_3
                    self.child_3 = None

                if self.child_1 and not self.child_2 and self.child_3 and not self.child_4:
                    self.child_2 = self.child_3
                    self.child_3 = None
                # Once in the correct spot, compare them to put them in their right order.
                if self.child_1 and self.child_2:
                    if self.child_1.obj_1.key > self.child_2.obj_1.key:
                        temp = self.child_2
                        self.child_2 = self.child_1
                        self.child_1 = temp

            # In case of three children:
            # Make a list with values, sort that list, and put them back in order.
            # For more in-depth explanation see ln. 37.
            elif self.amountOfChildren() == 3:
                #stel: 3 kinderen
                if self.child_1 and self.child_2 and self.child_3 and not self.child_4:
                    #haal de keydata eruit, maak een lijst, sorteer die, stop ze in volgorde van die lijst terug
                    order = []
                    order.append(self.child_1.obj_1.key)
                    order.append(self.child_2.obj_1.key)
                    order.append(self.child_3.obj_1.key)
                    order.sort()

                    if order[0] == self.child_1.obj_1.key:
                        temp_1 = self.child_1
                    if order[0] == self.child_2.obj_1.key:
                        temp_1 = self.child_2
                    if order[0] == self.child_3.obj_1.key:
                        temp_1 = self.child_3

                    if order[1] == self.child_1.obj_1.key:
                        temp_2 = self.child_1
                    if order[1] == self.child_2.obj_1.key:
                        temp_2 = self.child_2
                    if order[1] == self.child_3.obj_1.key:
                        temp_2 = self.child_3

                    if order[2] == self.child_1.obj_1.key:
                        temp_3 = self.child_1
                    if order[2] == self.child_2.obj_1.key:
                        temp_3 = self.child_2
                    if order[2] == self.child_3.obj_1.key:
                        temp_3 = self.child_3

                    self.child_1 = temp_1
                    self.child_2 = temp_2
                    self.child_3 = temp_3

            # In case of 4 children:
            # Same method as three children.
            elif self.amountOfChildren() == 4:
                if self.child_1 and self.child_2 and self.child_3 and self.child_4:
                    order = []
                    order.append(self.child_1.obj_1.key)
                    order.append(self.child_2.obj_1.key)
                    order.append(self.child_3.obj_1.key)
                    order.append(self.child_4.obj_1.key)
                    order.sort()

                    if order[0] == self.child_1.obj_1.key:
                        temp_1 = self.child_1
                    if order[0] == self.child_2.obj_1.key:
                        temp_1 = self.child_2
                    if order[0] == self.child_3.obj_1.key:
                        temp_1 = self.child_3
                    if order[0] == self.child_4.obj_1.key:
                        temp_1 = self.child_4

                    if order[1] == self.child_1.obj_1.key:
                        temp_2 = self.child_1
                    if order[1] == self.child_2.obj_1.key:
                        temp_2 = self.child_2
                    if order[1] == self.child_3.obj_1.key:
                        temp_2 = self.child_3
                    if order[1] == self.child_4.obj_1.key:
                        temp_2 = self.child_4

                    if order[2] == self.child_1.obj_1.key:
                        temp_3 = self.child_1
                    if order[2] == self.child_2.obj_1.key:
                        temp_3 = self.child_2
                    if order[2] == self.child_3.obj_1.key:
                        temp_3 = self.child_3
                    if order[2] == self.child_4.obj_1.key:
                        temp_3 = self.child_4

                    if order[3] == self.child_1.obj_1.key:
                        temp_4 = self.child_1
                    if order[3] == self.child_2.obj_1.key:
                        temp_4 = self.child_2
                    if order[3] == self.child_3.obj_1.key:
                        temp_4 = self.child_3
                    if order[3] == self.child_4.obj_1.key:
                        temp_4 = self.child_4

                    self.child_1 = temp_1
                    self.child_2 = temp_2
                    self.child_3 = temp_3
                    self.child_4 = temp_4

        def hasChildren(self):
            """
            Checks if the node operated on has children.
            :return: A boolean statement, which is true if the node has either .child_1, -_2, -_3, or -_4.
            """
            return self.child_1 or self.child_2 or self.child_3 or self.child_4

        def amountOfChildren(self):
            """
            Counts the amount of children, returns an integer with the amount of children
            :return: integer containing # of children
            """
            amount = 0
            if self.child_1:
                amount += 1
            if self.child_2:
                amount += 1
            if self.child_3:
                amount += 1
            if self.child_4:
                amount += 1
            return amount

    def __init__(self):
        self.root = ttTree.node()

    def go_to_leaf(self, node, obj):
        """
        This recursive function is called upon the tree, and returns the leaf node where a certain object would fit
        :param node: The node already descended to
        :param obj: The object we're looking for
        :return: The node containing obj
        """

        # Recursive Base case: the node descended to has no children. Thus it's a leaf; return node.
        if not node.child_1 and not node.child_2 and not node.child_3:
            return node
        else:
            # Descend into the tree; which child is descended to is determined by the key value; compare and go into
            # the correct child node.
            if node.obj_1.key > obj.key:
                return self.go_to_leaf(node.child_1, obj)
            if not node.obj_2:
                if node.obj_1.key < obj.key:
                    return self.go_to_leaf(node.child_2, obj)
            else:
                if node.obj_1.key < obj.key < node.obj_2.key:
                    return self.go_to_leaf(node.child_2, obj)
                if node.obj_2.key < obj.key:
                    return self.go_to_leaf(node.child_3, obj)

    def make_dot(self, filename):
        """
        This function creates a .dot file for the tree.
        :param filename: Output file name for .dot file
        """

        if self.empty():
            print("Could not make .dot: Tree empty")
            return False
        # Create an empty string for content
        content = ""
        # Begin at the root
        node = self.root

        # If the root has no children, just print the root. No need for recursive functions.
        if not node.hasChildren():
            content += "\""
            content += str(node.obj_1.key)
            if node.obj_2:
                content += " "
                content += str(node.obj_2.key)
            content += "\";"

        # In case root exists (which it nearly always does), call recursive function draw_children to fill content
        if self.root:
            content = self.draw_children(node, content)

        # Create the file using string content
        with open(filename, "w") as fout:
            fout.write("digraph \"2-3-Tree\" {")
            fout.write(content)
            fout.write("}")

        # Also print in console
        print("digraph \"Tree\" {")
        print(content)
        print("}")

    def draw_children(self, node, content):
        """
        This function recursively adds lines to the string 'content'.
        :param node: Node recursively descended to
        :param content: string 'content' as is
        :return: string 'content' with new nodes added.
        """

        # If the current node has an object, print it at the string 'current_node_values' for the beginning of the line
        current_node_values = str(node.obj_1.key)
        # If it has an object in the second spot too, add it to 'current_node_values'
        if node.obj_2:
            current_node_values += " "
            current_node_values += str(node.obj_2.key)

        # If the node has a first child, make a line with current_node_values, followed by an arrow, followed by the
        # value of obj_1 in the first child and, if necessery, the value from obj_2
        if node.child_1:
            content += "\""
            content += current_node_values
            content += "\" -> \""
            content += str(node.child_1.obj_1.key)
            if node.child_1.obj_2:
                content += " "
                content += str(node.child_1.obj_2.key)
            content += "\""
            content += "\n"

            # If this child node has children of itself, perform this recursively. Base case: There's no children.
            if node.child_1.child_1 or node.child_1.child_2 or node.child_1.child_3:
                content = self.draw_children(node.child_1, content)

        # This is repeated for child_2 and -_3. Child 4 should never be present (it's a 2-3-Tree) thus won't be printed.
        if node.child_2:
            content += "\""
            content += current_node_values
            content += "\" -> \""
            content += str(node.child_2.obj_1.key)
            if node.child_2.obj_2:
                content += " "
                content += str(node.child_2.obj_2.key)
            content += "\""
            content += "\n"
            if node.child_2.child_1 or node.child_2.child_2 or node.child_2.child_3:
                content = self.draw_children(node.child_2, content)

        if node.child_3:
            content += "\""
            content += current_node_values
            content += "\" -> \""
            content += str(node.child_3.obj_1.key)
            if node.child_3.obj_2:
                content += " "
                content += str(node.child_3.obj_2.key)
            content += "\""
            content += "\n"
            if node.child_3.child_1 or node.child_3.child_2 or node.child_3.child_3:
                content = self.draw_children(node.child_3, content)

        # Return the content string to the caller
        return content

    def inOrderTraverse(self, node, list):
        """
        This function recursively passes through the tree, and prints the node values inorder. Is callee for the
        .getList() function. In first call, this is the root of the tree.
        :param node: Node currently at while traversing
        :param list: list that keeps track of all values already passed
        :return: list, now containing values from current node.
        """

        # If (sub-)tree has a child_1, enter that node and perform this function again for that node.
        if node.child_1:
            list = self.inOrderTraverse(node.child_1, list)

        # Append the value of obj_1 to the list
        list.append(node.obj_1.restvalue)

        # If (sub-)tree has a child_2, enter that node and perform this function again for that node.
        if node.child_2:
            list = self.inOrderTraverse(node.child_2, list)

        # If this node has a second object, add that value to the list too
        if node.obj_2:
            list.append(node.obj_2.restvalue)

        # If this node ha sa child_3, enter that node and perform this function again for that node.
        if node.child_3:
            list = self.inOrderTraverse(node.child_3, list)

        # Return the list, as altered by this node (and all its sub-nodes)
        return list

    def inOrderTraverseCount(self, node, counter=None):
        """
        This function works the same as .inOrderTraverse(), but instead of appending values to a list, it initiates a
        counter that increments at each found object.
        :param node: Node currently at while traversing
        :param counter: Amount of objects currently found
        :return: Amount of objects found after traversing this node (and its children)
        """
        if not counter:
            counter = 0
        if node.child_1:
            counter = self.inOrderTraverseCount(node.child_1, counter)
        counter += 1

        if node.child_2:
            counter = self.inOrderTraverseCount(node.child_2, counter)

        if node.obj_2:
            counter += 1
        if node.child_3:
            counter = self.inOrderTraverseCount(node.child_3, counter)
        return counter

    def descendToNode(self, value, node=None):
        """
        This function recursively finds the node that contains a key value.
        Always called upon by .getItem() or .delete().
        :param value: given key we're trying to get the object of
        :param node: current node
        :return: node containing the object
        """
        # First check if tree is empty: if it is, descending to nodes cannot happen
        if self.empty():
            print("Could not descend to node: Tree empty")
            return False

        # For the first call, initiate first node as root

        if not node:
            node = self.root

        # If the root contains the value we're looking for, no recursive calls are necessary
        if node.obj_1.key == value:
            return node
        elif node.obj_2:
            if node.obj_2.key == value:
                return node

        # In case the node has no children (we're in a leaf node), and the value has not been found, the function
        # returns False.
        elif not node.hasChildren():
            return False

        # The following part decides which part child needs to be entered to look for the given key value.

        # In case the node has one object:
        if not node.obj_2:
            if value < node.obj_1.key:
                if node.child_1:
                    return self.descendToNode(value, node.child_1)
            else:
                if node.child_2:
                    return self.descendToNode(value, node.child_2)

        # In case the node has two objects:
        if node.obj_2:
            if value < node.obj_1.key:
                if node.child_1:
                    return self.descendToNode(value, node.child_1)
            elif node.obj_1.key < value < node.obj_2.key:
                if node.child_2:
                    return self.descendToNode(value, node.child_2)
            elif node.obj_2.key < value:
                if node.child_3:
                    return self.descendToNode(value, node.child_3)

    def getInorderSuccessor(self, value, node=None):
        """
        This function is used in the delete process. It returns the node containing the
        inOrderSuccessor of any value. This function is called by .swapWithInorderSuccessor()
        :param value: Value to find inorder successor of
        :param node: Node containing object of which we need the inorder successor, or one of its children on the way
                        towards this successo node
        :return:
        """

        # If the node given contains the value, go one child to the right
        if node.obj_1.key == value:
            return self.getInorderSuccessor(value, node.child_2)
        if node.obj_2:
            if node.obj_2.key == value:
                return self.getInorderSuccessor(value, node.child_3)

        # If the node now has a child_1 (which is always except if it's a leaf), enter this node and call same function
        if node.child_1:
            return self.getInorderSuccessor(value, node.child_1)
        else:
            # If it has no children, we're in a leaf: return the node.
            # The inorder successor in this node is always obj_1
            return node

    def swapWithInorderSuccessor(self, value):
        """
        This function is used in the .delete() function. When the to be deleted object is not in a leaf, we have to
        put it there for a relatively easy removal.
        :param value: The key value of the object to swap with its inorder successor (and then be deleted
        :return: The leaf node which now contains the swapped - and to be soon deleted - object
        """

        # Get the node currently containing our to be deleted object
        nodeContainingValue = self.descendToNode(value)
        # Get our inorder successor node
        nodeContainingSuccessor = self.getInorderSuccessor(value, nodeContainingValue)

        # Temporarily store our inorder successor. This can only be .obj_1!
        temp = nodeContainingSuccessor.obj_1

        # Make the swap (test for original object location first)
        if nodeContainingValue.obj_1.key == value:
            nodeContainingSuccessor.obj_1 = nodeContainingValue.obj_1
            nodeContainingValue.obj_1 = temp

        if nodeContainingValue.obj_2:
            if nodeContainingValue.obj_2.key == value:
                nodeContainingSuccessor.obj_1 = nodeContainingValue.obj_2
                nodeContainingValue.obj_2 = temp

        # Return the node now containing our to-be-deleted object
        return nodeContainingSuccessor

    def fixEmptyNode(self, node):
        """
        If an object was deleted from a node, and there's now an empty node: there's a problem. This function
        resolves that problem, by categorising 4 situations, of which one is recursive.
        :param node: Empty node
        :return:
        """

        # This boolean determines if one of the solutions was applicable to the situation. The situations are
        # in order of difficulty, so if a problem can be solved by a category 1 solution, it shouldn't try to fix the
        # problem later on.
        situationFound = False

        # Category 1: a close sibling has 2 objects

        # If current empty node is its parent's first child and..
        if node.parent:
            if node == node.parent.child_1 and not situationFound:
                # .. The parent's second child has two objects:
                if node.parent.child_2.obj_2:
                    situationFound = True
                    # Shuffle objects and children so our problem gets solved
                    node.obj_1 = node.parent.obj_1
                    node.parent.obj_1 = node.parent.child_2.obj_1
                    node.parent.child_2.obj_1 = node.parent.child_2.obj_2
                    node.parent.child_2.obj_2 = None
                    node.child_2 = node.parent.child_2.child_1
                    if node.child_2:
                        node.child_2.parent = node
                    node.parent.child_2.child_1 = None
                    node.parent.child_2.sortChildren()

            # If current empty node is its parent's second child and..
            if node == node.parent.child_2 and not situationFound:
                # .. The parent's first child has two objects:
                if node.parent.child_1.obj_2:
                    situationFound = True
                    # Shuffle objects and children so our problem gets solved
                    node.obj_1 = node.parent.obj_1
                    node.parent.obj_1 = node.parent.child_1.obj_2
                    node.parent.child_1.obj_2 = None
                    node.child_2 = node.parent.child_1.child_3
                    if node.child_2:
                        node.child_2.parent = node
                    node.sortChildren()
                    node.parent.child_1.child_3 = None
                # .. The parent's third child has two objects:
                elif node.parent.child_3:
                    if node.parent.child_3.obj_2:
                        situationFound = True
                        node.obj_1 = node.parent.obj_2
                        node.parent.obj_2 = node.parent.child_3.obj_1
                        node.parent.child_3.obj_1 = node.parent.child_3.obj_2
                        node.parent.child_3.obj_2 = None
                        node.child_2 = node.parent.child_3.child_1
                        node.parent.child_3.child_1 = None
                        node.parent.child_3.sortChildren()
                        if node.child_2:
                            node.child_2.parent = node
                        node.sortChildren()

            # If current empty node is its parent's third child and..
            if node == node.parent.child_3 and not situationFound:
                # .. The parent's second child has two objects:
                if node.parent.child_2.obj_2:
                    situationFound = True
                    # Shuffle objects and children so our problem gets solved
                    node.obj_1 = node.parent.obj_2
                    node.parent.obj_2 = node.parent.child_2.obj_2
                    node.parent.child_2.obj_2 = None
                    node.child_2 = node.parent.child_2.child_3
                    if node.child_2:
                        node.child_2.parent = node
                    node.parent.child_2.child_3 = None
                    node.parent.child_2.sortChildren()

            # Category 2: A non-neighbouring sibling has 2 objects

            # If the empty node is its parent's first child and..
            if node == node.parent.child_1 and not situationFound:
                # its parent's third child has two objects:
                if node.parent.child_3:
                    if node.parent.child_3.obj_2:
                        situationFound = True
                        # Shuffle objects and children so our problem gets solved
                        node.obj_1 = node.parent.obj_1
                        node.parent.obj_1 = node.parent.child_2.obj_1
                        node.parent.child_2.obj_1 = node.parent.obj_2
                        node.parent.obj_2 = node.parent.child_3.obj_1
                        node.parent.child_3.obj_1 = node.parent.child_3.obj_2
                        node.parent.child_3.obj_2 = None
                        node.child_2 = node.parent.child_2.child_1
                        node.parent.child_2.child_1 = node.parent.child_2.child_2
                        node.parent.child_2.child_2 = node.parent.child_3.child_1
                        node.parent.child_3.child_1 = None
                        node.parent.child_3.sortChildren()

            # If the empty node is its parent's third child and..
            if node == node.parent.child_3 and not situationFound:
                # its parent's first child has two objects:
                if node.parent.child_1.obj_2:
                    situationFound = True
                    # Shuffle objects and children so our problem gets solved
                    node.obj_1 = node.parent.obj_2
                    node.parent.obj_2 = node.parent.child_2.obj_1
                    node.parent.child_2.obj_1 = node.parent.obj_1
                    node.parent.obj_1 = node.parent.child_1.obj_2
                    node.parent.child_1.obj_2 = None
                    node.child_2 = node.parent.child_2.child_2
                    node.sortChildren()
                    node.parent.child_2.child_2 = node.parent.child_1.child_3
                    node.parent.child_2.sortChildren()
                    node.parent.child_1.child_3 = None
                    node.parent.child_1.sortChildren()

            # Category 3: the parent has 3 objects, and all the siblings have one object
            if node.parent.obj_2 and not situationFound:

                situationFound = True
                # If the empty node is the parent's first child:
                if node == node.parent.child_1:
                    node.obj_1 = node.parent.obj_1
                    node.parent.obj_1 = node.parent.child_2.obj_1
                    node.parent.child_3.obj_2 = node.parent.child_3.obj_1
                    node.parent.child_3.obj_1 = node.parent.obj_2
                    node.parent.obj_2 = None
                    node.child_2 = node.parent.child_2.child_1
                    node.sortChildren()
                    node.parent.child_3.child_3 = node.parent.child_2.child_2
                    node.parent.child_3.sortChildren()
                    node.parent.child_2 = node.parent.child_3
                    node.parent.child_3 = None

                # If the empty node is the parent's second child:
                if node == node.parent.child_2:
                    node.parent.child_3.obj_2 = node.parent.child_3.obj_1
                    node.parent.child_3.obj_1 = node.parent.obj_2
                    node.parent.obj_2 = None
                    node.parent.child_3.child_3 = node.child_1
                    node.child_1 = None
                    node.parent.child_3.sortChildren()
                    node.parent.child_2 = node.parent.child_3
                    node.parent.child_3 = None

                # If the empty node is the parent's third child:
                if node == node.parent.child_3:
                    node.parent.child_1.obj_2 = node.parent.obj_1
                    node.parent.obj_1 = node.parent.child_2.obj_1
                    node.parent.child_2.obj_1 = None
                    node.obj_1 = node.parent.obj_2
                    node.parent.obj_2 = None
                    node.parent.child_1.child_3 = node.parent.child_2.child_1
                    node.parent.child_1.sortChildren()
                    node.child_2 = node.parent.child_2.child_2
                    node.sortChildren()
                    node.parent.child_2.child_1 = None
                    node.parent.child_2.child_2 = None
                    node.parent.child_2 = node
                    node.parent.child_3 = None

            # Category 4: Both parent and sibling only have one object. This one requires recursion.

            # Both situations beneath work the same; they make a subtree with an empty root.
            if not node.parent.obj_2 and not situationFound:
                situationFound = True
                if node == node.parent.child_1:
                    node.parent.child_2.obj_2 = node.parent.child_2.obj_1
                    node.parent.child_2.obj_1 = node.parent.obj_1
                    node.parent.obj_1 = None
                    node.parent.child_2.child_3 = node.child_1
                    node.parent.child_2.sortChildren()
                    node.parent.child_1 = node.parent.child_2
                    parent = node.parent
                    parent.child_2 = None
                    node.parent = None
                    node.child_1 = None
                    # If the empty root was our original root, the problem is solved.
                    # If not, there's now an empty node in the tree. This can be fixed by recursively calling this function.
                    if not self.root == parent:
                        self.fixEmptyNode(parent)

            # Same goes for the second situation, where the empty node is its parent's second child.
                # Test for parent first, because we might just be deleting from root!
                if node.parent:
                    if node.parent.child_2:
                        if node == node.parent.child_2:
                            node.parent.child_1.obj_2 = node.parent.obj_1
                            node.parent.obj_1 = None
                            node.parent.child_1.child_3 = node.child_1
                            node.parent.child_1.sortChildren()
                            parent = node.parent
                            parent.child_2 = None
                            node.parent = None
                            node.child_1 = None
                            if not self.root == parent:
                                self.fixEmptyNode(parent)


        # If root is now empty, it automatically has only one child (We had a category 4 problem previous recursion call
        # and now the empty parent node is our root. This is no problem, we just need to delete this node and
        # make it's child our new root.
        if not self.root.obj_1:
            self.root.sortObj()
            if not self.root.obj_1:
                self.root.sortChildren()
                self.root = self.root.child_1

        # If there was a fix made, situationFound = True. Otherwise, it's still False.
        return situationFound

    # Everything under this line is an interface function. Everything above this line is a helper function

    def insert(self, object):
        """
        This function is used to add objects to the tree.
        :param object: the object to be added
        """
        node = self.root

        # If the node has no children, no need to descend in the tree. Call the .merge function for merging with a
        # new node (/subtree) containing object
        if not node.hasChildren():
            node.merge(ttTree.node(None, object))

        # If the node does have children, first descend to the node where we would expect our object.
        else:
            node_to_insert_into = self.go_to_leaf(node, object)
            node_to_insert_into.merge(ttTree.node(None, object))

    def delete(self, key):
        """
        This function is used to delete objects from our tree
        :param key: The search key for our to-delete-object
        :return: boolean statement wether the node was deleted or not
        """

        # Find the node to delete from
        node = self.descendToNode(key)

        # If this node exists
        if node:
            if node.hasChildren():
                # If the node has children (i.e. if the object is not in a leaf), swap the object with its inorder
                # successor
                node = self.swapWithInorderSuccessor(key)

            # From here on, the object is always in a leaf.
            # Delete the object and sort the node it was in
            node.obj_1 = None
            node.sortObj()

            # If the node still has an object, the node is not empty and no problems have occurred
            if node.obj_1:
                return True
            else:
                # If it didn't, the node is now empty. This needs to be fixed using .fixEmptyNode(node)
                return self.fixEmptyNode(node)

        # If the node did not exist, return false and print an error.
        else:
            print("Value not found during deletion of ", key)
            return False

    def getItem(self, key):
        """
        This function returns the object with the given key value
        :param key: key value
        :return: object matching the corresponding key value
        """

        # If the tree is empty, don't even bother looking for the item
        if self.empty():
            print("Could not get item: Tree empty")
            return False

        # Descend to the node that should contain the item
        node = self.descendToNode(key)
        # If the given key matches one of the node's object's keys, temporarily store that object
        if key == node.obj_1.key:
            item = node.obj_1
        if node.obj_2:
            if key == node.obj_2.key:
                item = node.obj_2

        # If item was filled with an object, return the item. Otherwise return False: The object wasn't found.
        if item:
            return item
        else:
            return False

    def getList(self):
        """
        This function returns the entire tree in a sorted list, using the function .inOrderTraverse()
        :return: list containing all objects
        """

        list = []
        # Check if the tree isn't empty (would get errors otherwise)
        if not self.empty():
            # If it wasn't empty, return the list returned by the function .inOrderTraverse()
            return self.inOrderTraverse(self.root, list)
        else:
            # If the tree was empty, return the empty list
            return list

    def getSize(self):
        """
        This function counts all objects using the function .inOrderTraverseCount()
        :return: integer containing the amount of objects
        """

        # First check if tree isn't empty
        if not self.empty():
            # If it isn't empty, return the value given by .inOrderTraverseCount()
            return self.inOrderTraverseCount(self.root)
        else:
            # If it is empty, return 0
            return 0

    def empty(self):
        """
        This function returns a boolean statement containing wether the tree is empty or not. It actually checks wether
        the place .obj_1 in self.root exists, and if it's occupied. If it's neither, it returns True (-> empty).
        :return:
        """
        if self.root:
            return not self.root.obj_1
        else:
            return True
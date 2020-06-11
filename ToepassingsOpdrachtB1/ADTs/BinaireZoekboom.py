class object:
    def __init__(self, key, restvalue):
        self.restvalue = restvalue
        self.key = key

class binarySearchTree:

    class node:
        def __init__(self, object=None, parent=None, leftchild=None, rightchild=None):
            self.object = object
            self.parent = parent
            self.leftchild = leftchild
            self.rightchild = rightchild

    def __init__(self):
        self.root = binarySearchTree.node()

    def descend_to_node(self, value, node=None):
        """
        This recursive function returns a node containing a given value, or false if value is not found
        :param value: given value to find the node for
        :param node: current node looking into
        :return: node (if value found) or false
        """
        # If the node isn't specified, we're starting, and we start at root
        if not node:
            node = self.root

        # If node's value corresponds to given key, return the node
        if node.object.key == value:
            return node

        # Else: compare and recursively call the corresponding child. If the corresponding child does not exist,
        # value is not present in tree, so return False.
        if value > node.object.key:
            if node.rightchild:
                return self.descend_to_node(value, node.rightchild)
            else:
                return False
        elif value < node.object.key:
            if node.leftchild:
                return self.descend_to_node(value, node.leftchild)
            else:
                return False

    def get_inorder_successor_from_right_part_tree(self, node):
        """
        This function recursively returns the node containing the inorder successor from the right subtree of given
        node. This function's first call is already in the right sub-tree!
        :param node: Current node
        :return: node containing the successor
        """

        # If the node has no children: This is a leaf, we can return this node
        if not node.leftchild:
            return node

        # If it's not a leaf, go left as much as possible...
        if node.leftchild:
            return self.get_inorder_successor_from_right_part_tree(node.leftchild)

    def make_dot(self, filename):
        """
        This function creates a .dot file for the tree.
        :param filename: Output file name for .dot file
        :return: if tree empty, return false
        """
        if self.empty():
            print("Could not make .dot: Tree empty")
            return False
        # Create an empty string for content
        content = ""
        node = self.root

        # If the root has no children, just print the root. No need for recursive functions.
        if not self.root.leftchild and not self.root.rightchild:
            content += "\"" + str(self.root.object.key) + "\";"

        # In case root exists (which it nearly always does), call recursive function draw_children to fill content
        if self.root:
            content = self.draw_children(node, content)

        # Create the file using string content
        with open(filename, "w") as fout:
            fout.write("digraph \"Tree\" {")
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

        # If the node has a left child..
        if node.leftchild:
            # Print key of node.object, followed by an arrow, followed by the key of leftchild.object, followed by a nl.
            content += "\"" + str(node.object.key) + "\" -> \"" + str(node.leftchild.object.key) + "\";"
            content += "\n"
            # If this node has children, call recursively
            if node.leftchild.leftchild or node.leftchild.rightchild:
                content = self.draw_children(node.leftchild, content, )

        # Right child works the same
        if node.rightchild:
            content += "\"" + str(node.object.key) + "\" -> \"" + str(node.rightchild.object.key) + "\";"
            content += "\n"
            if node.rightchild.leftchild or node.rightchild.rightchild:
                content = self.draw_children(node.rightchild, content, )
        return content

    def inOrderTraverse(self, node, list):
        """
        This function recursively passes through the tree, and prints the node values inorder. Is callee for the
        .getList() function. In first call, this is the root of the tree.
        :param node: Node currently at while traversing
        :param list: list that keeps track of all values already passed
        :return: list, now containing values from current node.
        """

        # If node has leftchild, call recursively
        if node.leftchild:
            list = self.inOrderTraverse(node.leftchild, list)

        # Append key value of current node object
        list.append(node.object.restvalue)

        # If node has rightchild, call recursively
        if node.rightchild:
            list = self.inOrderTraverse(node.rightchild, list)
        return list

    def delete_node(self, node):
        """
        This function is called during .delete(). It distinguishes 4 categories, of which the last one requires
        a recursive call
        :param node: Node to be deleted
        """

        # if node is loose LEAF, just delete the node and tell its parent its child is gone
        if not node.rightchild and not node.leftchild:
            if node == node.parent.rightchild:
                node.parent.rightchild = None
            if node == node.parent.leftchild:
                node.parent.leftchild = None
        # if node has ONE CHILD, being left: just delete the node and tell its parent is node's left child
        if not node.rightchild and node.leftchild:
            if node == node.parent.rightchild:
                node.parent.rightchild = node.leftchild
            if node == node.parent.leftchild:
                node.parent.leftchild = node.leftchild
        # if node has ONE CHILD, being right: just delete the node and tell its parent is node's right child
        if node.rightchild and not node.leftchild:
            if node == node.parent.rightchild:
                node.parent.rightchild = node.rightchild
            if node == node.parent.leftchild:
                node.parent.leftchild = node.rightchild
        # if node has TWO CHILDREN: swap node with the one containing the inorder successor, then solve the problem from
        # there by trying to delete that node (which is a recursive call)
        if node.rightchild and node.leftchild:
            swapnode = self.get_inorder_successor_from_right_part_tree(node.rightchild)
            temp = node.object
            node.object = swapnode.object
            swapnode.object = temp
            self.delete_node(swapnode)

    # Everything under this line is an interface function. Everything above this line is a helper function

    def insert(self, object, node=None):
        """
        This recursive function inserts objects into the tree, sorted by .key
        :param object: object to insert
        :param node: node currently descended to
        :return: return if inserting was successful
        """
        # If there's no node specified because it's the first call, begin from Root.
        if not node:
            node = self.root
        # If current node is empty, insert into this node (base case for recursion)
        if not node.object:
            node.object = object
        else:
            # If current node already holds said value, return False and throw error (base case for recursion)
            if object.key == node.object.key:
                print("Value", object.key, "already in tree")
                return False
            # Determine to branch left or right, then if node doesn't exists, make a new one store object there
            # If it does exist, recursively call on that node
            if object.key > node.object.key:
                if not node.rightchild:
                    node.rightchild = binarySearchTree.node(object, node)
                else:
                    binarySearchTree.insert(self, object, node.rightchild)
            if object.key < node.object.key:
                if not node.leftchild:
                    node.leftchild = binarySearchTree.node(object, node)
                else:
                    binarySearchTree.insert(self, object, node.leftchild)
        return True

    def delete(self, value):
        """
        This function deletes an object from the tree, by given value
        :param value: value which corresponding object needs to be deleted
        :return: bool if delete was successful
        """
        # Return false if tree was empty
        if self.empty():
            return False

        # Find the node containing the value
        node = self.descend_to_node(value)
        # If that node is 'False', value wasn't found. Give error and return False.
        if not node:
            print("Value", value, "not found.")
            return False
        else:
            # If it wasn't False, call on helper function delete_node
            self.delete_node(node)

    def getSize(self):
        """
        Calls on .inOrderTraverse(), and counts the elements in the given list.
        :return: integer with amount of elements in tree
        """
        list = self.getList()
        return len(list)

    def empty(self):
        """
        return the boolean statement, which is true if size == 0, and false in all other cases
        :return: boolean if empty or not
        """
        return self.getSize() == 0

    def getItem(self, value):
        """
        This function returns the object corresponding to a given value
        :param value: value to find the object for
        :return: the object (if found), or False (if not found)
        """
        # If the tree contains no items, return false
        if self.empty():
            return False

        # If the returned node is False, it wasn't found and an error should be given and False returned
        node = self.descend_to_node(value)
        if node:
            return node.object
        else:
            print("Value", value, "not found.")
            return False

    def getList(self):
        """
        This function calls on .inOrderTraverse() to make a list of all values.
        :return: list
        """
        node = self.root
        list = []
        return self.inOrderTraverse(node, list)

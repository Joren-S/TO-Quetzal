''' 
Python file for the implementation of the Red-Black Tree for TO GA&S.

Author:     Joren Servotte

'''


#
#       Helper Classes
#           -> You can interpret these classes as the python version of enums.
#


class Color:
    ''' 
    Class for the colors of the Red-Black Tree.
    Black = 0, Red = 1
    '''
    Black, Red = range(2)

class RotateType:
    '''
    Class for the rotation types.
    Left = 0, Right = 1
    '''
    Left, Right = range(2)



#
#       Main Classes
#


class RBT_Node:
    '''
    Class for a node of the Red-Black Tree.
    When initialized, creates a node by itself (no parent/children) with the 'color' property being set to Color.Red.
    Has 1 mandatory argument: the value being stored in the node.
    '''
    def __init__(self, zoeksleutel, waarde, color = Color.Red):
        self.zoeksleutel = zoeksleutel
        self.value = waarde
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.color = color

class RBT:
    '''
    Class for the Red-Black Tree.
    When initialized, creates an empty tree.
    '''

    def __init__(self):
        self.size = 0
        self.root = None

    def insert(self, zoeksleutel, waarde):
        '''
        Insert a value/node in the Red-Black tree.
        Zoeksleutel can not be None. 
        Will return a boolean if it succeeded or not.
        '''
        # We have to create an RBT_Node object first.
        value = RBT_Node(zoeksleutel, waarde)
        if (value is None):
            return False
        else:            
            # First off, we insert just like we would in a binary searchtree.
            # We traverse the Red-Black tree until we find where we have to insert our node, starting from the root.
            parentNode = None
            curNode = self.root
            while (curNode is not None):
                parentNode = curNode
                if (value.zoeksleutel < curNode.zoeksleutel):
                    curNode = curNode.leftChild
                else:
                    curNode = curNode.rightChild

            # Once done, we set the parent to the found node and set our node as the correct child in the parent.
            # If no node was found it means the tree is empty, so the node we have to insert becomes the root.
            value.parent = parentNode
            if (parentNode is not None):
                if (value.zoeksleutel > parentNode.zoeksleutel):
                    parentNode.rightChild = value
                else:
                    parentNode.leftChild = value
            else:
                self.root = value

            # At the start, the color of our inserted node is red.
            value.color = Color.Red

            # As long as the value node isn't the root of the Red-Black Tree and the parent of the value node isn't red.
            while ((value != self.root) and (value.parent.color != Color.Black)):

                # Store if the parent of value is the right child of its parent.
                parentIsRChild = (value.parent == value.parent.parent.rightChild)
                # Store the sibling
                sibling = (value.parent.parent.leftChild if parentIsRChild else value.parent.parent.rightChild)

                # If there is no sibling or the sibling is black
                if ((sibling is None) or (sibling.color == Color.Black)):
                    if (parentIsRChild == True):
                        # If parent is right child -> change value and rotate right
                        if (value == value.parent.leftChild):
                            value = value.parent
                            self.rotate(value, RotateType.Right)
                        
                    else:
                        # If parent is left child -> change value and rotate left
                        if (value == value.parent.rightChild):
                            value = value.parent
                            self.rotate(value, RotateType.Left)

                    # Switch the colors so the parent is black and the parent's parent is red.
                    # Next, rotate left if the parent was the right child or rotate right if it was the left child.
                    value.parent.color = Color.Black
                    value.parent.parent.color = Color.Red
                    rType = RotateType.Left if parentIsRChild else RotateType.Right
                    self.rotate(value.parent.parent, rType)

                else:
                    # Recolor
                    sibling.color = Color.Black
                    value.parent.color = Color.Black
                    value.parent.parent.color = Color.Red
                    value = value.parent.parent

            # We set the color of the root to black.
            self.root.color = Color.Black

            # And finally, we increment the size by 1, this makes it so we can create an easy getSize function.
            self.size = self.size + 1
            return True
        return False

    def delete(self, value):
        '''
        Delete a value/node from the Red-Black tree.
        Value can either be ItemType (whatever the tree is storing: ints, floats, objects, lists, ...) or an existing RBT_Node object.
        Returns True if deletion was succesful.
        '''
        # If the value to delete is not an RBT_Node, we have to search for the value in the tree first.
        if (type(value) is not RBT_Node):
            # If the value was found, it can be deleted
            # If not, return False (deletion failed since value is not in tree).
            searchInfo = self.search(value)
            if (searchInfo[1] == True):
                return self.delete(searchInfo[0])
            else:
                return False

        else:
            # If the node that needs to be deleted has a child -> tmpNode = inorder successor of node that needs to be deleted.
            # If not, tmpNode = node that needs to be deleted
            tmpNode = value if ((value.leftChild is None) or (value.rightChild is None)) else self.findInorderSuccessor(value)

            # If tmpNode has a left child -> nodeChild = left child of tmpNode
            # If not, nodeChild = right child of tmpNode
            nodeChild = tmpNode.rightChild if (not tmpNode.leftChild) else tmpNode.leftChild

            if (nodeChild is not None):
                nodeChild.parent = tmpNode.parent

            # If tmpNode has a parent, we are going to check if tmpNode is the left or right child and set nodeChild to the approriate field so it replaces tmpNode as the child of tmpNode's parent.
            if (tmpNode.parent is not None):
                if (tmpNode == tmpNode.parent.rightChild):
                    # tmpNode is right child of his parent -> nodeChild becomes new right child
                    tmpNode.parent.rightChild = nodeChild
                else:
                    # tmpNode is left child of his parent -> nodeChild becomes new left child
                    tmpNode.parent.leftChild = nodeChild
            else:
                # The parent of tmpNode doesn't exist -> tmpChild (which is the root) is replaced by nodeChild, which becomes the new root.
                self.root = nodeChild

            # If there are no children, we don't need to move over the value inside.
            if (value != tmpNode):
                value.value = tmpNode.value
                
            # If tmpNode is black, we have to check the tree for violations and make sure the colors are correct.
            # If nodeChild is None, it means a leaf was deleted and there aren't any violations.
            if ((tmpNode.color == Color.Black) and (nodeChild is not None)):

                # Keep going as long as nodeChild is black and isn't the root.
                while ((nodeChild.color == Color.Black) and (nodeChild != self.root)):

                    # Store if nodeChild is the left child of his parent in isLeftChild
                    isLeftChild = (nodeChild == nodeChild.parent.leftChild)

                    # Store the sibling of nodeChild in sibling
                    sibling = nodeChild.parent.rightChild if (isLeftChild) else nodeChild.parent.leftChild

                    # If the sibling of nodeChild isn't black
                    if (sibling.color != Color.Black):

                        # We first turn nodeChild's parent red before turning nodeChild's sibling black.
                        nodeChild.parent.color = Color.Red
                        sibling.color = Color.Black

                        # We rotate left if nodeChild is the left child and right if it's the right child.
                        # Afterwards, we reset nodeChild to the correct child.
                        if (isLeftChild):
                            self.rotate(nodeChild.parent, RotateType.Left)
                        else:
                            self.rotate(nodeChild.parent, RotateType.Right)
                        sibling = nodeChild.parent.rightChild if (isLeftChild) else nodeChild.parent.leftChild

                    # If both the children of nodeChild's sibling are black, sibling becomes red and we repeat the entire process for nodechild's parent.
                    if (sibling.leftChild.color == Color.Black) and (sibling.rightChild.color == Color.Black):
                        sibling.color = Color.Red
                        nodeChild = nodeChild.parent
                    else:
                        if (isLeftChild):
                            # If nodeChild is the left child, we check if the sibling's right child is not red.
                            # If so, the sibling's left child also becomes black but the sibling itself becomes red.
                            # We rotate right around sibling
                            if (sibling.rightChild.color != Color.Red):
                                sibling.color = Color.Red
                                sibling.leftChild.color = Color.Black
                                self.rotate(sibling, RotateType.Right)
                                sibling = nodeChild.parent.rightChild
                            # sibling inherits nodeChild's parent' color while said parent becomes black.
                            # We make sure the right child becomes black and finally, we rotate left around nodeChild's parent.
                            sibling.color = nodeChild.parent.color
                            sibling.rightChild.color = Color.Black
                            nodeChild.parent.color = Color.Black
                            self.rotate(nodeChild.parent, RotateType.Left)
                        else:
                            # Analog to above, but reversed. (left -> right and right -> left)
                            # If nodeChild is the right child, we check if the sibling's left child is not red.
                            # If so, the sibling's right child also becomes black but the sibling itself becomes red.
                            # We rotate right around sibling
                            if (sibling.leftChild.color != Color.Red):
                                sibling.color = Color.Red
                                sibling.rightChild.color = Color.Black
                                self.rotate(sibling, RotateType.Right)
                                sibling = nodeChild.parent.leftChild
                            # sibling inherits nodeChild's parent' color while said parent becomes black.
                            # We make sure the right child becomes black and finally, we rotate left around nodeChild's parent.
                            sibling.color = nodeChild.parent.color
                            sibling.leftChild.color = Color.Black
                            nodeChild.parent.color = Color.Black
                            self.rotate(nodeChild.parent, RotateType.Right)
                        nodeChild = self.root

                nodeChild.color = Color.Black

            # We decerement the size field by 1 so our getSize function returns the correct result.
            self.size = self.size - 1
            return True

    def search(self, searchkey):
        '''
        Look for the node with a specific value in the tree.
        Returns the node (if found, otherwise returns a None object) and a boolean (wether the search was succesful) in the form (node, boolean).
        '''
        # Search is the same as a search in a binary searchtree:
        # If the condition in the while statement is not met, the searchkey is not in the tree.
        cur_node = self.root
        while (cur_node is not None):

            # First, we check if the current node is the node we're looking for.
            if (cur_node.zoeksleutel == searchkey):
                return (cur_node, True)

            # If not, we check if the searchkey we are looking for is bigger than the searchkey in the current node.
            # If so, we go to the right child/subtree and repeat the process.
            elif (cur_node.zoeksleutel < searchkey):
                cur_node = cur_node.rightChild

            # If not, the searchkey must be smaller than the searchkey in the current node.
            # So we go to the left child/subtree and repeat the process.
            else:
                cur_node = cur_node.leftChild
        return (None, False)
    
    def getSize(self):
        '''
        The amount of nodes/values in the tree.
        '''
        return self.size

    def isEmpty(self):
        '''
        Check if the Red-Black tree is empty by checking if the root exists.
        '''
        return (self.root is None)

    def inorderTraverse(self):
        '''
        Inorder traversal of the Red-Black tree, stores the values in a list and returns this list.
        Returns a None object if the tree is empty.
        '''
        # If tree is empty, return None
        if (self.isEmpty()):
            return None

        # Find the left-most node in the tree (= smallest value), starting from the root.
        values = []
        cur_node = self.root
        while (cur_node.leftChild is not None):
            cur_node = cur_node.leftChild

        # We add the value of the node to our list, then look for the inorder successor.
        # We repeat this process until we can no longer find an inorder successor (= end of inorder traversal, all nodes checked).
        while (cur_node is not None):
            values.append(cur_node.value)
            cur_node = self.findInorderSuccessor(cur_node)

        # Finally, we return the list of values
        return values






    #
    #   Dependencies
    #       -> The following functions are functions used by the main functions (above) and aren't intended to be used seperately (although they can).
    #       -> These aren't in the original contract for the Red-Black Tree.
    #
    
    def findInorderSuccessor(self, node):
        ''' 
        Looks for the inorder successor of the provided node and returns this node if it exists. 
        '''
        # Find the left-most node in the right subtree.
        if (node.rightChild is not None):
            tmp = node.rightChild
            while (tmp.leftChild is not None):
                tmp = tmp.leftChild
            return tmp

        # Traverse the tree towards the root and check each node.
        # If a node is NOT the right child of its parent -> the parent is the inorder successor.
        # Because if a node is the left child, that means all the nodes we checked have a value LESS than the value of the parent of said node.
        cur_node = node
        cur_parent = node.parent
        while (cur_parent is not None):
            if (cur_parent.rightChild != cur_node):
                break
            cur_node = cur_parent
            cur_parent = cur_parent.parent
        return cur_parent

    def rotate(self, pivot, rtype):
        '''
        Function to rotate around a pivot. 
        Type can either be RotateType.Left or RotateType.Right
        Returns True if rotation succeeded
        '''

        # If we want to rotate left and the right child of the pivot node exists
        if ((rtype == RotateType.Left) and (pivot.rightChild is not None)):
            
            # We store the right child of the pivot in tmpNode.
            # Afterwards, we set the parent field of the tmpNode to the parent of the pivot (can also be non-existant).
            # Next, the left child of the right child of the pivot (which is currently also in tmpNode) moves up and replaces its father (the right child of the pivot).            
            tmpNode = pivot.rightChild
            tmpNode.parent = pivot.parent
            pivot.rightChild = pivot.rightChild.leftChild

            # If this node we just moved up (this is the node which replaced its father) exists, we set its parent field to the pivot.
            # After this, we made the connection between this node and its parent.
            if (tmpNode.leftChild is not None):
                tmpNode.leftChild.parent = pivot

            # Afterwards, we check if the parent of the pivot exists.
            # If it exists, we check if the pivot is a right child or a left child of its parent and store tmpNode in the correct child field.
            if (pivot.parent is not None):                
                if (pivot == pivot.parent.rightChild):
                    # pivot is a right child -> store tmpNode in the rightChild field
                    pivot.parent.rightChild = tmpNode
                else:
                    # pivot is a left child -> store tmpNode in the leftChild field
                    pivot.parent.leftChild = tmpNode
            # If it doesn't exist, we store tmpNode in the root.
            else:                
                self.root = tmpNode

            # We finish up by making the connection between tmpNode and pivot.
            tmpNode.leftChild = pivot
            pivot.parent = tmpNode
            return True

        # If we want to rotate right and the left child of the pivot node exists
        elif ((rtype == RotateType.Right) and (pivot.leftChild is not None)):

            # We store the left child of the pivot in tmpNode.
            # Afterwards, we set the parent field of the tmpNode to the parent of the pivot (can also be non-existant).
            # Next, the right child of the left child of the pivot (which is currently also in tmpNode) moves up and replaces its father (the left child of the pivot).            
            tmpNode = pivot.leftChild
            tmpNode.parent = pivot.parent
            pivot.leftChild = pivot.leftChild.rightChild
            
            # If this node we just moved up (this is the node which replaced its father) exists, we set its parent field to the pivot.
            # After this, we made the connection between this node and its parent.
            if (tmpNode.rightChild is not None):
                tmpNode.rightChild.parent = pivot

            # Afterwards, we check if the parent of the pivot exists.
            # If it exists, we check if the pivot is a right child or a left child of its parent and store tmpNode in the correct child field.
            if (pivot.parent is not None):                
                if (pivot == pivot.parent.rightChild):
                    # pivot is a right child -> store tmpNode in the rightChild field
                    pivot.parent.rightChild = tmpNode
                else:
                     # pivot is a left child -> store tmpNode in the leftChild field
                    pivot.parent.leftChild = tmpNode
            # If it doesn't exist, we store tmpNode in the root.
            else:                
                self.root = tmpNode

            # We finish up by making the connection between tmpNode and pivot.
            tmpNode.rightChild = pivot
            pivot.parent = tmpNode
            return True
        return False
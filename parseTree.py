import copy

class parseTree:
    """
    A class to represent an expression tree

    Attributes
    ----------
    node : str
        the value of the node
    left : Union[parseTree, None]
        the left child
    right: Union[parseTree, None]
        the right child

    Methods
    -------
    display(indent="")
        prints the parseTree that shows the structure of the tree
    """
    def __init__(self, node=None, left=None, right=None):
        self.node = node
        self.left = left
        self.right = right

    def display(self, indent=""):
        if self.node is not None:
            print(indent + self.node)
        if self.left is not None:
            self.left.display(indent + "   ")
        if self.right is not None:
            self.right.display(indent + "   ")
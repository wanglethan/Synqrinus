from parseTree import *

# Dictionary that contains acceptable operators and their precedence in an equation
# Operators with greater values have higher precedence
operators = {'+': 0, '-': 0, '*': 1, '/': 1}

def get_symbols(formula, acc_list=None, acc_str=None):
    """
    Converts a string in the standard spreadsheet formula form into a list
    of parentheses, operators, cells and numbers in the same order they appear.
    Ignores whitespace and uses a functional approach

    Parameters
    ----------
    formula : str
        The formula that is to be converted

    acc_list : list
        The accumulated list of symbols so far

    acc_str : str
        The accumulated cell/number that is being processed

    Returns
    -------
    list
        a list of strings that contain the parentheses, operators,
        cells and numbers from formula
    """

    # To avoid mutable default errors
    if acc_list is None:
        acc_list = []
    if acc_str is None:
        acc_str = ""

    # Base case is when formula is an empty string
    if len(formula) == 0:
        # Adds the accumulated string to acc_list if there is any
        if len(acc_str) != 0:
            acc_list.append(acc_str)
        # Return acc_list as the final result
        return acc_list

    # Otherwise there are characters left in formula
    else:
        # Set char equal to the first character in formula
        char = formula[0]

        # If the character is a parenthesis
        if char in operators or char in ['(', ')']:
            # Adds the accumulated string to acc_list if there is any
            if len(acc_str) != 0:
                acc_list.append(acc_str)
            # Append the parenthesis to acc_list
            acc_list.append(char)
            # Call get_symbols recrusively on the rest of formula and reset acc_str to empty
            return get_symbols(formula[1:], acc_list, "")

        # If the character is whitespace or an equal sign (the beginning of a formula)
        elif char == ' ' or char == '=':
            # Adds the accumulated string to acc_list if there is any
            if len(acc_str) != 0:
                acc_list.append(acc_str)
            # Call get_symbols recrusively on the rest of formula and reset acc_str to empty
            # ignoring char since it was either whitespace or the initial equals sign
            return get_symbols(formula[1:], acc_list, "")

        # If the character is not whitespace (cell or number) or '='
        else:
            # Call get_symbols recursively on the rest of formula
            # and concatenate char onto acc_str
            return get_symbols(formula[1:], acc_list, acc_str + char)


def parse_formula(formula):
    """
    Parses the mathematical expression formula into a binary tree of operators and values

    Parameters
    ----------
    formula : str
        The formula that is to be parsed into a tree

    Returns
    -------
    parseTree
        The formula represented as a parseTree
    """

    # Convert the formula string into a list of symbols (parentheses, operators, numbers, cells)
    symbols = get_symbols(formula)

    # If formula contains only one symbol, then it must be a cell / number
    if len(symbols) == 1:
        return parseTree(node=symbols[0])

    # Otherwise Formula contains at least two cells / numbers
    # tree is an intially 'empty' parseTree that will be the constructed into the final tree
    # tree comes in the form
    #       None
    #       /  \
    #     None None
    #     /  \
    #  None  None
    tree = parseTree(left=parseTree())

    # stack is the stack of nodes (parseTrees) that is currently being traversed,
    # starting from the root of tree, but excluding the current node
    stack = [tree]

    # current_tree stores the current node that is being dealt with
    current_tree = tree.left

    # iterates through each symbol (parenthesis, operator, cell, or number) and constructs tree
    for symbol in symbols:

        # If the symbol is an opening parenthesis, then make the left child
        # into a parseTree (new independent expression) and traverse into it
        if symbol == '(':
            # Push the current tree to stack
            stack.append(current_tree)
            # Make the left child into a parseTree
            current_tree.left = parseTree()
            # Traverse into the left child
            current_tree = current_tree.left

        # If the symbol is a closing parenthesis, then backtrack out of the
        # current tree (expression) and into to the previous tree in stack
        elif symbol == ')':
            # Pop the topmost tree from stack and set current_tree equal to it
            current_tree = stack.pop()

        # If the symbol is an operator, then check if this tree's node already
        # has an operator
        elif symbol in operators:
            # If current_tree's node has not been changed yet (None), then set it
            # equal to symbol, and then make the right child into a parseTree
            # and traverse into it
            if current_tree.node == None:
                # Set node of current_tree equal to the operator
                current_tree.node = symbol
                # Push the current tree to stack
                stack.append(current_tree)
                # Make the right child into a parseTree
                current_tree.right = parseTree()
                # Traverse into the right child
                current_tree = current_tree.right

            # If there is already an operator, then we must check whether or not it has
            # a higher precedence than symbol in order to deal with order of operations
            else:
                # If the existing operator has higher or equal precedence, then "squeeze"
                # symbol right above current_tree, making symbol its parent
                if operators[current_tree.node] >= operators[symbol]:
                    # Copy current_tree down into its own left child and set its node
                    # equal to symbol
                    current_tree.left = copy.deepcopy(current_tree)
                    current_tree.node = symbol
                    # Push the current tree to stack
                    stack.append(current_tree)
                    # Make the right child into a parseTree
                    current_tree.right = parseTree()
                    # Traverse into the right child
                    current_tree = current_tree.right

                # If symbol has higher precedence, then replace the right child with symbol
                # and push the original right child down into the left child of symbol
                else:
                    # Make the right child of current_tree into a new parseTree by moving it down
                    # into the left child of the new tree and symbol as the node
                    current_tree.right = parseTree(node=symbol, left=current_tree.right)
                    # Push the current tree to stack
                    stack.append(current_tree)
                    # Traverse into the right child
                    current_tree = current_tree.right
                    # Push the new current tree to stack
                    stack.append(current_tree)
                    # Make the right child into a parseTree
                    current_tree.right = parseTree()
                    # Traverse into the right child once again
                    current_tree = current_tree.right

        # Otherwise, the symbol must be a cell or a number
        else:
            # Set node of current_tree equal to the cell/number
            current_tree.node = symbol
            # Pop the topmost tree from stack and set current_tree equal to it
            current_tree = stack.pop()

        # ******************************************************************************
        # UNCOMMENT THE FOLLOWING BLOCK OF CODE TO SEE THE TREE BEING BUILT AT EACH STEP
        # ******************************************************************************
        # tree.display()
        # print("-----------------------")

    # Return tree as the final result
    return tree


def parse_file():
    """
    Reads the file 'formulas.txt' and prints each formula
    along with its parse tree

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    # Open the text file as read only
    file = open("formulas.txt", "r")

    # Iterate through each line in the file
    for formula in file:
        # Create a new tree based on the formula
        tree = parse_formula(formula.rstrip())
        # Formatting
        print("Formula: {}".format(formula.rstrip()))
        print("Tree:")
        tree.display()
        print("-----------------------------")

# ******************************************************************************
#                                TESTING AREA
# ******************************************************************************
# Uncomment/Comment the following line to read formulas from 'formulas.txt'
# and print their trees:

parse_file()

# Or optionally print trees for individual formulas here:
# An preformatted example is given below:

# formula1 = "= A1 + 2 * (B2 - 3)/C1"
# tree1 = parse_formula(formula1)
# print("Formula: {}".format(formula1))
# print("Tree:")
# tree1.display()






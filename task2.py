from task1 import *

def find_dependencies(formula):
    """
    Returns a list of cell ID dependencies for a given formula

    Parameters
    ----------
    formula : str
        The formula that will be checked

    Returns
    -------
    list
        a list of Cell IDs that appear in formula
    """

    # The corresponding parseTree for formula
    tree = parse_formula(formula)

    # List of dependencies for the given formula
    dependencies = []

    # Next is a simple BFS alogrithm to traverse tree
    queue = [tree]

    # Loop until queue becomes empty
    while queue:

        # Get the first tree in queue and pop it from the queue
        current_tree = queue.pop(0)
        # The value of the node of the first tree in queue
        symbol = current_tree.node

        # Check if the first character in symbol is a letter to see if it is a cell
        if symbol[0].isalpha():
            # Add symbol to dependencies if it is not already in there
            if symbol not in dependencies:
                dependencies.append(symbol)

        # Add the left child to the queue if it is not None
        if current_tree.left is not None:
            queue.append(current_tree.left)

        # Add the right child to the queue if it is not None
        if current_tree.right is not None:
            queue.append(current_tree.right)

    # Return dependencies for the final result
    return dependencies

def circular_ref(cell, dataset):
    """
    Returns true if the given cell has a dependency within its dataset and false otherwise

    Parameters
    ----------
    cell : str
        The cell that will be checked for circular dependencies

    dataset : (dict of str : str)
        A dictionary with cell IDs as keys and their numerical values or formulas as values

    Returns
    -------
    bool
        True if the cell has a circular dependency in dataset
    """

    # This function traverses through all links in dependencies by a BFS algorithm
    # Queue for the order of cells to visit
    queue = find_dependencies(dataset[cell])
    # List contains all cells that have been visited already
    visited = []

    # Loop until queue becomes empty
    while queue:
        # Get the first cell in queue and pop it from the queue
        current_cell = queue.pop(0)

        # If current_cell equals the original cell, then there is a circular dependency
        if current_cell == cell:
            return True

        # Otherwise add current_cell to visited
        visited.append(current_cell)
        # Iterate through the dependencies of current_cell
        for dependency in find_dependencies(dataset[current_cell]):
            # Check if the dependency has been visited
            if dependency not in visited:
                # Push dependency into the queue
                queue.append(dependency)

    # If the loop completed, then there were no circular dependencies so return false
    return False

def circular(formula, dataset):
    """
    Returns true if the given formula has any dependencies that are involved in a circular
    dependency in the given dataset of references. Returns false otherwise.

    Parameters
    ----------
    formula : str
        The formula that will be checked

    dataset : (dict of str : str)
        A dictionary with cell IDs as keys and their numerical values or formulas as values

    Returns
    -------
    bool
        True if formula has circular dependencies based on dataset
    """

    # Dependencies of formula
    formula_deps = find_dependencies(formula)

    # Iterate through each cell in dependencies
    for cell in formula_deps:
        # If cell has a circular dependency in dataset, then return true
        if circular_ref(cell, dataset):
            return True

    # If the loop completed, then there were no circular dependencies so return false
    return False

# ******************************************************************************
#                                TESTING AREA
# ******************************************************************************
# Dataset examples:
dataset1 = {"A1": "=A2*2", "A2": "=B3", "A3": "2", "B1": "4", "B2": "3", "B3": "=A1+B2"}
dataset2 = {"A1": "3", "A2": "=A1+B1", "A3": "1", "B1": "B3", "B2": "2", "B3": "3"}
dataset3 = {"A1": "=A2/(A2*B1)", "A2": "=A3+B2", "A3": "3", "B1": "A2*B2", "B2": "B3", "B3": "1"}

# Directly test the function "circular" below:
# Uncomment / Comment the following lines:

# formula1 = "=A1+52*2/(B2+B3)"
# print(circular(formula1, dataset1))
# print(circular(formula1, dataset2))
# print(circular(formula1, dataset3))
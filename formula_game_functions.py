"""
# Copyright Tanaan Karunakaran, Nick Cheng, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment

# Add your functions here.


def build_tree(formula):
    '''
    (string) -> formula_tree
    This function takes a string and puts it
    into a proper formula tree. If the string
    is not in the correct format, then return
    None.

    >>> build_tree('-x')
    NotTree(Leaf('x'))
    >>> build_tree('((-x+y)*-(-y+x))')
    AndTree(OrTree(NotTree(Leaf('x')), Leaf('y')), \
    NotTree(OrTree(NotTree(Leaf('y')), Leaf('x'))))
    >>> x = build_tree('Pancer Square')
    >>> x == None
    True
    '''
    # find length of formula
    length = len(formula)

    # base case, if only one character
    if (length == 1):
        # return a leaf
        return Leaf(formula)
    # if a not symbol occurs
    if (formula[0] == "-"):
        # create NotTree and continue building
        return NotTree(build_tree(formula[1:]))

    # this means that the root will either be
    # a AndTree or OrTree
    if (formula[0] == '('):

        # create counters and initialize variables
        counter = 0
        root = ''
        # to use in while loop
        x = 0
        # this loop finds the root
        while x < len(formula) and root == '':

            # subtract 1 if rigth bracket is found
            if formula[x] == ")":
                counter = counter - 1

            # if a not symbol is used
            if formula[x] == '-':
                x = x + 1
            # add 1 if left bracket is found
            if formula[x] == "(":
                counter = counter + 1

            # if the counter reaches 1
            elif counter == 1:
                root = formula[x+1]
            x = x + 1

        # if root is a +
        if root == '+':
            return OrTree(build_tree(formula[1:x]),
                          build_tree(formula[x+1:-1]))

        # if the root is a *
        if root == '*':
            return AndTree(build_tree(formula[1:x]),
                           build_tree(formula[x+1:-1]))

    # in case of incorrect format
    if formula[0].isalpha() is False:
        return None


def draw_formula_tree(root):
    '''
    (FormulaTree) -> str
    This function takes a formula tree and returns
    the formula tree drawn out.
    REQ: root be in correct format
    >>> draw_formula_tree(Leaf('x'))
    'x'
    >>> draw_formula_tree(AndTree(Leaf('y'), \
    OrTree(NotTree(Leaf('z')), NotTree(Leaf('x')))))
    * + - x
        - z
      y
    '''
    # call helper function
    result = draw_formula_tree_help(root)
    # remove blank line at the end
    result = result[:-1]
    # return result
    return result


def draw_formula_tree_help(root, counter=0):
    '''
    (FormulaTree, int) -> str
    Take a formula tree and print it out
    in correct format. When returned, it will have a
    blank line at the end.
    REQ: root be in correct format
    >>> draw_formula_tree(AndTree(OrTree(NotTree\
    (Leaf('x')), Leaf('y')), NotTree(OrTree(NotTree\
    (Leaf('y')), Leaf('x')))))
    * - + x\
        - y
      + y
        - x

    >>> draw_formula_tree(Leaf('x'))
    'x'

    >>> draw_formula_tree(AndTree(Leaf('y'), \
    OrTree(NotTree(Leaf('z')), NotTree(Leaf('x')))))
    * + - x
        - z
      y

    '''
    # initialize string value
    word = ''

    # if Leaf occurs
    if type(root) == Leaf:
        return root.symbol + '\n'

    # if a NotTree occurs
    if type(root) == NotTree:
        return root.symbol + ' ' + \
               draw_formula_tree_help(root.children[0], counter + 2)

    # at this point it is either a OrTree or AndTree
    else:
        # start drawing the right side of the tree first
        word += root.symbol + ' ' + \
            draw_formula_tree_help(root.children[1], counter + 2)
        # add space to make it correct format
        word += '  '
        # based on recursion, add spaces
        for x in range(counter):
            word += " "
        # draw left side of formula tree
        word += draw_formula_tree_help(root.children[0], counter + 2)
        # return result
        return word


def evaluate(root, variables, values):

    '''
    (FormulaTree, str, str) -> int
    This function takes a FormulaTree, a string of variables
    and a string of truth values, and determines wether the
    final result of the FormulaTree is true or false.
    Return 1 for True, 0 for False
    REQ: root be in correct format
    REQ: letters in variables must exist in root
    REQ: values must be 0 or 1
    >>> root = AndTree(Leaf('y'), OrTree(NotTree(Leaf('z')), \
    NotTree(Leaf('x'))))
    >>> evaluate(root, 'yzx', '001')
    0
    '''
    # Base Case: If there is only a leaf
    if isinstance(root, Leaf):
        # find position of symbol in the variable
        variable_position = variables.find(root.symbol)
        # return the value, based on the variable_position

        return int(values[variable_position])
    # if a Not symbol occurs
    if isinstance(root, NotTree):
        result = evaluate(root.children[0], variables, values)
        # since this is NotTree, return oposite result
        if str(result) == '0':
            return 1
        else:
            return 0

    # At this point, we know that the root is a AndTree or OrTree.
    # Evaluate both sides of the tree
    left_side = str(evaluate(root.children[0], variables, values))
    right_side = str(evaluate(root.children[1], variables, values))

    result = left_side + right_side

    # check if it is an OrTree
    if isinstance(root, OrTree):
        # Return 1 if a '1' exists in the string, else return 0
        if ('1' in result):
            return 1
        else:
            return 0

    # if it is an AndTree
    if isinstance(root, AndTree):
        # check if result == '11' (meaning both sides are true.
        # If not, return 0
        if (result == '11'):
            return 1

        else:
            return 0


def play2win(root, turns, variables, values):
    '''
    (root, str, str, str) -> int
    This function takes a root, string of turns,
    variables and values and returns an int value
    (0 or 1) to indicate the best move
    REQ: root must be correct format
    REQ: turns can only consist of A and E
    REQ: the chars in variables must exist in
    the Leaf of the root
    REQ: len(values) <= len(turns)
    REQ: values can only consist of 1 and 0
    >>> root = build_tree('(y*(-z+-x))')
    >>> play2win(root, "AEA", 'xyz', '10')
    1
    '''
    # find the letter of which player's turn
    player = turns[len(values)]
    # creata variables
    # if true were to be pased
    With_True = None
    # if false were to be passed
    With_False = None

    # if it is the final move (Base Case)
    if ((len(turns) - len(values)) <= 1):
        # check if a true will win
        With_True = evaluate(root, variables, values + '1')
        # if player was A
        # return false is obtained, then return 1
        # otherwise return 0
        # for player a
        if player == 'A':
            # if false is obtained from a 1
            if With_True == 0:
                return 1
            # otherwise return 0
            else:
                return 0

        # for player E
        else:
            # if true is obtained from 1
            if With_True == 1:
                return 1
            # otherwise return 0
            else:
                return 0

    # need to recurse
    else:
        # check with both possibilities with true or false
        With_True = play2win(root, turns, variables, values + '1')
        With_False = play2win(root, turns, variables, values + '0')

        # for player a
        if player == 'A':
            # if false is obtained from 1
            if With_True == 0:
                return 1
            # if false is obtained from 0
            elif With_False == 0:
                return 0
            # if result does not matter
            else:
                return 0

        # for player E
        else:
            # if true is obtained from a 1
            if With_True == 1:
                return 1

            # if true is obtained from a 0
            if With_False == 1:
                return 0
            # if result does not matter
            else:
                return 1

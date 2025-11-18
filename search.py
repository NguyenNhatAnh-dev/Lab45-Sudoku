"""
In search.py, you will implement Backtracking and AC3 searching algorithms
for solving Sudoku problem which is called by sudoku.py
"""

from csp import *
from copy import deepcopy
import util
from util import digits, rows, cols, squares 


def Backtracking_Search(csp):
    """
    Backtracking search initialize the initial assignment
    and calls the recursive backtrack function
    """
    assignment = {}
    for var in csp.variables:
        if len(csp.values[var]) == 1:
            assignment[var] = csp.values[var]
            
    csp.values = deepcopy(csp.values)

    return Recursive_Backtracking(assignment, csp)


def Recursive_Backtracking(assignment, csp):
    """
    The recursive function which assigns value using backtracking
    """
    
    if len(assignment) == len(csp.variables):
        return assignment

    try:
        var = Select_Unassigned_Variables(assignment, csp)
    except ValueError:
        return None 
    except:
        return assignment 

    for value in Order_Domain_Values(var, assignment, csp):
        
        if isConsistent(var, value, assignment, csp):
            
            state_backup = deepcopy(csp.values)

            assignment[var] = value

            inferences = {} 
            inference_status = Inference(assignment, inferences, csp, var, value)
            
            if inference_status is not False: 

                result = Recursive_Backtracking(assignment, csp)
                
                if result is not None:
                    return result

            del assignment[var]
    
            csp.values = state_backup
            
    return None


def Inference(assignment, inferences, csp, var, value):
    """
    Forward checking (FC) implementation.
    Prunes 'value' from the domains of all unassigned peers of 'var'.
    Includes recursive propagation if a domain shrinks to size 1.
    
    Returns False if a domain becomes empty (FAILURE), True otherwise (SUCCESS).
    """
    
    for neighbor in csp.peers[var]:
        if neighbor not in assignment and value in csp.values[neighbor]:

            if len(csp.values[neighbor]) == 1 and csp.values[neighbor] == value:
                return False

            remaining = csp.values[neighbor].replace(value, "")
            csp.values[neighbor] = remaining

            if len(remaining) == 0:
                return False

            if len(remaining) == 1:
                flag = Inference(assignment, inferences, csp, neighbor, remaining[0])
                if flag is False:
                    return False

    return True

def Order_Domain_Values(var, assignment, csp):
    """
    Returns string of values of given variable (simple ordering).
    """
    return csp.values[var]

def Select_Unassigned_Variables(assignment, csp):
    """
    Selects new variable to be assigned using minimum remaining value (MRV).
    """
    unassigned_variables = {}
    
    for var in csp.variables:
        if var not in assignment:
            unassigned_variables[var] = len(csp.values[var])
    
    if not unassigned_variables:
        raise ValueError("No unassigned variables found, but assignment is incomplete.")

    mrv = min(unassigned_variables, key=unassigned_variables.get)
    return mrv

def isConsistent(var, value, assignment, csp):
    """
    Check if assignment is consistent (i.e., 'value' does not conflict 
    with any assigned peers of 'var').
    """
    for neighbor in csp.peers[var]:
        if neighbor in assignment.keys() and assignment[neighbor] == value:
            return False
    return True


def display(values):
    """
    Display the solved sudoku on screen
    """
    for row in rows:
        if row in 'DG':
            print("-------------------------------------------")
        for col in cols:
            if col in '47':
                print(' | ', values[row + col], ' ', end=' ')
            else:
                print(values[row + col], ' ', end=' ')
        print(end='\n')

def write(values):
    """
    Write the string output of solved sudoku to file
    """
    output = ""
    for variable in squares:
        output = output + values[variable] 
    return output


def AC3(csp):
    """
    AC-3 algorithm: enforce arc consistency.
    """
    queue = list(csp.constraints)  

    while queue:
        Xi, Xj = queue.pop(0)

        if REVISE(csp, Xi, Xj):
            if len(csp.values[Xi]) == 0:
                return False
            for Xk in csp.peers[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    return True


def REVISE(csp, Xi, Xj):
    """
    Make Xi arc-consistent with Xj.
    Remove any value x in domain(Xi) that has no possible support in domain(Xj).
    Constraint: Xi != Xj  (Sudoku rule)
    """
    revised = False
    domain_Xi = csp.values[Xi]

    for x in domain_Xi[:]:  
        has_support = any(y != x for y in csp.values[Xj])

        if not has_support:
            csp.values[Xi] = csp.values[Xi].replace(x, '')
            revised = True

    return revised
# CLASS DESCRIPTION FOR CONSTRAINT SATISFACTION PROBLEM (CSP)

from util import *

class csp:

    # INITIALIZING THE CSP
    def __init__(self, domain=digits, grid=""):
        """
        Initializes the CSP model for Sudoku.
        """
        
        rows = 'ABCDEFGHI'
        cols = '123456789'
        
        def cross(A, B):
            return [a + b for a in A for b in B]

        self.variables = cross(rows, cols) 

        row_units = [cross(r, cols) for r in rows]
        col_units = [cross(rows, c) for c in cols]
        square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
        
        self.unitlist = row_units + col_units + square_units 

        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.variables)

        self.peers = dict((s, set(sum(self.units[s], [])) - {s}) for s in self.variables)
        

        self.values = self.getDict(grid)
        
        self.constraints = []
        for v1 in self.variables:
            for v2 in self.peers[v1]:
                self.constraints.append((v1, v2))


    def getDict(self, grid=""):
        """
        Getting the string as input and returning the corresponding dictionary
        """
        i = 0
        values = dict()
        for cell in self.variables:
            if grid[i] != '0':
                values[cell] = grid[i]
            else:
                values[cell] = digits
            i = i + 1
        return values
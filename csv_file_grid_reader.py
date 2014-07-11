"""
Class for reading in a grid file, a comma-separated text file representing an
NxN grid.   
"""

class CsvFileGridReader(object):    
    SEPARATOR = ','
    ERROR_BAD_GRID = "File must be a file of comma-separated text representing an NxN grid."


    def __init__(self, filename):
        """
        @param filename: The name of a text file representing an NxN grid.
                         A file with N rows must have in each row exactly N
                         values separated by N-1 commas.
        """
        self.filename = filename


    def read(self):
        """
        Converts a comma-separated text file representing an NxN grid into a list
        of lists, with grid[i][j] representing the square at the ith row and jth
        column in the file (where indices start at 0).
        
        @return: A list of lists representing an NxN grid.
        """
        # Convert CSV file into a list, each element containing a row of the file
        f = open(self.filename, 'r')
        grid = f.read().splitlines()
    
        # If file is empty or nothing was read in, raise an exception
        if not grid:
            raise Exception(CsvFileGridReader.ERROR_BAD_GRID)
    
        # Convert each comma-separated row of the file into a list in the grid.
        for row in xrange(len(grid)):
            grid[row] = grid[row].split(CsvFileGridReader.SEPARATOR)
            # Ensure that each row has the right number of columns
            if len(grid[row]) != len(grid):
                raise Exception(CsvFileGridReader.ERROR_BAD_GRID)
        return grid

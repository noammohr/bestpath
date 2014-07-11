import sys
from csv_file_grid_reader import CsvFileGridReader

# Allowed characters in the grid
START = 'A'
END = 'B'
BLOCK = 'X'
EMPTY = '0'

# Sucessful output string
OUTPUT_TEMPLATE = "The robot visited {0} squares moving from A to B inclusive.\n" \
                  "The robot did not visit {1} unblocked squares.\n" \
                  "The robot visited each square this many times: \n" \
                  "{2}\n"

# Error messages
ERROR_IMPOSSIBLE = "It is impossible to reach B from A."
ERROR_NO_START = "There is no start {!r}.".format(START)
ERROR_NO_END = "There is no destination {!r}.".format(END)
ERROR_TOO_MANY_STARTS = "Found more than one start {!r}.".format(START)
ERROR_TOO_MANY_ENDS = "Found more than one start {!r}.".format(END)
ERROR_INVALID_CHARACTER = "Found {0}. Only {1}, {2}, {3}, and {4} are permitted.".\
                                format('{!r}', START, END, BLOCK, EMPTY)


def find_path(filename, output=sys.stdout):
    """
    Given a comma-separated text file representing an NxN grid with a start
    square labeled A, a destination square labeled B, blocked squares labeled
    X, and empty squares labeled 0, finds the shortest path from A to B that
    includes no diagonals and prints out three relevant pieces of information:
        (1) The number of squares along the path (including A and B).
        (2) The number of squares not visited along the path (excluding
            blocked squares).
        (3) The NxN grid with each square showing the number of times it was
            visited.
    
    @param filename: A text file representing an NxN grid. A file with N rows
                     must have in each row exactly N characters that are each
                     either A, B, X, or 0, each separated from the next by N-1
                     commas. The file must contain exactly one A and one B.
    @param output: Default output is to stdout, but this can be changed for
                   tests.
    @return: None
    """
    try:
        # Read the file into a list of lists, and validate the format of the input.
        grid = CsvFileGridReader(filename).read()

        # Extract key features from the grid (A, B, and how many X's), and validate
        # the content of the input.
        start, end, num_blocks = _get_features(grid)

        # Crawl through the grid from the start, searching for the destination,
        # leaving a trail in empty squares of the grid
        end_found = _find_path_to_destination(grid, start)

        if end_found:
            # Note that the robot path includes the start position of the robot.
            robot_path, num_visited = _get_robot_path(grid, start, end)

            # Print output.
            num_squares = len(grid) ** 2
            num_unvisited = num_squares - num_blocks - num_visited
            printable_robot_path = '\n'.join([','.join(row) for row in robot_path])
            output.write(OUTPUT_TEMPLATE.format(num_visited, num_unvisited,
                                                printable_robot_path))
        else:
            raise Exception(ERROR_IMPOSSIBLE)
    except Exception as e:
        output.write(str(e) + '\n')
    

def _get_features(grid):
    """
    Takes an NxN grid and returns three features from that grid:
        (1) The start sqare (2) end sqare, and (3) number of blocked squares

    @param grid: A list of lists representing an NxN grid, including exactly
                 one square with the constant START, exactly one with END,
                 and all other square either EMPTY or BLOCK. Anything else
                 raises an Exception.
    @return: a tuple representing the indices of the START position in the
             grid, a tuple representing the indices of the END position in the
             grid, and an integer representing the number of BLOCK positions.
    """
    # Initialize return values
    start = None
    end = None
    num_blocks = 0

    # Check each square in the grid for relevant features
    for row in xrange(len(grid)):
        for col in xrange(len(grid)):
            square = grid[row][col]
            # Count the number of BLOCK squares
            if square == BLOCK:
                num_blocks += 1
            # Store the START position, and make sure there's only one
            elif square == START:
                if not start:
                    start = (row, col)
                else:
                    raise Exception(ERROR_TOO_MANY_STARTS)
            # Store the END position, and make sure there's only one
            elif square == END:
                if not end:
                    end = (row, col)
                else:
                    raise Exception(ERROR_TOO_MANY_ENDS)
            # Make sure there are no invalid values in the grid
            elif square != EMPTY:
                raise Exception(ERROR_INVALID_CHARACTER.format(square))

    # Make sure a START and END square were found
    if not start:
        raise Exception(ERROR_NO_START)
    elif not end:
        raise Exception(ERROR_NO_END)

    return start, end, num_blocks


def _find_path_to_destination(grid, start):
    """
    Searches the grid, starting at the start square and crawling in all
    directions except where there are BLOCK squares, until the destination
    square is found. Each empty square checked is overwritten with a tuple
    (row, column) of the position of the adjacent square from which that square
    was reached, so that the path back can be calculated.

    @param grid: A list of lists representing an NxN grid.
    @param start: A tuple with the row number and column number (index starting
                  at 0) of the start position from which to search for a path
                  to the destination position that contains the constant END.
    @return: Boolean of whether a path to the destination square was found.
    """
    # Initialize the return value
    end_found = False
    # The list of tuples representing the row and column position of squares
    # currently just checked for whether they are the destination.
    new_current = [start]

    # Search for the END square, until found or there's nothing left to check.
    while new_current and not end_found:
        # The new list of just-checked squares becomes our current list on each
        # successive step of our crawl.
        current = new_current
        new_current = []
        for square in current:
            # For each square checked, check the adjacent unchecked unblocked squares.
            end_found, next_current = _next_steps(grid, square)
            # If we find the desintination, we're done.
            if end_found:
                break
            # Add the positions of these adjacent squares to our list of adjacent squares.
            new_current += next_current

    return end_found


def _next_steps(grid, square):
    """
    Look for a destination square in all squares adjacent to the input square.
    Overwrite any unblocked adjacent squares with the position of the input
    square, unless already overwritten. This serves as a track of the path
    that led to the new square.
    
    @param grid: A list of lists representing an NxN grid.
    @param square: A tuple with the row number and column number (index
                   starting at 0) of position from which to check adjecent
                   squares for the square containing the constant END.
    @return: A tuple, the first element a boolean on whether the destination
             was found, and the second element a list of tuples representing
             the rows and column numbers of the adjacent 
    """
    def step(next_row, next_col):
        """
        Checks the square in the grid with the given row/column position for
        the destination string. If unblocked and not previously checked,
        overwrites it with a tuple representing the row and column of the
        square from which the robot would step into this square. 
        
        @param next_row: Index of the row of the square to check.
        @param next_col: Index of the column of the square to check.
        @return: Boolean of whether the checked square is the destination.
        """
        if grid[next_row][next_col] == END:
            grid[next_row][next_col] = square
            return True
        elif grid[next_row][next_col] == EMPTY:
            grid[next_row][next_col] = square
            new_squares.append((next_row, next_col))
        return False

    end_found = False
    # n is the highest row or column number in the grid.
    n = len(grid) - 1
    row, col = square
    # The list of adjacent unblocked unchecked squares that we've checked in
    # this call of the function.
    new_squares = []
    # Check to the right.
    if row < n:
        end_found = step(row + 1, col)
    # Check to the left.
    if not end_found and row > 0:
        end_found = step(row - 1, col)
    # Check to the bottom.
    if not end_found and col < n:
        end_found = step(row, col + 1)
    # Check to the top.
    if not end_found and col > 0:
        end_found = step(row, col - 1)
    return end_found, new_squares


def _get_robot_path(grid, start, end):
    """
    Takes the processed grid and returns a list of tuples, each representing
    successive positions in the grid for the robot to step into in order to
    travel from start to end.
    
    @param grid: NxN grid with tuples in each square along the
                 robot's path representing the row and column
                 indices of the square from which the robot
                 should step into it as it travels.
    @param start: A tuple with the row number and column number (index starting
                  at 0) of the start sqaure in the grid from which to the
                  robot will begin.
    @param end: A tuple with the row number and column number (index starting
                at 0) of the destination sqaure in the grid where the robot
                will end up.
    @return: path - A list of lists representing the NxN grid, each element
                    containing a string value of the number of times that
                    square had been visited by the robot (the start square
                    included), and
             pathlength - the number of squares visited by the robot. 
    """
    # Initialize out path map to contain all zeroes.
    path = [['0'] * len(grid) for row in xrange(len(grid))]

    # Include the start square as a visited square.
    row, col = start
    path[row][col] = '1'
    pathlength = 1

    # Each location has the previous location stored therein.
    # Find the robot's path starting at the destination and working back.
    square = end
    while square != start:
        row, col = square
        path[row][col] = '1'
        pathlength += 1
        square = grid[row][col]
    
    return path, pathlength

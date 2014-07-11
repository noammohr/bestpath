"""
Suite of tests of robot.py's find_path() method.
"""
from __future__ import print_function
from StringIO import StringIO
from csv_file_grid_reader import CsvFileGridReader
import robot


def test_grid_zero_blocks(output=StringIO()):
    # A 5x5 empty grid with no blocks.
    output = StringIO()
    robot.find_path("testgrids/grid_zero_blocks.txt", output=output)
    assert robot.OUTPUT_TEMPLATE.format(6, 19, '').strip() in output.getvalue()


def test_grid_one_block(output=StringIO()):
    # A 6x6 grid with one block.
    output = StringIO()
    robot.find_path("testgrids/grid_one_block.txt", output=output)
    assert robot.OUTPUT_TEMPLATE.format(5, 30, '').strip() in output.getvalue()


def test_grid_three_blocks(output=StringIO()):
    # A 7x7 grid with three blocks around the destination,
    # requiring a path around them.
    output = StringIO()
    robot.find_path("testgrids/grid_three_blocks.txt", output=output)
    assert robot.OUTPUT_TEMPLATE.format(10, 36, '').strip() in output.getvalue()


def test_grid_impossible_blocked_end(output=StringIO()):
    # An 8x8 grid with four blocks around the destination
    # closing off any path to it, and a corner start.
    output = StringIO()
    robot.find_path("testgrids/grid_impossible_blocked_end.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_IMPOSSIBLE


def test_grid_impossible_blocked_start(output=StringIO()):
    # An 8x8 grid with four blocks around the start
    # closing off any path from it, and a corner destination.
    output = StringIO()
    robot.find_path("testgrids/grid_impossible_blocked_start.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_IMPOSSIBLE


def test_grid_impossible_blocked_middle(output=StringIO()):
    # An 8x8 grid with a jagged set of blocks across the middle of the grid
    # closing off any path from start to destination.
    output = StringIO()
    robot.find_path("testgrids/grid_impossible_blocked_middle.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_IMPOSSIBLE


def test_grid_maze_with_loops(output=StringIO()):
    # A 9x9 grid with many blocks requiring most of the unblocked grid to be
    # traversed, and includes loops around a set of blocks that could keep a
    # robot going in circles, and a corner start.
    output = StringIO()
    robot.find_path("testgrids/grid_maze_with_loops.txt", output=output)
    assert robot.OUTPUT_TEMPLATE.format(37, 20, '').strip() in output.getvalue()


def test_grid_no_start(output=StringIO()):
    # A 5x5 grid with no blocks and no start position A, but an end position B.
    output = StringIO()
    robot.find_path("testgrids/grid_no_start.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_NO_START


def test_grid_no_end(output=StringIO()):
    # A 5x5 grid with no blocks and no end position B, but a start position A.
    output = StringIO()
    robot.find_path("testgrids/grid_no_end.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_NO_END


def test_grid_two_starts(output=StringIO()):
    # A 5x5 grid with no blocks and two start positions A.
    output = StringIO()
    robot.find_path("testgrids/grid_two_starts.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_TOO_MANY_STARTS


def test_grid_two_ends(output=StringIO()):
    # A 5x5 grid with no blocks and two end positions B.
    output = StringIO()
    robot.find_path("testgrids/grid_two_ends.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_TOO_MANY_ENDS


def test_grid_invalid_character(output=StringIO()):
    # A 5x5 grid with no blocks, an A, a B, and an invalid character C.
    output = StringIO()
    robot.find_path("testgrids/grid_invalid_character.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_INVALID_CHARACTER.format('C')


def test_grid_missing_character(output=StringIO()):
    # A 5x5 grid with no blocks, an A, a B, and a square with no character.
    output = StringIO()
    robot.find_path("testgrids/grid_missing_character.txt", output=output)
    assert output.getvalue().strip() == robot.ERROR_INVALID_CHARACTER.format('')


def test_grid_not_square_long(output=StringIO()):
    # A 4x5 grid.
    output = StringIO()
    robot.find_path("testgrids/grid_not_square_long.txt", output=output)
    assert output.getvalue().strip() == CsvFileGridReader.ERROR_BAD_GRID


def test_grid_not_square_tall(output=StringIO()):
    # A 5x4 grid.
    output = StringIO()
    robot.find_path("testgrids/grid_not_square_tall.txt", output=output)
    assert output.getvalue().strip() == CsvFileGridReader.ERROR_BAD_GRID


def test_grid_not_square_jagged(output=StringIO()):
    # A (nearly) 5x5 grid with one row of length 4.
    output = StringIO()
    robot.find_path("testgrids/grid_not_square_jagged.txt", output=output)
    assert output.getvalue().strip() == CsvFileGridReader.ERROR_BAD_GRID


def test_grid_empty(output=StringIO()):
    # A grid with no elements, that is, an empty file.
    output = StringIO()
    robot.find_path("testgrids/grid_empty.txt", output=output)
    assert output.getvalue().strip() == CsvFileGridReader.ERROR_BAD_GRID


def test_nonexistent_file(output=StringIO()):
    # A (nearly) 5x5 grid with one row of length 4.
    output = StringIO()
    robot.find_path("nonexistent_file.txt", output=output)
    assert "No such file or directory: 'nonexistent_file.txt'" in output.getvalue()


def test_all():
    TESTS = [test_grid_zero_blocks,
             test_grid_one_block,
             test_grid_three_blocks,
             test_grid_impossible_blocked_end,
             test_grid_impossible_blocked_start,
             test_grid_impossible_blocked_middle,
             test_grid_maze_with_loops,
             test_grid_no_start,
             test_grid_no_end,
             test_grid_two_starts,
             test_grid_two_ends,
             test_grid_invalid_character,
             test_grid_missing_character,
             test_grid_not_square_long,
             test_grid_not_square_tall,
             test_grid_not_square_jagged,
             test_grid_empty,
             test_nonexistent_file]
    failed_tests = 0
    for test in TESTS:
        print(test.__name__ + ':', end=" ")
        try:
            test()
            print("PASSED")
        except AssertionError:
            failed_tests += 1
            print("FAILED")
    if failed_tests:
        print(failed_tests, "tests failed.")
    else:
        print("---> ALL TESTS PASSED.")

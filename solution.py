assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        twins = [(s, t) for s in unit for t in unit if values[s] == values[t]]
        for twin in twins:
            twin_value = values[twin[0]]
            for box in unit:
                if box not in twin:
                    values[box] = ''.join([ch for ch in values[box] if ch not in twin_value])
    return values

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+d for s in A for d in B]

boxes = cross(rows, cols)
row_units = [cross(r,cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs)
                for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
first_diagnal = [rows[i]+cols[i] for i in range(9)]
second_diagnal = [rows[i]+cols[-1 * (i+1)] for i in range(9)]
diagnal_units = [first_diagnal, second_diagnal]
unitlist = row_units + col_units + square_units + diagnal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'.
            If the box has no value, then the value will be '123456789'.
    """
    sudoku_dict = {}
    for i in range(81):
        if grid[i] != '.':
            sudoku_dict[boxes[i]] = grid[i]
        else:
            sudoku_dict[boxes[i]] = '123456789'

    return sudoku_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values is False:
        print("This puzzle can't be solved")
        return
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        for peer in peers[box]:
            values[peer] = values[peer].replace(values[box], '')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dboxes = [box for box in unit if digit in values[box]]
            if len(dboxes) == 1:
                values[dboxes[0]] = digit
    return values

def reduce_puzzle(values):
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_boxes_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_boxes_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_boxes_before == solved_boxes_after
        if len([box for box in values.keys() if len(values[box]) == 0]) > 0:
            return False

    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values

    _, min_box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    for ch in values[min_box]:
        values_copy = values.copy()
        values_copy[min_box] = ch
        attempt = search(values)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    puzzle = grid_values(grid)
    return search(puzzle)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

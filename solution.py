assignments = []

# ---------------------------------------------
#  _______  _______  _______  ______    ______  
# |  _    ||       ||   _   ||    _ |  |      | 
# | |_|   ||   _   ||  |_|  ||   | ||  |  _    |
# |       ||  | |  ||       ||   |_||_ | | |   |
# |  _   | |  |_|  ||       ||    __  || |_|   |
# | |_|   ||       ||   _   ||   |  | ||       |
# |_______||_______||__| |__||___|  |_||______| 
#  _______  _______  _______  __   __  _______  
# |       ||       ||       ||  | |  ||       | 
# |  _____||    ___||_     _||  | |  ||    _  | 
# | |_____ |   |___   |   |  |  |_|  ||   |_| | 
# |_____  ||    ___|  |   |  |       ||    ___| 
#  _____| ||   |___   |   |  |       ||   |     
# |_______||_______|  |___|  |_______||___|     

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [left + right for left in A for right in B]

def zip_chars(A, B):
    "Zips together two iterators of characters as paired strings instead of tuples"
    zipped = []
    for l, r in zip(A, B):
        zipped.append(l + r)
    return zipped

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [
    list(zip_chars([r for r in rows], [c for c in cols])),
    list(zip_chars([r for r in rows], [c for c in cols][::-1]))
]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# -----------------------------------------------------
#  _______  __   __  ______   _______  ___   _  __   __ 
# |       ||  | |  ||      | |       ||   | | ||  | |  |
# |  _____||  | |  ||  _    ||   _   ||   |_| ||  | |  |
# | |_____ |  |_|  || | |   ||  | |  ||      _||  |_|  |
# |_____  ||       || |_|   ||  |_|  ||     |_ |       |
#  _____| ||       ||       ||       ||    _  ||       |
# |_______||_______||______| |_______||___| |_||_______|
#  ___      _______  _______  ___  _______              
# |   |    |       ||       ||   ||       |             
# |   |    |   _   ||    ___||   ||       |             
# |   |    |  | |  ||   | __ |   ||       |             
# |   |___ |  |_|  ||   ||  ||   ||      _|             
# |       ||       ||   |_| ||   ||     |_              
# |_______||_______||_______||___||_______|             

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
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
    twins = []

    for box in boxes:
        box_vals = values[box]
        # If a box has only two possible values...
        if len(box_vals) == 2:
            # ...check every peer for the exact same...
            for peer in peers[box]:
                if box_vals == values[peer]:
                    # ...those'll be the other twin!
                    twins.append((box, peer))

    for a, b in twins:
        # Shared peers will be the intersection of the two lists
        shared_peers = [p for p in peers[a] if p in peers[b]]
        vals_to_rm = values[a]
        for val in vals_to_rm:
            for peer in shared_peers:
                assign_value(values, peer, values[peer].replace(val, ''))

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    possible_values = '123456789'
    for c in grid:
        if c in possible_values:
            chars.append(c)
        if c == '.':
            chars.append(possible_values)

    # Sanity
    assert len(chars) == 81

    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)

    for r in rows:
        print(
            ''.join(
                values[r + c].center(width) + \
                ('l' if c in '36' else '')
                for c in cols
            )
        )
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
    Given a dictionary of values, apply the elimination algorithms
    to eliminate possible values from contention in boxes given
    the values of their peers.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values dict with contending values eliminated
    """
    solved_values = [box for box in values.keys() if len(values[box]) is 1]
    for box in solved_values:
        val = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(val, ''))
    return values

def only_choice(values):
    """
    Given a dictionary of values in a sudoku board, iterate through
    the units and their respective boxes to determine if any unit has only one box that could possible hold a given value. Then, for every such case, set that box to hold that value.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values dict with 'only choice' boxes set correctly
    """
    for unit in unitlist:
        for val in '123456789':
            locations = [box for box in unit if val in values[box]]
            if len(locations) is 1:
                assign_value(values, locations[0], val)
    return values

def reduce_puzzle(values):
    """
    Given a dict of possible values in a sudoku board, apply
    strategies iteratively through constraint propagation to
    reduce the board as much as is possible.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        the reduced values dict, or False if something goes wrong
    """
    stalled = False

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) is 1])

        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) is 1])

        stalled = solved_values_before == solved_values_after

        # If there is an impossible box, return False!
        if len([box for box in values.keys() if len(values[box]) is 0]):
            return False

    return values

def solve(grid):
    """
    Given a string representation of a sudoku grid, solve the puzzle
    and return a dict representing the solved state.
    Args:
        A string representation of a sudoku grid
    Returns:
        The solved, dict representaiton of a sudoku grid
    """
    values = grid_values(grid) # Convert to values dict

    solved = search(values) # Solve the puzzle!

    if not solved:
        raise Exception('Can\'t solve that one!')
    else:
        return solved

def search(values):
    """
    Given a dict of possible values in a sudoku board, reduce the
    puzzle with simple strategies, then apply depth-first-search
    to traverse through possible solutions and solve the puzzle,
    if possible.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        Either a dict representing the values in a solved sudoku board, or False if the board is unsolvable.
    """
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[s]) is 1 for s in boxes):
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

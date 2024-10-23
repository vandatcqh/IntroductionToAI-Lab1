import os

def read_input_file(input_file):
    with open(input_file, 'r') as file:
        # Read the first line to get the weights of the stones
        weights_line = file.readline().strip()
        weights = list(map(int, weights_line.split()))
        # Read the rest of the lines to get the grid
        grid = [list(line.rstrip('\n')) for line in file]
    return weights, grid

def read_output_file(output_file):
    with open(output_file, 'r') as file:
        lines = file.readlines()
        if len(lines) < 2:
            print("Error: Output file does not contain enough information.")
            return None
        # The solution is on the second line
        solution = lines[1].strip()
    return solution

def parse_grid(grid, weights):
    stones = {}
    switches = set()
    walls = set()
    player_pos = None
    stone_index = 0

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                player_pos = (i, j)
            elif cell == '$':
                if stone_index < len(weights):
                    stones[(i, j)] = weights[stone_index]
                    stone_index += 1
                else:
                    print("Error: Not enough weights provided for all stones.")
                    return None
            elif cell == '.':
                switches.add((i, j))
            elif cell == '#':
                walls.add((i, j))
            # Handle cells that are both a switch and a stone
            elif cell == '*':
                if stone_index < len(weights):
                    stones[(i, j)] = weights[stone_index]
                    stone_index += 1
                else:
                    print("Error: Not enough weights provided for all stones.")
                    return None
                switches.add((i, j))

    if stone_index != len(weights):
        print("Error: Number of stones does not match number of weights.")
        return None

    return {
        'player_pos': player_pos,
        'stones': stones,
        'switches': switches,
        'walls': walls
    }

def simulate_solution(state, solution):
    player_pos = state['player_pos']
    stones = state['stones'].copy()
    walls = state['walls']
    switches = state['switches']
    total_sum_weight = 0  # Sum of weights of stones pushed

    # Define movement directions
    move_offsets = {
        'u': (-1, 0),
        'd': (1, 0),
        'l': (0, -1),
        'r': (0, 1),
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    for idx, move in enumerate(solution):
        if move not in move_offsets:
            print(f"Error: Invalid move '{move}' in solution at step {idx + 1}.")
            return False, total_sum_weight
        dx, dy = move_offsets[move]
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        new_pos = (new_x, new_y)

        if new_pos in walls:
            print(f"Error: Player walks into a wall at position {new_pos} at step {idx + 1}.")
            return False, total_sum_weight

        if new_pos in stones:
            # There is a stone in the new position
            stone_weight = stones[new_pos]
            next_x = new_x + dx
            next_y = new_y + dy
            next_pos = (next_x, next_y)

            if next_pos in walls or next_pos in stones:
                print(f"Error: Cannot push stone from {new_pos} to {next_pos} at step {idx + 1}.")
                return False, total_sum_weight

            if move.islower():
                print(f"Error: Attempted to push stone with lowercase move '{move}' at position {new_pos} at step {idx + 1}.")
                return False, total_sum_weight

            # Move the stone
            stones[next_pos] = stones.pop(new_pos)
            total_sum_weight += stone_weight

        else:
            if move.isupper():
                print(f"Error: Attempted to push with uppercase move '{move}' but no stone at position {new_pos} at step {idx + 1}.")
                return False, total_sum_weight

        # Move the player
        player_pos = new_pos

    # After applying all moves, check if all stones are on switches
    if set(stones.keys()) == switches:
        return True, total_sum_weight
    else:
        print("Error: Not all stones are on switches at the end of the solution.")
        return False, total_sum_weight

def main():
    # Directories
    input_dir = 'input'
    output_dir = os.path.join('output', 'UCS')

    for i in range(1, 2):  # For files 01 to 10
        input_file = os.path.join(input_dir, f'input-{i:02d}.txt')
        output_file = os.path.join(output_dir, f'output-{i:02d}.txt')


        # Check if files exist
        if not os.path.isfile(input_file):
            print(f"Error: Input file {input_file} does not exist.")
            continue
        if not os.path.isfile(output_file):
            print(f"Error: Output file {output_file} does not exist.")
            continue

        # Read the input and output files
        weights, grid = read_input_file(input_file)
        solution = read_output_file(output_file)

        if solution is None:
            print("Error reading solution from output file.")
            continue

        # Parse the grid to get initial state
        state = parse_grid(grid, weights)
        if state is None:
            print("Error parsing the grid.")
            continue

        is_valid, total_sum_weight = simulate_solution(state, solution)
        if is_valid:
            print(f"The solution in output-{i} is TRUE.")
        else:
            print(f"The solution in output-{i} is FALSE.")

if __name__ == "__main__":
    main()

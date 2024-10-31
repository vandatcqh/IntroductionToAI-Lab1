import os
import time
from collections import deque
import tracemalloc  

# Read input 
def read_input(input_file):
    with open(input_file, 'r') as file:
        weights_line = file.readline().strip()
        weights = list(map(int, weights_line.split()))
        grid = [list(line.rstrip('\n')) for line in file]
    return weights, grid

# Write output 
def write_output(output_file, algorithm, steps, total_weight, nodes, elapsed_time, memory, solution):
    with open(output_file, 'w') as file:
        file.write(f"{algorithm}\n")
        file.write(f"Steps: {steps}, Weight: {total_weight}, Node: {nodes}, Time (ms): {elapsed_time:.2f}, Memory (MB): {memory:.2f}\n")
        file.write(solution + "\n")

# Parse the grid to get the initial state 
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
            elif cell == '.':
                switches.add((i, j))
            elif cell == '#':
                walls.add((i, j))
            elif cell == '*':
                if stone_index < len(weights):
                    stones[(i, j)] = weights[stone_index]
                    stone_index += 1
                switches.add((i, j))

    return {
        'player_pos': player_pos,
        'stones': stones,
        'switches': switches,
        'walls': walls
    }

def bfs(initial_state):
    # Create a queue with the initial state, an empty path, and a total weight of 0
    queue = deque([(initial_state, "", 0)])  
    # Create a set to track visited states to avoid revisiting them
    visited = set()
    visited.add((initial_state['player_pos'], frozenset(initial_state['stones'].items())))

    # Movement offsets for player movement
    move_offsets = {
        'u': (-1, 0),  # Up
        'd': (1, 0),   # Down
        'l': (0, -1),  # Left
        'r': (0, 1)    # Right
    }
    
    # Movement offsets for pushing stones
    push_offsets = {
        'U': (-1, 0),  
        'D': (1, 0),   
        'L': (0, -1),  
        'R': (0, 1)    
    }
    
    nodes = 0

    while queue:
        current_state, path, total_weight = queue.popleft()
        player_pos = current_state['player_pos']
        stones = current_state['stones']

        # Check if all stones are on switches
        if set(stones.keys()) == current_state['switches']:
            return path, total_weight, nodes 

        # Explore all possible player moves
        for move, (dx, dy) in move_offsets.items():
            new_pos = (player_pos[0] + dx, player_pos[1] + dy)  
            # Check if the new position is valid 
            if new_pos not in current_state['walls'] and new_pos not in stones:
                new_state = {
                    'player_pos': new_pos,
                    'stones': stones.copy(), 
                    'switches': current_state['switches'],
                    'walls': current_state['walls']
                }
                state_key = (new_state['player_pos'], frozenset(new_state['stones'].items()))
                # If this state has not been visited before, add it to queue
                if state_key not in visited:
                    visited.add(state_key) 
                    queue.append((new_state, path + move, total_weight))
                    nodes += 1  

        # Explore all possible stone pushes
        for push, (dx, dy) in push_offsets.items():
            stone_pos = (player_pos[0] + dx, player_pos[1] + dy)  
            next_pos = (stone_pos[0] + dx, stone_pos[1] + dy)  
            
            # Check if the stone can be pushed 
            if stone_pos in stones and next_pos not in current_state['walls'] and next_pos not in stones:
                new_stones = stones.copy() 
                stone_weight = new_stones.pop(stone_pos) 
                new_stones[next_pos] = stone_weight  
                # Create a new state after pushing the stone
                new_state = {
                    'player_pos': stone_pos, 
                    'stones': new_stones,
                    'switches': current_state['switches'],
                    'walls': current_state['walls']
                }
                state_key = (new_state['player_pos'], frozenset(new_state['stones'].items()))
                # If this state has not been visited before, add it to the queue
                if state_key not in visited:
                    visited.add(state_key) 
                    queue.append((new_state, path + push, total_weight + stone_weight))  
                    nodes += 1 

    return None, None, nodes  # No solution is found

def measure_memory():
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    return peak_memory / (1024 * 1024)  

def main():
    input_directory = 'input'  
    output_directory = 'output/BFS'  
    os.makedirs(output_directory, exist_ok=True)  

    for i in range(1, 11): 
        input_file = os.path.join(input_directory, f'input-{i:02d}.txt')  
        output_file = os.path.join(output_directory, f'output-{i:02d}.txt')  

        weights, grid = read_input(input_file)
        initial_state = parse_grid(grid, weights)

        tracemalloc.start()  # Start tracking memory allocations
        start_time = time.time()
        solution, total_weight, nodes = bfs(initial_state)
        end_time = time.time()
        memory_usage_mb = measure_memory()  
        tracemalloc.stop()  # Stop tracking memory allocations

        if solution is not None:
            elapsed_time = (end_time - start_time) * 1000  
            write_output(output_file, "BFS", len(solution), total_weight, nodes, elapsed_time, memory_usage_mb, solution)
        else:
            print(f"No solution found for {input_file}.")

if __name__ == "__main__":
    main()

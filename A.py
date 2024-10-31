import psutil
import time
from dataclasses import dataclass
from typing import List, Tuple
from queue import PriorityQueue
import sys
import os

def print_memory_usage() -> float:
    """Get current process memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

@dataclass
class State:
    x: int
    y: int
    stones: List[Tuple[int, int, int]]  # List of tuples (x, y, weight)
    g: int
    f: int

    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        return self.g < other.g

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.x == other.x and 
                self.y == other.y and 
                sorted(self.stones) == sorted(other.stones))

    def __hash__(self):
        return hash((self.x, self.y, 
                    tuple(sorted(self.stones))))

def is_valid(x: int, y: int, grid: List[str]) -> bool:
    return not (x < 0 or y < 0 or x >= len(grid) or 
                y >= len(grid[0]) or grid[x][y] == '#')

def get_heuristic(state: State, switches: List[Tuple[int, int]]) -> int:
    """Calculate heuristic as sum of minimal weighted distances from stones to switches."""
    total = 0
    for stone in state.stones:
        min_dist = min(abs(stone[0] - sx) + abs(stone[1] - sy) for sx, sy in switches)
        total += min_dist * stone[2]
    return total

def is_goal(state: State, switches: List[Tuple[int, int]]) -> bool:
    stone_positions = {(stone[0], stone[1]) for stone in state.stones}
    return stone_positions == set(switches)

def read_input(filename):
    """Read and parse input file"""
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Read the first line containing numbers
    first_line = lines[0].strip()
    numbers = [int(x) for x in first_line.split()]
    
    # Read the grid lines
    grid = [line.rstrip('\n') for line in lines[1:] if line.strip()]
    
    return numbers, grid

def search(filename, id):
    # Read input from file
    numbers, grid = read_input(filename)

    start_time = time.time()
    node = 0

    # Create output directory and filename
    output_dir = os.path.join('output', 'A')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filename = os.path.join(output_dir, f'output-{id:02d}.txt')

    # Initialize starting state
    Ax = Ay = -1
    switches = []
    start_stones = []
    pos = 0

    # Process grid to find object positions
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell = grid[i][j]
            if cell == '@':
                Ax, Ay = i, j
            elif cell == '$':
                if pos < len(numbers):
                    weight = numbers[pos]
                    start_stones.append((i, j, weight))
                    pos += 1
            elif cell == '.':
                switches.append((i, j))
            elif cell == '*':  # Stone on a switch
                if pos < len(numbers):
                    weight = numbers[pos]
                    start_stones.append((i, j, weight))
                    switches.append((i, j))
                    pos += 1
            # else: empty space

    if Ax == -1 or Ay == -1:
        print("Error: Player starting position '@' not found.")
        return

    start_state = State(
        x=Ax,
        y=Ay,
        stones=start_stones,
        g=0,
        f=0  # Will compute f below
    )

    start_state.f = start_state.g + get_heuristic(start_state, switches)

    # Movement directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dir_chars = ['u', 'd', 'l', 'r']

    # Priority queue for A* algorithm
    queue = PriorityQueue()
    queue.put(start_state)
    g_score = {start_state: start_state.g}
    before = {}

    last = None  # Variable to store the goal state

    # A* algorithm
    while not queue.empty():
        node += 1
        current_state = queue.get()

        if is_goal(current_state, switches):
            last = current_state
            break

        for v, dir_char in zip(directions, dir_chars):
            new_x = current_state.x + v[0]
            new_y = current_state.y + v[1]

            if not is_valid(new_x, new_y, grid):
                continue

            # Check if there is a stone at the new position
            stone_at_new_pos = None
            for idx, stone in enumerate(current_state.stones):
                if (stone[0], stone[1]) == (new_x, new_y):
                    stone_at_new_pos = (idx, stone)
                    break

            # Create new stones list
            new_stones = [stone for stone in current_state.stones]
            new_g = current_state.g

            if stone_at_new_pos:
                # There is a stone at new_x, new_y
                stone_idx, stone = stone_at_new_pos
                # Check if we can push the stone
                push_x = new_x + v[0]
                push_y = new_y + v[1]
                if not is_valid(push_x, push_y, grid):
                    continue
                # Check if another stone is at push_x, push_y
                if any((s[0], s[1]) == (push_x, push_y) for s in current_state.stones):
                    continue
                # Push the stone
                stone_weight = stone[2]
                new_g += stone_weight
                # Update the stone's position
                new_stones[stone_idx] = (push_x, push_y, stone_weight)
                # Move the player to new_x, new_y
                action = dir_char.upper()
            else:
                # No stone at new_x, new_y
                action = dir_char.lower()

            new_state = State(
                x=new_x,
                y=new_y,
                stones=new_stones,
                g=new_g,
                f=0  # Will compute f below
            )

            new_state.f = new_state.g + get_heuristic(new_state, switches)

            if (new_state in g_score and new_g >= g_score[new_state]):
                continue

            before[new_state] = (current_state, action)
            g_score[new_state] = new_g
            queue.put(new_state)

    # Calculate time and memory usage
    time_ms = (time.time() - start_time) * 1000
    memory_usage = print_memory_usage()

    # Write results to output file
    with open(output_filename, 'w') as f_out:
        if last is not None:
            # Create path string
            path = []
            current = last
            while current != start_state:
                prev_state, move = before[current]
                path.append(move)
                current = prev_state

            path_str = ''.join(reversed(path))
            steps = len(path)

            # Write information to file
            f_out.write('A*\n')
            f_out.write('Steps: {}, Weight: {}, Node: {}, Time (ms): {:.2f}, Memory (MB): {:.2f}\n'.format(
                steps, last.g,node, time_ms, memory_usage))
            f_out.write(path_str + '\n')
        else:
            f_out.write('No solution found.\n')
            f_out.write('Nodes Expanded: {}, Time (ms): {:.2f}, Memory (MB): {:.2f}\n'.format(
                node, time_ms, memory_usage))

def main():
    for id in range(1,11):  # Adjust range as needed
        input_filename = os.path.join('input', f'input-{id:02d}.txt')
        print(f"Processing {input_filename}")
        search(input_filename, id)

if __name__ == "__main__":
    main()

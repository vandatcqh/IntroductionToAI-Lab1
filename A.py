import psutil
import time
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
from queue import PriorityQueue
import itertools

def print_memory_usage() -> int:
    """Get current process memory usage in MB"""
    process = psutil.Process()
    return int(process.memory_info().rss / (1024 * 1024))

@dataclass
class State:
    f: int = -1
    x: int = -1
    y: int = -1
    g: int = -1
    stones: List[List[int]] = None

    def __post_init__(self):
        if self.stones is None:
            self.stones = []

    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        if self.g != other.g:
            return self.g < other.g

        this_stones = sorted(self.stones)
        other_stones = sorted(other.stones)

        for i in range(len(this_stones)):
            if this_stones[i] != other_stones[i]:
                return this_stones[i] < other_stones[i]
        return False

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.f == other.f and 
                self.x == other.x and 
                self.y == other.y and 
                self.g == other.g and 
                sorted(self.stones) == sorted(other.stones))

    def __hash__(self):
        return hash((self.f, self.x, self.y, self.g, 
                    tuple(tuple(stone) for stone in sorted(self.stones))))

def is_valid(x: int, y: int, grid: List[str]) -> bool:
    return not (x < 0 or y < 0 or x >= len(grid) or 
                y >= len(grid[0]) or grid[x][y] == '#')

def get_heuristic(state: State, switches: List[Tuple[int, int]]) -> int:
    """Calculate minimum cost to move stones to switches"""
    def generate_permutations(n: int, state: State) -> int:
        ans = float('inf')
        for perm in itertools.permutations(range(n)):
            var = 0
            for i in range(n):
                pos = perm[i]
                var += (abs(state.stones[i][0] - switches[pos][0]) + 
                       abs(state.stones[i][1] - switches[pos][1])) * state.stones[i][2]
            ans = min(ans, var)
        return ans
    
    return generate_permutations(len(state.stones), state)

def is_goal(state: State, switches: List[Tuple[int, int]]) -> bool:
    return get_heuristic(state, switches) == 0

def main():
    # Read input
    numbers = list(map(int, input().split()))
    grid = []
    while True:
        try:
            line = input()
            if not line:
                break
            grid.append(line)
        except EOFError:
            break

    start_time = time.time()
    node = 0

    # Initialize game state
    Ax = Ay = 0
    switches = []
    start = State(stones=[])
    pos = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '@':
                Ax, Ay = i, j
            elif grid[i][j] == '$':
                start.stones.append([i, j, numbers[pos]])
                pos += 1
            elif grid[i][j] == '.':
                switches.append((i, j))

    # Directions: left, right, up, down
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    dir_chars = ['l', 'r', 'u', 'd']

    # Initialize start state
    start.f = get_heuristic(start, switches)
    start.x = Ax
    start.y = Ay
    start.g = 0

    # Priority queue for A* search
    queue = PriorityQueue()
    queue.put(start)
    f_score = {start: start.f}
    g_score = {start: start.g}
    before = {}
    
    # A* search
    while not queue.empty():
        node += 1
        top = queue.get()
        
        if is_goal(top, switches):
            last = top
            break

        for v, dir_char in zip(directions, dir_chars):
            newstate = State(
                stones=[stone.copy() for stone in top.stones],
                x=top.x + v[0],
                y=top.y + v[1],
                g=top.g
            )

            if is_valid(newstate.x, newstate.y, grid):
                check1 = check2 = False
                pos1 = -1

                for i in range(len(top.stones)):
                    if top.stones[i][0] == newstate.x and top.stones[i][1] == newstate.y:
                        check1 = True
                        pos1 = i
                    if (top.stones[i][0] == newstate.x + v[0] and 
                        top.stones[i][1] == newstate.y + v[1]):
                        check2 = True

                if (check1 and is_valid(newstate.x + v[0], newstate.y + v[1], grid) 
                    and not check2):
                    newstate.g += top.stones[pos1][2]
                    newstate.stones[pos1][0] = newstate.x + v[0]
                    newstate.stones[pos1][1] = newstate.y + v[1]

                newstate.f = newstate.g + get_heuristic(newstate, switches)

                if (newstate in f_score and 
                    f_score[newstate] <= newstate.g + get_heuristic(newstate, switches)):
                    continue

                before[newstate] = (top, dir_char)
                f_score[newstate] = newstate.f
                g_score[newstate] = newstate.g
                queue.put(newstate)

    # Generate output
    print(f_score[last])
    current = last
    while current in before:
        print(f"{current.x} {current.y}")
        current, _ = before[current]
    
    print(print_memory_usage())
    print(int((time.time() - start_time) * 1000))  # Convert to milliseconds
    print(node)
    
    # Reconstruct path
    path = []
    current = last
    while current in before:
        prev_state, move = before[current]
        if prev_state.g != current.g:
            move = move.upper()
        path.append(move)
        current = prev_state

    print(''.join(reversed(path)))

if __name__ == "__main__":
    main()
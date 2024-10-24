import heapq
import time
import sys

class State:
    def __init__(self, walls, stones, switches, player, move, sum_weight, weights):
        self.walls = walls
        self.stones = stones  
        self.switches = switches
        self.player = player
        self.move = move
        self.sum_weight = sum_weight
        self.weights = weights  

    def getNeighbors(self):
        x, y = self.player
        self.neighbors = []  

        self.movePlayer(x - 1, y, x - 2, y, "u")
        self.movePlayer(x + 1, y, x + 2, y, "d")
        self.movePlayer(x, y - 1, x, y - 2, "l")
        self.movePlayer(x, y + 1, x, y + 2, "r")

        return self.neighbors

    def movePlayer(self, ax, ay, bx, by, direction):
        attempt = (ax, ay)
        newstone = (bx, by)
        if attempt not in self.walls:
            if attempt not in self.stones or (newstone not in self.stones and newstone not in self.walls):
                if attempt in self.stones:
                    stones_copy = self.stones.copy()
                    weight = stones_copy[attempt]
                    del stones_copy[attempt]
                    stones_copy[newstone] = weight
                    sum_weight = self.sum_weight + weight
                    self.neighbors.append(State(
                        self.walls,
                        stones_copy,
                        self.switches,
                        attempt,
                        self.move + direction.upper(),
                        sum_weight,
                        self.weights
                    ))
                else:
                    sum_weight = self.sum_weight
                    self.neighbors.append(State(
                        self.walls,
                        self.stones.copy(),
                        self.switches,
                        attempt,
                        self.move + direction,
                        sum_weight,
                        self.weights
                    ))

    def reachedGoal(self):
        return all(stone in self.switches for stone in self.stones)

    def getMove(self):
        return self.move

    def __hash__(self):
        # Hash based on player position and stones with their weights
        return hash((self.player, frozenset(self.stones.items())))

    def __eq__(self, other):
        return self.player == other.player and self.stones == other.stones

    def __lt__(self, other):
        # Prioritize smaller sum_weight in heapq
        if self.sum_weight != other.sum_weight:
            return self.sum_weight < other.sum_weight
        else:
            # Tie-breaker based on move length
            return len(self.move) < len(other.move)

class UCS:
    def __init__(self, start_state):
        self.start_state = start_state

    def ucs(self):
        pq = []
        heapq.heappush(pq, (self.start_state.sum_weight, self.start_state))
        costs = {}
        start_time = time.time()
        max_memory = 0
        cnt_node = 0
        while pq:
            cnt_node += 1
            cost, current_state = heapq.heappop(pq)
            if current_state in costs and costs[current_state] <= cost:
                continue
            costs[current_state] = cost
            if current_state.reachedGoal():
                total_time = (time.time() - start_time) * 1000
                return current_state.getMove(), current_state.sum_weight, total_time, max_memory, cnt_node
            for neighbor in current_state.getNeighbors():
                neighbor_cost = neighbor.sum_weight
                if neighbor not in costs or neighbor_cost < costs.get(neighbor, float('inf')):
                    heapq.heappush(pq, (neighbor_cost, neighbor))
            current_memory = sys.getsizeof(pq) + sys.getsizeof(costs)
            max_memory = max(max_memory, current_memory)
        total_time = (time.time() - start_time) * 1000
        return None, float("inf"), total_time, max_memory

def Search(file_path):
    with open(file_path, 'r') as file:
        # Read the first line (weights of the stones)
        weights_line = file.readline().strip()
        weights = list(map(int, weights_line.split()))
        # Read the rest of the lines (Sokoban grid)
        grid = [list(line.rstrip()) for line in file.readlines()]
    
    stones = {}
    switches = set()
    walls = set()
    player = None
    stone_index = 0  # To assign weights to stones

    # Traverse the grid and add positions to respective sets
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '$':
                if stone_index < len(weights):
                    stones[(i, j)] = weights[stone_index]
                else:
                    print("Error: Not enough weights provided for all stones.")
                    return
                stone_index += 1
            elif grid[i][j] == '.':
                switches.add((i, j))
            elif grid[i][j] == '#':
                walls.add((i, j))
            elif grid[i][j] == '@':
                player = (i, j)
            elif grid[i][j] == '*':
                switches.add((i, j))
                if stone_index < len(weights):
                    stones[(i, j)] = weights[stone_index]
                else:
                    print("Error: Not enough weights provided for all stones.")
                    return
                stone_index += 1

    if stone_index != len(weights):
        print("Error: Number of stones does not match number of weights.")
        return

    start_state = State(walls, stones, switches, player, "", 0, weights)

    # Run UCS
    ucs_solver = UCS(start_state)
    solution, sum_weight, total_time, max_memory, cnt_node = ucs_solver.ucs()
    with open("output/UCS/output-02.txt", "w") as file:
        if solution:
            file.write(f"Steps: {len(solution)}, Node: {cnt_node}, Weight: {sum_weight}, Time (ms): {total_time:.2f}, Memory (MB): {max_memory / 1048576:.2f}\n")
            file.write(str(solution) + "\n")
        else:
            file.write("No solution found.\n")



if __name__ == "__main__":
    file_path = "input/input-02.txt"  # Path to input.txt file
    Search(file_path)  # Call the Search function with the file path

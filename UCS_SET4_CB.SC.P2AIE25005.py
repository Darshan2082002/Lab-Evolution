import heapq

def is_goal(state, goal):
    
    return state == goal

def get_clear_blocks(state):
    
    occupied = set(state.values())  
    return [b for b in state if b not in occupied]

def get_successors(state):
   
    succs = []
    clear = get_clear_blocks(state)
    for block in clear:
        
        if state[block] != "table":
            new_state = state.copy()
            new_state[block] = "table"
            succs.append((f"Move({block}, table)", new_state))

        
        for target in clear:
            if block == target:
                continue
           
            if state[block] == target:
                continue
            new_state = state.copy()
            new_state[block] = target
            succs.append((f"Move({block}, {target})", new_state))
    return succs

def uniform_cost_search(start, goal):
  
    pq = []
    tie = 0
    heapq.heappush(pq, (0, tie, start, []))

    visited = set()  

    while pq:
        cost, _, state, path = heapq.heappop(pq)
        state_key = tuple(sorted(state.items()))  
        if state_key in visited:
            continue
        visited.add(state_key)

        if is_goal(state, goal):
            return path

        for action, new_state in get_successors(state):
            tie += 1
            heapq.heappush(pq, (cost + 1, tie, new_state, path + [action]))

    return None

if __name__ == "__main__":
    
    init_state = {"A": "table", "B": "A", "C": "B", "D": "C"}
    goal_state = {"D": "table", "C": "D", "B": "C", "A": "B"}

    solution = uniform_cost_search(init_state, goal_state)

    print("UCS Solution Path:")
    if solution:
        for step in solution:
            print(step)
    else:
        print("No solution found")

def is_goal(state, goal):
    return state == goal

def clear_blocks(state):
    occupied = set(state.values())
    return [b for b in state if b not in occupied]

def successors(state):
    succs = []
    clear = clear_blocks(state)
    for x in clear:  
        
        if state[x] != "table":
            new_state = state.copy()
            new_state[x] = "table"
            succs.append((f"Move({x}, table)", new_state))
        
        for y in clear:
            if x != y:
                new_state = state.copy()
                new_state[x] = y
                succs.append((f"Move({x}, {y})", new_state))
    return succs

def dfs(init, goal):
    stack = [(init, [])]
    visited = set()
    while stack:
        state, path = stack.pop()
        if tuple(state.items()) in visited:
            continue
        visited.add(tuple(state.items()))
        if is_goal(state, goal):
            return path
        for action, new_state in successors(state):
            stack.append((new_state, path + [action]))
    return None


if __name__ == "__main__":
    init_state = {"A": "table", "B": "A", "C": "B", "D": "C"}
    goal_state = {"D": "table", "C": "D", "B": "C", "A": "B"}
    solution = dfs(init_state, goal_state)
    print("DFS Solution Path:")
    if solution:
        for step in solution:
            print(step)
    else:
        print("No solution found")

#https://adventofcode.com/2018/day/7

stepsfname = "inp\\day_seven.txt"

def parseInp():
    stepFile = [line.rstrip() for line in open(stepsfname).readlines()]
    steps_list = []

    for line in stepFile:

        action = line[5]
        dependency = line[-12]
        ctuple = (action, dependency)
        steps_list.append(ctuple)
    
    return steps_list

def generate_char_list(step_list):
    all_chars = []

    for step in step_list:
        if not step[0] in all_chars:
            all_chars.append(step[0])
        
        if not step[1] in all_chars:
            all_chars.append(step[1])

    return sorted(all_chars)

def generate_grid_map(char_list):
    map = {}

    for char in char_list:
        these_edges = {}

        for edge_char in char_list:
            these_edges[edge_char] = False
        
        map[char] = these_edges
    
    return map

def determine_connections(step_list, graph):
    for step in step_list:
        graph[step[0]][step[1]] = True

    return graph

def isEmpty(graph):
    count = 0

    for key in graph.keys():
        count+=1
    
    return count == 0

def find_path(graph):
    exec_steps = []

    while not isEmpty(graph):
        candidates = []

        for node in graph.keys():
            c_count = 0

            for conn_node in graph.keys():
                if conn_node == node:
                    continue
                else:
                    c_arr = graph[conn_node]

                    if c_arr.get(node):
                        c_count+=1
        
            if c_count == 0:
                candidates.append(node)

        sorted(candidates)

        exec_steps.append(candidates[0])
        graph.pop(candidates[0])

    print("FINAL STEPS:", "".join(exec_steps))


            
step_list = parseInp()

all_chars = generate_char_list(step_list)

print(step_list)

print(all_chars)

graph = generate_grid_map(all_chars)

graph = determine_connections(step_list, graph)

print(graph)

find_path(graph)
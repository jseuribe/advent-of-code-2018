#https://adventofcode.com/2018/day/7
from copy import copy

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

        #Determine what nodes have no incoming edges.
        for node in graph.keys():
            c_count = 0

            #Examine all nodes, and determine which have connections to it
            for conn_node in graph.keys():
                if conn_node == node:
                    continue
                else:
                    c_arr = graph[conn_node]

                    if c_arr.get(node):
                        #If there is a node connected to our currently processing node, then increment
                        c_count+=1
        
            #if this value is 0, then this node has no incoming connections. it is next in the step order
            if c_count == 0:
                candidates.append(node)

        sorted(candidates)

        exec_steps.append(candidates[0])
        graph.pop(candidates[0])

    print("FINAL STEPS:", "".join(exec_steps))

    return exec_steps

def create_completion_map(step_list):
    completion_map = {}
    for key in step_list:
        if key not in completion_map:
            completion_map[key] = False

    return completion_map

def incr_if_busy(workers):

    for worker in workers:
        if worker[2] != '.':
            worker[1] += 1
    return workers

def det_finished(workers):
    for worker in workers:
        if worker[1] == worker[3]:
            worker[3] = -1
            worker[2] = '.'
            worker[1] = 0

    return workers

def collect_finished(workers):
    finished = []
    for worker in workers:
        if worker[1] == worker[3]:
            finished.append(worker[2])
    
    return finished

def return_not_busy(workers):
    not_busy = []
    for worker in workers:
        if worker[2] == '.':
            not_busy.append(worker[0])
    
    return not_busy

def determine_if_currently_processing(workers, node):
    for worker in workers:
        if node == worker[2]:
            return False
    
    return True

def determine_bad_outcome(workers):
    not_busy_workers = 0
    for worker in workers:
        if worker[3] == -1:
            not_busy_workers += 1
    
    return not_busy_workers == len(workers)


def determine_incoming_edgeless_nodes(graph):
    edgeless_nodes = []
    for node in graph:
        conns = 0
        for cnode in graph:

            if cnode == node:
                continue

            if graph[cnode][node]:
                conns+=1

        if conns == 0:
            edgeless_nodes.append(node)
    return edgeless_nodes

def determine_if_node_has_no_incoming_edges(graph, node):
    conns = 0

    for cnode in graph:
        if cnode == node:
            continue

        if graph[cnode][node]:
            conns+=1
        
    if conns == 0:
        return True
    
    return False

def calculate_time_to_complete(step_map, exec_steps):
    alpha_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K':11,'L':12, 'M':13,'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26}
    completion_map = create_completion_map(exec_steps)
    completed_steps = []
    c_sec = 0
    workers = [[0,0,'.', -1],[1,0,'.', -1], [2,0,'.', -1], [3,0,'.', -1], [4,0,'.',-1]]
    #workers = [[0,0,'.', -1],[1,0,'.', -1]]

    #Step 0: Determine what seed values the workers will begin with
    available_work = sorted(determine_incoming_edgeless_nodes(step_map))

    #Sort the work, so that work is always assigned alphabetically
    acted_nodes = sorted(copy(available_work))

    print("Seed values", available_work)
    print("Seconds | Worker 1 | Worker 2 | Worker 3 | Worker 4 | Worker 5 | Done")
    while completion_map:
        
        #Step one: Collect any workers who are done
        finished = collect_finished(workers)
        workers = det_finished(workers)

        for node in finished:
            #Step two: For all nodes that have been finished:

            #Update the completion map, and the list of completed steps
            completion_map.pop(node)
            completed_steps.append(node)

            #if the node isn't in the list of acted nodes, add it. this list is checked to avoid dupes
            if node not in acted_nodes:
                acted_nodes.append(node)

            #Update the executed steps, and then remove the node from the current list of connections
            if node in exec_steps:
                exec_steps.remove(node)
                step_map.pop(node)

            #Step three: Determine if there are any new nodes that have no incoming edges
            exposed_nodes = determine_incoming_edgeless_nodes(step_map)
            for new_node in exposed_nodes:
                if new_node not in acted_nodes:
                    #add any new nodes to the list of work waiting
                    available_work.append(new_node)
                    acted_nodes.append(new_node)

        #Step four: sort the available nodes to be consumed
        sorted(available_work)

        #Step five: Determine if any workers are not busy
        c_available_workers = return_not_busy(workers)

        for c_available_worker in c_available_workers:

            #Determine if there is work to be consumed, if not, then do not proceed with worker delegation
            if available_work:
                work = available_work.pop(0)
            else:
                break

            #Step six: if there is work to be done, delegate the work to the first available worker
            first_available_worker = c_available_worker
            workers[first_available_worker][2] = work
            workers[first_available_worker][3] = 60+alpha_map[workers[first_available_worker][2]]

        #Step Seven: update the work performed at this step, then print out the current state of progression
        workers = incr_if_busy(workers)
        c_sec += 1
        print("{0} {1} {2} {3} {4} {5} | {6}".format(c_sec, workers[0][2], workers[1][2], workers[2][2], workers[3][2], workers[4][2], ''.join(completed_steps)))
        #print("{0} {1} {2} | {3}".format(c_sec, workers[0][2], workers[1][2], ''.join(completed_steps)))

    #Accomodate for the offset of starting at step 1.
    print("COMPLETED STEPS:", completed_steps, c_sec-1)

if __name__ == "__main__":
    step_list = parseInp()

    all_chars = generate_char_list(step_list)

    graph = generate_grid_map(all_chars)

    graph = determine_connections(step_list, graph)

    #keep the graph for problem 2
    step_map = copy(graph)

    #determine problem 1's solution
    exec_steps = find_path(graph)
    print(exec_steps)
    #calculate_time_to_complete(step_map, exec_steps)
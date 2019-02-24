#https://adventofcode.com/2018/day/8
import sys

sys.setrecursionlimit(500000)
license_file = "inp\\day_eight.txt"
#using a global counter because...well it makes sense I guess! (thse would just be in the local scope)
global_data = []
element_list = []

class node:

    def __init__(self, children=0, meta_data=0, index=0):
        self.children = children
        self.counter_children = children
        self.meta_data = meta_data
        self.index = index
        self.meta_data_list = []
        self.incre_value = 0
        self.children_nodes = []
        self.parent_node = None

    def set_values(self, children, meta_data, index, meta_data_list):
        self.children = children
        self.meta_data = meta_data
        self.index = index
        self.meta_data_list = meta_data_list

    def print(self):
        return "[children: {0}, meta_data: {1}, index: {2}, meta_data: {3}]".format(self.children, self.meta_data, self.index, self.meta_data_list)

def obtain_first_node_header(element_list):
    return node(element_list[0], element_list[1], 1)

def obtain_header_at(index):
    return node(element_list[index+1], element_list[index+2], index+2)

def get_lengths(node):
    c_sum = 0
    if not node.children_nodes:
        return 2+len(node.meta_data_list)
    
    else:
        for child in node.children_nodes:
            c_sum += get_lengths(child)
            if len(child.children_nodes) != 0:
                c_sum += 2+child.meta_data

    return c_sum

def parse_node(node, step=0):
    '''
    extremely bad first recursive attempt
    '''
    node_count = node[0]
    meta_data = node[1]
    index_at = node[2]

    while node_count != 0:
        n_node = obtain_header_at(index_at)

        n_node_meta_data = parse_node(n_node, step+1)
        #print("Meta data:", n_node_meta_data)
        global_data.extend(n_node_meta_data)
        
        index_at += 2+len(n_node_meta_data)
        del n_node_meta_data
        del n_node
        print("Index:", index_at, "at step:", step)

        node_count -= 1
    
    #print("INDEX:", index_at)
    if step == 0:
        index_at += 3
    node_meta_data = element_list[index_at+1:index_at+meta_data+1]
    return node_meta_data

def parse_tree(node, step=0):

    children = node.children
    memo = [node]
    memo_at = 0

    c_index = node.index
    while memo:
        print("cmemo:", memo[memo_at].print(), memo[memo_at].counter_children)

        if memo[memo_at].counter_children == 0:
            if memo[memo_at].parent_node:
                memo[memo_at].parent_node.counter_children -= 1
            print("no children left")
            incre_val = get_lengths(memo[memo_at])
            print("incre val:", incre_val)
            memo[memo_at].meta_data_list.extend(element_list[memo[memo_at].index+incre_val+1:memo[memo_at].index+incre_val+1+memo[memo_at].meta_data])
            print("meta data:", memo[memo_at].meta_data_list)
            global_data.extend(memo[memo_at].meta_data_list)
            memo.pop()
            if memo:
                print("REMAINDER MEMO")
                memo_at -= 1
                c_index = memo[memo_at].index
            else:
                print("EMPTY")

            continue

        if len(memo[memo_at].children_nodes) > 0:
            #if the current parent node has children
            c_index += get_lengths(memo[memo_at])

        next_node = obtain_header_at(c_index)
        memo[memo_at].children_nodes.append(next_node)

        if next_node.counter_children == 0:

            print("no children")
            c_node_meta_data = element_list[next_node.index+1:next_node.index+1+next_node.meta_data]
            print("meta data", c_node_meta_data)
            memo[memo_at].counter_children -= 1

        else:
            print("node has children to be processed")
            next_node.parent_node = memo[memo_at]
            memo_at += 1
            memo.append(next_node)
            c_node_meta_data = []
            c_index += 2


        #print("meta data",c_child_meta_data)

        if c_node_meta_data:
            global_data.extend(c_node_meta_data)
            next_node.meta_data_list.extend(c_node_meta_data)


    
def collect_nodes(node):

    if not node.children_nodes:
        print(node.meta_data_list)
        global_data.extend(node.meta_data_list)
        return

    for node in node.children_nodes:
        if node.children_nodes:
            collect_nodes(node)
        global_data.extend(node.children_nodes)

def print_obtained_nodes(node):
    if not node.children_nodes:
        print(node.print())
        return

    for c_node in node.children_nodes:
        print_obtained_nodes(c_node)
    
    print(node.print())

def parseInp():

    with open(license_file, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]

        for line in lines:
            for char in line.split(' '):
                element_list.append(int(char))

    return element_list

if __name__ == "__main__":
    element_list = parseInp()
    print("length of elements:", len(element_list))
    first_node_header = obtain_first_node_header(element_list)

    parse_tree(first_node_header)

    #collect_nodes(first_node_header)

    print(global_data)

    print("results:")
    print_obtained_nodes(first_node_header)

    print(sum(global_data))
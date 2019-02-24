#https://adventofcode.com/2018/day/8
import sys

sys.setrecursionlimit(500000)
license_file = "inp\\day_eight.txt"
#using a global counter because...well it makes sense I guess! (these would just be in the local scope...but i am lazy)
global_data = []
element_list = []

class node:

    def __init__(self, children=0, meta_data=0, index=0):
        self.children = children
        self.counter_children = children
        self.meta_data = meta_data
        self.index = index
        self.meta_data_list = []
        self.children_nodes = []
        self.parent_node = None

        self.value = 0
        self.b_value_set = False


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
    This actually kind of works (worked with example), but Python's bad at tail recursion!!!
    Not even setting the recursion depth helped it...
    Maybe this approach works in a language that's tail recursion friendly???
    '''
    node_count = node[0]
    meta_data = node[1]
    index_at = node[2]

    while node_count != 0:
        n_node = obtain_header_at(index_at)

        n_node_meta_data = parse_node(n_node, step+1)
        #print("Meta data:", n_node_meta_data)
        global_data.extend(n_node_meta_data)
        
        index_at += 2+get_lengths(n_node)
        #I thought freeing up memory would help..but alas..
        del n_node_meta_data
        del n_node
        print("Index:", index_at, "at step:", step)

        node_count -= 1
    
    #print("INDEX:", index_at)
    index_at += node.index + get_lengths(n_node)
    node_meta_data = element_list[index_at+1:index_at+meta_data+1]
    return node_meta_data

def parse_tree(node, step=0):
    '''
    Part One Solution/Tree builder for part two
    element_list containing the values of the input, and global_list containing the meta_data of all nodes, is global
    They could be local here, but it wouldn't really matter!!!
    '''
    children = node.children
    #Think of the memo as our "Memory Stack"
    memo = [node]
    memo_at = 0

    c_index = node.index
    while memo:
        print("cmemo:", memo[memo_at].print(), memo[memo_at].counter_children)

        if memo[memo_at].counter_children == 0:
            '''State where the children of this node have been visited'''

            if memo[memo_at].parent_node:
                #If this is a node that has a parent, decrement its parent children by one, signifying its child has been visited
                memo[memo_at].parent_node.counter_children -= 1
            
            print("no children left")
            incre_val = get_lengths(memo[memo_at])

            #Fetch the current node's meta data by adding the entries that its children occupies, then grabbing the x elements after those
            memo[memo_at].meta_data_list.extend(element_list[memo[memo_at].index+incre_val+1:memo[memo_at].index+incre_val+1+memo[memo_at].meta_data])
            
            print("meta data:", memo[memo_at].meta_data_list)
            global_data.extend(memo[memo_at].meta_data_list)

            memo.pop()
            #After consuming the current node
            if memo:
                #Either jump back to the node's parent
                print("REMAINDER MEMO")
                memo_at -= 1
                c_index = memo[memo_at].index
            else:
                #Or we're done processing the tree.
                print("EMPTY")

            continue

        #If the node has children to speak of
        if len(memo[memo_at].children_nodes) > 0:
            #if the current parent node has children, increment the next node to check according to the children of this current node visited
            c_index += get_lengths(memo[memo_at])

        #obtain the next child
        next_node = obtain_header_at(c_index)
        memo[memo_at].children_nodes.append(next_node)

        if next_node.counter_children == 0:
            #State where the next node has children already..could probably have handled this end state a bit better
            print("no children")
            c_node_meta_data = element_list[next_node.index+1:next_node.index+1+next_node.meta_data]
            print("meta data", c_node_meta_data)
            #Decrement the children of this current node by one
            memo[memo_at].counter_children -= 1

        else:
            #This node has children
            print("node has children to be processed")
            #Set the node's parent to the current position in the memo
            next_node.parent_node = memo[memo_at]
            #Increment the memo position, add the node to the memo, and increment the counter by 2
            memo_at += 1
            memo.append(next_node)
            c_node_meta_data = []
            c_index += 2

        if c_node_meta_data:
            global_data.extend(c_node_meta_data)
            next_node.meta_data_list.extend(c_node_meta_data)
    
def collect_nodes(node):
    '''
    Part Two Solution Function
    '''
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

def collect_sums(node):

    if node.children == 0:
        #If this is a childless node, its value is just its meta-data-list
        node.value = sum(node.meta_data_list)
        node.b_value_set = True
        return

    c_sum = 0

    #Otherwise, it is the values of its children, corresponding to the entries of its meta data list
    for c_node_index in node.meta_data_list:

        if c_node_index > node.children:
            #if the entry is for a nonexistant child (IE: bigger than the actual child list)
            continue
        else:
            c_node = node.children_nodes[c_node_index-1]

            if c_node.b_value_set:
                c_sum += c_node.value
            else:
                collect_sums(c_node)
                c_sum += c_node.value
    
    node.value = c_sum
    node.b_value_set = True

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
    print("PART ONE SOLUTION:", sum(global_data))

    collect_sums(first_node_header)
    print("PART TWO SOLUTION:", first_node_header.value)

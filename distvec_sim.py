import os.path

# nodes on the network
class Node:
    def __init__(self, name):
        self.name = name
        self.edges = set(())
        self.routingtable = {}

    def __str__(self):
        return self.name

# edge between nodeso on the network
class Edge:
    def __init__(self, data):
        self.nodes = [data[0], data[1]]
        self.weight = int(data[2])

# build a new graph representing our network from a .txt file
def new_graph_from_file(path):
    try:
        with open(path) as f:
            nodes = []
            edges = []
            node_initializer = f.readline().split()
            for node in node_initializer:
                nodes.append(Node(node))
            for line in f.readlines():
                edge_data = line.split()
                for node in nodes:
                    if node.name == edge_data[0]:
                        edge_data[0] = node
                    elif node.name == edge_data[1]:
                        edge_data[1] = node
                edges.append(Edge(edge_data))
            for edge in edges:
                edge.nodes[0].edges.add(edge)
                edge.nodes[1].edges.add(edge)
        graph = {"nodes": nodes, "edges": edges}
        return graph
    except:
        print(" Could not build network from file. Check file contents and try again. Exiting...")
        quit()

# set nodes to know the cost to themselves is 0 and there is no intermediate node
def initialise(graph):
    nodes = graph['nodes']
    for node in nodes:
        node.routingtable[node.name] = (0, None, None)
    return

# print current routing tables in format "From <NodeA>: <NodeB>: cost/via <NodeC>: cost/via . . ."
def print_all_tables(graph, t):
    nodes = graph['nodes']
    tableString = ""
    print(" T = " + str(t)) 
    for node in nodes:
        print(" From " + node.name + " (cost/via): \t", end="")
        tableString += ("From " + node.name + " (cost/via): \t")
        for route in node.routingtable:
            print(route + ": " + str(node.routingtable[route][0]) + " / " + str(node.routingtable[route][1]) + "\t", end="")
            tableString += (route + ": " + str(node.routingtable[route][0]) + " / " + str(node.routingtable[route][1]) + "\t")
        print()
    print()
    return tableString

# initialise nodes to know their immediate neighbours
def first_step(graph, t):
    edges = graph['edges']
    for edge in edges:
        edge.nodes[0].routingtable[edge.nodes[1].name] = (edge.weight, edge.nodes[1].name, None)
        edge.nodes[1].routingtable[edge.nodes[0].name] = (edge.weight, edge.nodes[0].name, None)

    return t

# advance the simulation by 1 time unit - updating routing tables based on those of immediate neighbours
def step(graph, t):
    nodes = graph['nodes']
    edges = graph['edges']

    table_snapshots = {}

    # capture each node's routing table at time t
    for node in nodes:
        table_snapshots[node.name] = node.routingtable

    # for each node
    for node in nodes:
        # for each edge
        for edge in node.edges:
            # dest = the node at the other end of the edge
            if edge.nodes[0] == node:
                dest = edge.nodes[1]
            else:
                dest = edge.nodes[0]
            
            # for each rout in snapshot table for dest node
            for entry in table_snapshots[dest.name]:
                # if entry is for node, skip
                if entry == node.name:
                    pass
                # if there's no corresponding entry in the current node's table
                elif entry not in node.routingtable:
                    # create an entry, with dest as next hop, sum the weights
                    node.routingtable[entry] = ((table_snapshots[dest.name][entry][0] + edge.weight), dest.name, dest.name)
                # otherwise if the path from node to entry via dest is shorter    
                elif (table_snapshots[dest.name][entry][0] + edge.weight) < node.routingtable[entry][0]:
                    # update entry with new weigh and next hop
                    node.routingtable[entry] = ((table_snapshots[dest.name][entry][0] + edge.weight), dest.name, dest.name)
                else:
                    # do nothing
                    pass

    t += 1
    return t

# as above but with split horizon mode enabled
def sh_step(graph, t):
    nodes = graph['nodes']
    edges = graph['edges']

    table_snapshots = {}

    # capture each node's routing table at time t
    for node in nodes:
        table_snapshots[node.name] = node.routingtable

    # for each node
    for node in nodes:
        # for each edge
        for edge in node.edges:
            # dest = the node at the other end of the edge
            if edge.nodes[0] == node:
                dest = edge.nodes[1]
            else:
                dest = edge.nodes[0]
            
            # for each rout in snapshot table for dest node
            for entry in table_snapshots[dest.name]:
                # if entry is for node, skip
                if entry == node.name:
                    pass
                # split horizon - node ignores routes that originated from self
                elif table_snapshots[dest.name][entry][2] == node.name:
                    pass
                # if there's no corresponding entry in the current node's table
                elif entry not in node.routingtable:
                    # create an entry, with dest as next hop, sum the weights
                    node.routingtable[entry] = ((table_snapshots[dest.name][entry][0] + edge.weight), dest.name, dest.name)
                # otherwise if the path from node to entry via dest is shorter    
                elif (table_snapshots[dest.name][entry][0] + edge.weight) < node.routingtable[entry][0]:
                    # update entry with new weigh and next hop
                    node.routingtable[entry] = ((table_snapshots[dest.name][entry][0] + edge.weight), dest.name, dest.name)
                else:
                    # do nothing
                    pass

    t += 1
    return t

# find an edge and update its weight
def change(graph):
    edges = graph['edges']
    print()
    print(" Change cost of link between which two nodes? [Ni Nj]")
    nodes = input(" >> ").split()
    print(" Enter new cost: ")
    cost = input(" >> ")

    try:
        cost = int(cost)
    except:
        print(" Invalid cost.")
        print(" Press enter to advance.")
        adv = input(" >> ")
        print(" Advancing...")
        return

    for edge in edges:
        if (edge.nodes[0].name == nodes[0] or edge.nodes[0].name == nodes[1]):
            if (edge.nodes[1].name == nodes[0] or edge.nodes[1].name == nodes[1]):
                # update edge weight and routing table entries of nodes at eithher end of edge
                edge.weight = cost
                edge.nodes[0].routingtable[edge.nodes[1].name] = (edge.weight, edge.nodes[1].name, None)
                edge.nodes[1].routingtable[edge.nodes[0].name] = (edge.weight, edge.nodes[0].name, None)
                print(" Cost updated.")
                print(" Press enter to advance.")
                adv = input(" >> ")
                print("Advancing...")
                return
    print(" Could not find specified link.")
    print(" Press enter to advance.")
    adv = input(" >> ")
    print(" Advancing...")
    return

# find an edge and remove it
def delete(graph):
    edges = graph['edges']
    print()
    print(" Delete link between which two nodes? [Ni Nj]")
    nodes = input(" >> ").split()
        
    for edge in edges:
        if (edge.nodes[0].name == nodes[0] or edge.nodes[0].name == nodes[1]):
            if (edge.nodes[1].name == nodes[0] or edge.nodes[1].name == nodes[1]):
                # delete entries from routing tables at either end of the edge, then delete the edge
                del edge.nodes[0].routingtable[edge.nodes[1].name]
                del edge.nodes[1].routingtable[edge.nodes[0].name]
                edge.nodes[0].edges.remove(edge)
                edge.nodes[1].edges.remove(edge)
                del edge
                print(" Link deleted.")
                print(" Press enter to advance.")
                adv = input(" >> ")
                print(" Advancing...")
                return
    print(" Could not find specified link.")
    print(" Press enter to advance.")
    adv = input(" >> ")
    print(" Advancing...")
    return

# trace a path between two endpoints by checking successive routing tables
def view(graph):
    nodes = graph['nodes']
    edges = graph['edges']

    print()
    print(" View route between which nodes? [Ni Nj]")
    route_nodes = input(" >> ").split()
    
    start = None
    for node in nodes:
        if node.name == route_nodes[0]:
            start = node
            break;

    if (route_nodes[1] not in start.routingtable):
        print(" Route not yet known.")
        print(" Press enter to advance.")
        adv = input (" >> ")
        print(" Advancing...")
        return

    print(" " + start.name + " ->", end="")
    dest_reached = False
    while(not dest_reached):
        next_node_name = start.routingtable[route_nodes[1]][1]
        if next_node_name == route_nodes[1]:
            print(" " + next_node_name)
            dest_reached = True
        next_node = None
        for node in nodes:
            if (node.name == next_node_name) :
                print(" " + node.name + " ->", end="")
                start = node    
    print(" Press enter to advance.")
    adv = input(" >> ")     
    print(" Advancing...")
    return

# # # # # # #
# main loop #
# # # # # # #

if __name__ == '__main__':

    print("\n\n")
    print(" - - - - Distance-Vector Routing Simulator - - - - ")
    print(" - - - - - ANC (H) 2020-21 - - - 2283853 - - - - - ")
    print("\n\n")
    print(" Welcome. Enter path to network file:")
    got_networkfile = False

    while(not got_networkfile):
        path = input(" >> ")
        if (os.path.isfile(path)):
            got_networkfile = True
        else:
            print(" Could not find file. Please check path and try again.")

    graph = new_graph_from_file(path)
    print()
    print(" Success! Network loaded.")
    print()

    print(" Simulation will run until tables converge or the exchange limit is reached.")
    print(" Please enter an exchange limit: ")
    
    got_tmax = False
    while (not got_tmax):
        T_MAX = input(" >> ")
        if (T_MAX.isdigit()):
            T_MAX = int(T_MAX)
            got_tmax = True
        else:
            print(" Please enter an integer value.")

    print()
    print(" Exchange limit set: " + str(T_MAX))
    print()
    print(" Would you like to enable Split Horizon mode? [y/n]")
    got_splith = False
    while (not got_splith):
        y_n = input(" >> ")
        if ((y_n[0] == 'y') or (y_n[0] == 'Y')):
            SPLIT_H = 1
            got_splith = True
        elif ((y_n[0] == 'n') or (y_n[0] == 'N')):
            SPLIT_H = 0
            got_splith = True
        else:
            print(" Enter y or n:")

    print()
    if SPLIT_H:
        print(" Split Horizon enabled.")
        
    initialise(graph)
    print()
    print(" Press enter to begin.")
    go = input(" >> ")
    print("\n")
    print(" <- Beginning Simulation at T=0 (Nodes know immediate neighbours) -> ")
    print() 
    t = 0 
    t = first_step(graph, t)
    prevTable = print_all_tables(graph, t)
    print(" Press enter to advance...")
    adv = input(" >> ")
    converged = False

    if (not SPLIT_H):
        while ((not converged) and t < T_MAX):
        
            t = step(graph, t)
            table = print_all_tables(graph, t)
            if table == prevTable:
                converged = True
            prevTable = table
            
            print(" [C]hange Cost | [D]elete Link | [V]iew route | [Enter] to advance simulation")
            adv = input(" >> ")
            if (adv == 'c' or adv == 'C'):
                change(graph)
            elif (adv == 'd' or adv == 'D'):
                delete(graph)
            elif (adv == 'v' or adv == 'V'):
                view(graph)
            print("\n\n")

    else:
        while ((not converged) and t < T_MAX):
        
            t = sh_step(graph, t)
            table = print_all_tables(graph, t)
            if table == prevTable:
                converged = True
            prevTable = table
            
            print(" [C]hange Cost | [D]elete Link | [V]iew route | [Enter] to advance simulation")
            adv = input(" >> ")
            if (adv == 'c' or adv == 'C'):
                change(graph)
            elif (adv == 'd' or adv == 'D'):
                delete(graph)
            elif (adv == 'v' or adv == 'V'):
                view(graph)
            print("\n\n")

    print(" Tables have converged. Simulation complete. Exiting...")
    quit()

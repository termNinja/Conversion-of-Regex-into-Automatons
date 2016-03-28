import re, os, sys
from Queue import Queue
# -----------------------------------------------------------------------------
class term_colors:
    # Usage: print term_colors.WARNING + "This is a msg" + term_colors.ENDC
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# -----------------------------------------------------------------------------
class xdebug:
    @staticmethod
    def dbg(msg):
        print >> sys.stderr, term_colors.FAIL + str(msg) + term_colors.ENDC

    @staticmethod
    def warn(msg):
        print >> sys.stderr, term_colors.WARNING + str(msg) + term_colors.ENDC

    @staticmethod
    def info(msg): 
        print >> sys.stderr, term_colors.OKBLUE + str(msg) + term_colors.ENDC

    @staticmethod
    def fine(msg):
        print >> sys.stderr, term_colors.OKGREEN + str(msg) + term_colors.ENDC

# -----------------------------------------------------------------------------
# VERY IMPORTANT:
# -----------------------------------------------------------------------------
# I changed type of end_node into STRING type, if error occurs BEFORE determinisation,
# make sure to check it wasn't caused by this
# -----------------------------------------------------------------------------
#
class Edge:
    def __init__(self, end_node, weight):
        self.end_node = str(end_node)
        self.weight = str(weight)

    def __str__(self):
        return "(" + str(self.end_node) + ", " + str(self.weight) + ")"
    
    def __eq__(self, other):
        if self.end_node == other.end_node and self.weight == other.weight:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.end_node) ^ hash(self.weight)
# -----------------------------------------------------------------------------
# *****************************************************************************
# -----------------------------------------------------------------------------
class Node:
    def __init__(self, node_val, is_ending):
        self.node_val = int(node_val)
        self.is_ending = bool(is_ending)

    def __str__(self):
        if self.is_ending:
            return "(" + str(self.node_val) + ")" 
        else:
            return str(self.node_val)
# -----------------------------------------------------------------------------
# *****************************************************************************
# -----------------------------------------------------------------------------
# When reading thomhpson's graph from .gv file, we KNOW that
# node 1 is ENDING state, because that's how Thompson's algorithm was implemented.
class Graph:
    def __init__(self, graph_map, graph_name):
        self.graph_map = {}
        self.graph_name = graph_name
        self.ending_nodes = [int(1)]
        for ending_node in self.ending_nodes:
            self.graph_map[ending_node] = []

    def __str__(self):
        output = str(self.graph_name) + "\n-----------------------------\n"
        output += str(self.graph_map)
        return output

    def form_graph_from_gv(self):
        print "reading graph: " + self.graph_name
        f = open("../graphs/" + self.graph_name, "r")
        data = f.read()
        f.close()
        print "Graph data:"
        print data
        print

        # -----------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------
        # Forming graph
        regex = r"\"([a-zA-Z0-9]+)\"\s*->\s*\"([a-zA-Z0-9]+)\"\s*"
        regex += r"(\[label\s*[=]\s*\"([a-zA-Z0-9]+)\"\])?"
        regex = re.compile(regex)
        for iter in regex.finditer(data):
            node_val = iter.group(1)
            into_node = iter.group(2)
            if iter.group(4) == None:
                graph_weight = "eps"
            else:
                graph_weight = iter.group(4)

            # Creating node
            # NOTICE TODO: Node objects aren't actually needed. It can be removed...later though
            if int(node_val) in self.ending_nodes:
                node = Node(node_val, True)
                print "making " + str(node_val) + "into ending node!"
            else:
                node = Node(int(node_val), False)

            # Creating edge
            edge = Edge(into_node, graph_weight)

            print node, edge
            if node.node_val in self.graph_map.keys():
                self.graph_map[node.node_val].append(edge)
            else:
                self.graph_map[node.node_val] = []
                self.graph_map[node.node_val].append(edge)

        ## TODO remove this, i've put it for testing purposes
        # self.export_as_gv()
        # self.export_as_pdf(2)
        self.elim_eps()
        self.determinize()
        # -----------------------------------------------------------------------------------------

    def export_as_gv(self): 
        output_text = []
        output_text.append("digraph finite_state_machine {\n")
        output_text.append("\trankdir=LR;\n")
        output_text.append("\tsize=\"8,5\"\n")
        output_text.append("\tnode [shape = doublecircle]; ")
        for node in self.ending_nodes:
            output_text.append(str(node))
            output_text.append(",")

        output_text[-1] = ";\n"
        output_text.append("\tnode [shape = circle];\n")
        
        # lets fill in the elements
        nodes = self.graph_map.keys()
        for node in nodes:
            edges = self.graph_map[node]
            for edge in edges:
                output_text.append("\t\"" + str(node) + "\" -> \"" + str(edge.end_node) + "\"")
                # check if it was epsilon
                if edge.weight != "eps":
                    output_text.append(" [label=\"" + str(edge.weight) + "\"]")
                output_text.append("\n")

        output_text.append("}")
        
        # writing into file
        f = open("tester.gv", "w")
        f.write("".join(output_text))
        f.close()

    # Export graph structure as pdf
    # command is:
    # dot -Tpdf ../../graphs/source_file.gv -o ../../graphs/output.pdf
    def export_as_pdf(self, step):
        graph_id = self.graph_name.split("_")[0]
        if step == 1:
            algo = "thompson"
        elif step == 2:
            algo = "elimeps"
        elif step == 3:
            algo = "determ"
        elif step == 4:
            algo = "minim"
        else:
            print "error in export_as_pdf function, wrong step argument (allowed 1, 2, 3, 4), given " + str(step)
            sys.exit(1) 

        output_name = graph_id + "_" + str(step) + "_" + algo + ".pdf"
        os.system("dot -Tpdf tester.gv -o output.pdf")
        return 1


    def elim_eps(self):
        print
        print "starting eps elimination:"

        new_map = {0: []}
        new_ending_nodes = []
        visited_nodes = {0: False}

        visited = {}
        for node in self.graph_map.keys():
            visited[node] = {}
            for tmp_node in self.graph_map.keys():
                visited[node][tmp_node] = False

        self.solve_eps_prob(0, 0, new_map, visited, new_ending_nodes)

        self.graph_map = new_map
        self.ending_nodes = new_ending_nodes
        self.export_as_gv()
        self.export_as_pdf(2)
        print "Exported as .gv and .pdf"
        print
    # -------------------------------------------------------------------------
    def solve_eps_prob(self, root_node, current_node, new_map, visited, ending_nodes):
        visited[root_node][current_node] = True
        
        if current_node in self.ending_nodes:
            ending_nodes.append(root_node)     
            return
        
        for adj in self.graph_map[current_node]:
            if adj.weight == "eps" and not visited[root_node][int(adj.end_node)]:
                self.solve_eps_prob(root_node, int(adj.end_node), new_map, visited, ending_nodes)
            elif adj.weight == "eps":
                return
            else:
                if not root_node in new_map.keys():
                    new_map[root_node] = []
                new_map[root_node].append(adj)
                if not visited[root_node][int(adj.end_node)]:
                    self.solve_eps_prob(int(adj.end_node), int(adj.end_node), new_map, visited, ending_nodes)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # TODO: Next to work on
    # TODO: -> I got a bit carried away, write this code all over again,
    #   but please, extract into functions next time
    # -------------------------------------------------------------------------
    def determinize(self):
        # we switch to string keys because of new states
        queue = Queue()            # queue.get() queue.put(item)
        queue.put("0")             # 0 is always the starting node
        new_map = {}
        new_map["0"] = set()

        while queue.qsize() > 0:
            print
            print "----------------------------------------------------------"
            xdebug.info("Queue state: " + str([item for item in queue.queue]))
            print "----------------------------------------------------------"

            current_node = queue.get()
            xdebug.info("Took " + str(current_node) + " from queue.")

            # find all adjacent vertices
            # gives something like: "1,2,3"

            # gives a hash map like:
            # str(a) -> set(int(1), ...)  str(b) -> set(int(5), int(6), int(7))
            xdebug.info("Calling find_adjacent_nodes with " + str(current_node))
            adjacent_nodes = self.find_adjacent_nodes(current_node)
            xdebug.info("Adjacent nodes: " + str(adjacent_nodes))

            # update a map row if required for new deterministic nodes
            self.update_new_map_row(current_node, adjacent_nodes, new_map, queue)
                    
        xdebug.fine("Determinized graph:")
        for key in new_map.keys():
            print str(key) + "->"
            for elem in new_map[key]:
                print "---->" + str(elem)

        self.convert_into_object_map(new_map)
        self.export_as_gv()
        self.export_as_pdf(3)

        return 1

    # ----------------------------------------------------------------------
    # Used by method: determinize
    # ----------------------------------------------------------------------
    def update_new_map_row(self, current_node, adjacent_nodes, new_map, queue): 
        # For each weight in array
        for weight in adjacent_nodes.keys():
            # --------------------------------------------------------------
            # We iterate over set of ints and form a string
            # --------------------------------------------------------------
            new_node = []
            new_edges = []
            for elem in adjacent_nodes[weight]:
                # forming a string
                new_node.append(str(elem))
                new_node.append(",")
            new_node = "".join(new_node)[0:-1]  # cut , at the end
            xdebug.info("formed string: " + new_node)

                ## forming edge if required after loop
                # xdebug.warn("elem: " + str(elem))
                # if elem in self.graph_map:
                    # xdebug.dbg("YES")
                    # for edge in self.graph_map[elem]:
                        # new_edges.append(edge.end_node)
                # xdebug.dbg("new_edges: " + str(new_edges)) 

            # --------------------------------------------------------------
            elem = self.convert_node_list_to_string(adjacent_nodes[weight])
            xdebug.info("result from [a] -> str: " + str(elem))
            xdebug.info("type(" + str(elem) + " is " + str(type(elem)))
            # new_map[current_node] = elem

            if not current_node in new_map:
                new_map[current_node] = set()
            new_map[current_node].add((weight, elem))




            ## now we check if new_node is in new_map.keys(),
            ## if so, we ignore it, if not, we add it into queue and update
            ## it's adjacent nodes
            print type(new_node)
            if not new_node in new_map.keys():
                ## adding into queue
                xdebug.info("adding into queue: " + str(new_node))
                queue.put(new_node)
                ## updating
                # new_map[new_node] = []

    # ----------------------------------------------------------------------
    # [1, 2, 3] => "1,2,3"
    # ----------------------------------------------------------------------
    def convert_node_list_to_string(self, nodelist):
        print
        xdebug.dbg("Converting " + str(nodelist) + " into string")
        res = []
        for elem in nodelist:
            res.append(str(elem))
            res.append(",")
        res = "".join(res)[0:-1]  # cut , at the end
        xdebug.dbg("Done conversion: " + str(res))
        print
        return res
    # ----------------------------------------------------------------------
    # "1,2,3" => [1, 2, 3]
    # ----------------------------------------------------------------------
    def convert_string_nodes_to_list(self, nodestr):
        if nodestr[-1] == ",":
            nodestr = nodestr.split(",")[0:-1]
        else:
            nodestr = nodestr.split(",")
        return nodestr
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # Used by method: determinize
    # ----------------------------------------------------------------------
    def find_adjacent_nodes(self, current_node):
        xdebug.info("Entered find_adjacent_nodes with current_node = " + str(current_node))
        # current node can be something like: "0,3,5"
        adjacent_nodes = {}     # example: a -> "1,2,3" b -> "3,4,5"

        # [1, 2, 3] -> "1,2,3"
        xdebug.dbg("calling conversion for: " + str(current_node))
        current_node = self.convert_string_nodes_to_list(current_node)
        xdebug.info("updated current_node, current_node = " + str(current_node))

        # ['0', '3', '5] -> '0',   '3',  '5'
        xdebug.dbg("current node: " + str(current_node))
        for node in current_node:
            xdebug.dbg("node: " + str(node))
            if int(node) in self.graph_map.keys():
                for edge in self.graph_map[int(node)]:
                    if edge.weight not in adjacent_nodes:
                        adjacent_nodes[edge.weight] = set()
                    adjacent_nodes[edge.weight].add(int(edge.end_node))

        return adjacent_nodes

    # ----------------------------------------------------------------------
    # TODO
    def convert_into_object_map(self, new_map):
        # We need to rename 
        xdebug.info("old ending nodes: " + str(self.ending_nodes))
        ending_nodes = []        
        self.graph_map.clear()
        for node in new_map.keys():
            # updating object map
            self.graph_map[node] = []
            for edge in new_map[node]:
                # ('a', '1,2,3')
                self.graph_map[node].append(Edge(edge[1], edge[0]))

            # finding ending nodes
            nodes = self.convert_string_nodes_to_list(node)
            xdebug.info("str->lst: nodes: " + str(nodes))
            for xnode in nodes:
                if int(xnode) in self.ending_nodes:
                    ending_nodes.append(node)
                    break
            self.ending_nodes = ending_nodes

        print
        self.show_graph()
    # ----------------------------------------------------------------------

    def show_graph(self):
        for node in self.graph_map.keys():
            print node
            for edge in self.graph_map[node]:
                print " -> " + str(edge)

    def break_info_nodes(nodes):
        return nodes.split(",")[0:-1]

    def minimize():
        return 1
# -----------------------------------------------------------------------------






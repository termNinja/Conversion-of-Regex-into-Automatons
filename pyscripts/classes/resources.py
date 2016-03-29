import re, os, sys
from Queue import Queue
# -----------------------------------------------------------------------------
class term_colors:
    """ Usage: print term_colors.WARNING + "This is a msg" + term_colors.ENDC """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# -----------------------------------------------------------------------------
class xlogger:
    @staticmethod
    def dbg(msg):
        """ Prints a debugging msg onto stderr """
        print >> sys.stderr, term_colors.FAIL + str(msg) + term_colors.ENDC

    @staticmethod
    def warn(msg):
        """ Prints a warning msg onto stderr """
        print >> sys.stderr, term_colors.WARNING + str(msg) + term_colors.ENDC

    @staticmethod
    def info(msg): 
        """ Prints an info msg onto stderr """
        print >> sys.stderr, term_colors.OKBLUE + str(msg) + term_colors.ENDC

    @staticmethod
    def fine(msg):
        """ Prints an ok msg onto stderr """
        print >> sys.stderr, term_colors.OKGREEN + str(msg) + term_colors.ENDC
# -----------------------------------------------------------------------------
# handy macro
class algo_step:
    thompson = "_01_thompson"
    elimeps = "_02_elimeps"
    determ = "_03_determ"
    minim = "_04_minim"
# -----------------------------------------------------------------------------
# VERY IMPORTANT:
# -----------------------------------------------------------------------------
# I changed type of end_node into STRING type, if error occurs BEFORE determinisation,
# make sure to check it wasn't caused by this
# -----------------------------------------------------------------------------
class Edge:
    def __init__(self, end_node, weight):
        """ 
        Initializes edge object. 
        end_node    -> string
        weight      -> string 
        """
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
class Node:
    def __init__(self, node_val, is_ending):
        self.node_val = int(node_val)
        self.is_ending = bool(is_ending)

    def __str__(self):
        if self.is_ending:
            return "(" + str(self.node_val) + ")" 
        else:
            return str(self.node_val)
# When reading thomhpson's graph from .gv file, we KNOW that
# node 1 is ENDING state, because that's how Thompson's algorithm was implemented
# for this particular project.
# -----------------------------------------------------------------------------
class Graph:
    # -------------------------------------------------------------------------
    def __init__(self, graph_map, graph_name):
        self.graph_map = {}
        self.graph_name = graph_name
        self.ending_nodes = [int(1)]
        for ending_node in self.ending_nodes:
            self.graph_map[ending_node] = []

    # -------------------------------------------------------------------------
    def __str__(self):
        output = str(self.graph_name) + "\n-----------------------------\n"
        output += str(self.graph_map)
        return output

    # -------------------------------------------------------------------------
    def form_graph_from_gv(self):
        """
        Reads the .gv file that represent the graph
        and maps it onto Graph object.
        """
        print "reading graph: " + self.graph_name
        # algo_step.thompson because python continues where C stopped with work
        #  => Thompson algorithm has been performed
        f = open("../graphs/" + self.graph_name + algo_step.thompson + ".gv", "r")
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
        self.elim_eps()
        self.determinize()

    # -------------------------------------------------------------------------
    def export_as_gv(self, algstep): 
        """
        Maps Graph object as gv file.
        """
        output_text = []
        output_text.append("digraph finite_state_machine {\n")
        output_text.append("\trankdir=LR;\n")
        output_text.append("\tsize=\"8,5\"\n")
        output_text.append("\tnode [shape = doublecircle]; ")
        for node in self.ending_nodes:
            output_text.append("\"")
            output_text.append(str(node))
            output_text.append("\"")
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
        f = open(self.graph_name + str(algstep) + ".gv", "w")
        # f = open("tester.gv", "w")
        f.write("".join(output_text))
        f.close()

    # -------------------------------------------------------------------------
    # Export graph structure as pdf
    # command is:
    # dot -Tpdf ../../graphs/source_file.gv -o ../../graphs/output.pdf
    def export_as_pdf(self, algstep):
        """
        Draw a vector image of graph that it reads
        from gv file (make sure you have it created).
        Uses dot from graphviz to acomplish this amazing task.
        """
        graph_id = self.graph_name.split("_")[0]

        output_name = self.graph_name + str(algstep)
        os.system("dot -Tpdf " + output_name + ".gv -o " + output_name + ".pdf")
        return 1


    # -------------------------------------------------------------------------
    def elim_eps(self):
        """
        Performs algorithm that eliminates epsilon edges in graph.
        Wrapper for solve_eps_prob.
        """
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
        self.export_as_gv(algo_step.elimeps)
        self.export_as_pdf(algo_step.elimeps)
        xlogger.fine("Exported: " + self.graph_name + algo_step.elimeps + ".gv")
        xlogger.fine("Exported: " + self.graph_name + algo_step.elimeps + ".pdf")
    # -------------------------------------------------------------------------
    def solve_eps_prob(self, root_node, current_node, new_map, visited, ending_nodes):
        """
        Recursive method that peforms a DFS search and eliminates epsilon edges.
        """
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
    def determinize(self):
        """
        Performs the determinisation algorithm.
        """
        # we switch to string keys because of new states
        queue = Queue()            # queue.get() queue.put(item)
        queue.put("0")             # 0 is always the starting node
        new_map = {}
        new_map["0"] = set()

        while queue.qsize() > 0:
            print
            print "----------------------------------------------------------"
            xlogger.info("Queue state: " + str([item for item in queue.queue]))
            print "----------------------------------------------------------"

            current_node = queue.get()
            xlogger.info("Took " + str(current_node) + " from queue.")

            # find all adjacent vertices
            # gives something like: "1,2,3"

            # gives a hash map like:
            # str(a) -> set(int(1), ...)  str(b) -> set(int(5), int(6), int(7))
            xlogger.info("Calling find_adjacent_nodes with " + str(current_node))
            adjacent_nodes = self.find_adjacent_nodes(current_node)
            xlogger.info("Adjacent nodes: " + str(adjacent_nodes))

            # update a map row if required for new deterministic nodes
            self.update_new_map_row(current_node, adjacent_nodes, new_map, queue)
                    
        xlogger.fine("Determinized graph:")
        for key in new_map.keys():
            print str(key) + "->"
            for elem in new_map[key]:
                print "---->" + str(elem)

        self.convert_into_object_map(new_map)
        self.export_as_gv(algo_step.determ)
        self.export_as_pdf(algo_step.determ)

    # ----------------------------------------------------------------------
    # Used by method: determinize
    # ----------------------------------------------------------------------
    def update_new_map_row(self, current_node, adjacent_nodes, new_map, queue): 
        """
        Used as a helper function in determinsation algorithm.
        It initialises and transforms some things in main graph object.
        """
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
            xlogger.info("formed string: " + new_node)

            # --------------------------------------------------------------
            elem = self.list_to_string(adjacent_nodes[weight])
            xlogger.info("result from [a] -> str: " + str(elem))
            xlogger.info("type(" + str(elem) + " is " + str(type(elem)))
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
                xlogger.info("adding into queue: " + str(new_node))
                queue.put(new_node)
                ## updating
                # new_map[new_node] = []

    # ----------------------------------------------------------------------
    def list_to_string(self, nodelist):
        """
        Converts a list of elements onto string with character ',' as separator
        [1, 2, 3] => "1,2,3"
        """
        print
        xlogger.dbg("Converting " + str(nodelist) + " into string")
        res = []
        for elem in nodelist:
            res.append(str(elem))
            res.append(",")
        res = "".join(res)[0:-1]  # cut , at the end
        xlogger.dbg("Done conversion: " + str(res))
        print
        return res

    # ----------------------------------------------------------------------
    def string_to_list(self, nodestr):
        """
        Converts a , separated string into a list of strings.
        "1,2,3" => [1, 2, 3]
        "ab,cd" => ["ab", "cd"]
        """
        if nodestr[-1] == ",":
            nodestr = nodestr.split(",")[0:-1]
        else:
            nodestr = nodestr.split(",")
        return nodestr

    # ----------------------------------------------------------------------
    # Used by method: determinize
    # ----------------------------------------------------------------------
    def find_adjacent_nodes(self, current_node):
        """
        Used as a helper function in determinsation algorithm.
        It finds adjacent nodes for a given node. 
        """
        xlogger.info("Entered find_adjacent_nodes with current_node = " + str(current_node))
        # current node can be something like: "0,3,5"
        adjacent_nodes = {}     # example: a -> "1,2,3" b -> "3,4,5"

        # [1, 2, 3] -> "1,2,3"
        xlogger.dbg("calling conversion for: " + str(current_node))
        current_node = self.string_to_list(current_node)
        xlogger.info("updated current_node, current_node = " + str(current_node))

        # ['0', '3', '5] -> '0',   '3',  '5'
        xlogger.dbg("current node: " + str(current_node))
        for node in current_node:
            xlogger.dbg("node: " + str(node))
            if int(node) in self.graph_map.keys():
                for edge in self.graph_map[int(node)]:
                    if edge.weight not in adjacent_nodes:
                        adjacent_nodes[edge.weight] = set()
                    adjacent_nodes[edge.weight].add(int(edge.end_node))

        return adjacent_nodes

    # ----------------------------------------------------------------------
    def convert_into_object_map(self, new_map):
        """
        Converts a temp hash map created during determinisation algorithm
        onto a main graph map used for storing a graph.
        It also sets ending nodes.
        """
        ending_nodes = []        
        self.graph_map.clear()
        graph_nodes = new_map.keys()
        for node in graph_nodes:
            self.graph_map[node] = []
            for edge in new_map[node]:
                # ('1,2,3', 'a')
                self.graph_map[node].append(Edge(edge[1], edge[0]))
                if not edge[1] in graph_nodes:
                    self.graph_map[edge[1]] = []

        # finding ending nodes
        # node => "11,3" for example
        for node in self.graph_map.keys():
            nodez = self.string_to_list(node)
            for elem in nodez:
                xlogger.dbg("elem: " + str(elem))
                if int(elem) in self.ending_nodes:
                    ending_nodes.append(str(node))
                    break
        

        xlogger.info("old ending nodes: " + str(self.ending_nodes))
        xlogger.info("new ending nodes: " + str(ending_nodes))

        # adding nodes that don't have an output edge
        # currently, they are implicitly given in our graph structure
        # they appear only in edges in map (example: 3 has no output edge)
        # For example, "1,2" -> ("ab", "3")
        # Lets find nodes like this and add them into main map
        for node in graph_nodes:
            for edge in new_map[node]:
                if not edge[1] in graph_nodes:
                    self.graph_map[edge[1]] = []
                
        

        # Finally, we form the ending nodes in Graph object
        self.ending_nodes = ending_nodes

        print
        self.show_graph()
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def show_graph(self):
        """
        Prints graph to stdout.
        """
        for node in self.graph_map.keys():
            print node
            for edge in self.graph_map[node]:
                print " -> " + str(edge)

    # ----------------------------------------------------------------------
    # TODO: Nexto to implement
    # ----------------------------------------------------------------------
    def minimize():
        """
        Performs minimization algorithm.
        """
        return 1
# -----------------------------------------------------------------------------

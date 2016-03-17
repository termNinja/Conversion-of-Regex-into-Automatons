import re, os, sys
# -----------------------------------------------------------------------------
class Edge:
    def __init__(self, end_node, weight):
        self.end_node = int(end_node)
        self.weight = str(weight)

    def __str__(self):
        return "(" + str(self.end_node) + ", " + str(self.weight) + ")"
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


    # -------------------------------------------------------------------------
    # TODO: Next to work on
    # -------------------------------------------------------------------------
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
    # -------------------------------------------------------------------------
    def solve_eps_prob(self, root_node, current_node, new_map, visited, ending_nodes):
        visited[root_node][current_node] = True
        
        if current_node in self.ending_nodes:
            ending_nodes.append(root_node)     
            return
        
        for adj in self.graph_map[current_node]:
            if adj.weight == "eps" and not visited[root_node][adj.end_node]:
                self.solve_eps_prob(root_node, adj.end_node, new_map, visited, ending_nodes)
            elif adj.weight == "eps":
                return
            else:
                if not root_node in new_map.keys():
                    new_map[root_node] = []
                new_map[root_node].append(adj)
                if not visited[root_node][adj.end_node]:
                    self.solve_eps_prob(adj.end_node, adj.end_node, new_map, visited, ending_nodes)
    # -------------------------------------------------------------------------

    def determinize(self):
        # we switch to string keys because of new states
        new_graph_map = {}
        for old_key in self.graph_map.keys():
            new_graph_map[str(old_key)] = self.graph_map[old_key]

        determinized_automaton = {} 
        edge_weight_map = {}

        # sex begins here

        return 1

    def minimize():
        return 1
# -----------------------------------------------------------------------------

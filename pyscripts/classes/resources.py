import re, os
# -----------------------------------------------------------------------------
class Edge:
    def __init__(self, end_node, weight):
        self.end_node = end_node
        self.weight = weight

    def __str__(self):
        return "(" + str(self.end_node) + ", " + str(self.weight) + ")"
# -----------------------------------------------------------------------------
# *****************************************************************************
# -----------------------------------------------------------------------------
class Node:
    def __init__(self, node_val, is_ending):
        self.node_val = node_val
        self.is_ending = is_ending

    def __str__(self):
        if self.is_ending:
            return "(" + str(self.node_val) + ")"
        else:
            return str(self.node_val)
# -----------------------------------------------------------------------------
# *****************************************************************************
# -----------------------------------------------------------------------------
# When reading thomhpson's graph from .gv file, we KNOW that
# node 1 is ENDING state. Cast it into such by YOURSELF.
class Graph:
    def __init__(self, graph_map, graph_name):
        self.graph_map = {}
        self.graph_name = graph_name
        self.ending_nodes = []

    def __str__(self):
        output = str(self.graph_name) + "\n-----------------------------\n"
        output += str(self.graph_map)
        return output

    def form_graph_from_gv(self):
        f = open("../graphs/" + self.graph_name, "r")
        data = f.read()
        f.close()
        print data


        # -----------------------------------------------------------------------------------------
        # adding only 1 because that's always the output of THompson's algorithm (the way I implemented it)
        self.ending_nodes.append(int(1))

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
                node = Node(node_val, False)

            # Creating edge
            edge = Edge(into_node, graph_weight)

            ## TODO: Form graph from parsed data...
            ## TODO Fix this baboon later...damn dictionaries
            print node, edge
            if node.node_val in self.graph_map.keys():
#                self.graph_map[node.node_val].append(edge)
                self.graph_map[node.node_val].append(edge)
            else:
                self.graph_map[node.node_val] = ([])
                self.graph_map[node.node_val].append(edge)
#            self.graph_map.append(node.node_val : edge)

        ## TODO remove this, i've put it for testing purposes
        self.export_as_gv()
        # -----------------------------------------------------------------------------------------

    def export_as_gv(self):
        output_text = []
        output_text.append("digraph finite state machine {\n")
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

    # Export graph strcutre as pdf
    # command is:
    # dot -Tpdf ../../graphs/source_file.gv -o ../../graphs/output.pdf
    def export_as_pdf():
        # os.system("...")
        return 1

    def elim_eps():
        return 1

    def determinize():
        return 1

    def minimize():
        return 1
# -----------------------------------------------------------------------------

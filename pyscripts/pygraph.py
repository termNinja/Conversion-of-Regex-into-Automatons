#!/usr/bin/python2
# -------------------------------------------------------------------------------------------------
import sys
from classes.resources import Node, Graph, Edge
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# This script is called from main C program as an external library.
# It behaves differently based of arguments C program calls it with.
# -------------------------------------------------------------------------------------------------
graph_name = sys.argv[1]
graph = Graph({}, graph_name)
graph.form_graph_from_gv()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Graph name is something like:
#   0_01_thompson.gv
#   * 0         -> graph id
#   * 01        -> step of conversion
#   * thompson  -> conversion name
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# if method == "thompson":
    # print "performing thompson on" + graph_name
    # graph = Graph({}, graph_name)
    # graph.form_graph_from_gv()

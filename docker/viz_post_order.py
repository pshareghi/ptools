#!/usr/bin/env python

################################################
# Given the output of
# $ docker images --viz
# and sha of a node in the tree, this script lists its subtree by doing a
# post order traversal. You can then feed the result to
# docker rmi to remove all the subtree (assuming no containers are
# running).
# 
# Example:
# $ docker images --viz | ./docker/viz_post_order.py 19f5e5f88586 | xargs \
#     docker rmi --no-prune
# 
# Author: Pooya Shareghi <shareghi@gmail.com>
################################################

import sys

def _valid_line(line):
    line = line.replace(" ", "")
    if line.startswith('"') and "->" in line:
        return True
    return False

def _clean_line(line):
    line = line.replace(" ", "")
    line = line.replace("\"", "")
    line = line.replace("\n", "")
    return line

def _tokenize(line):
    tokens = line.split("->")
    if len(tokens) != 2:
        print "# of tokens not equal to 2!!"
        print "line: " + line
        print "tokens: " + tokens
        sys.exit(1)
    return tokens

def _build_graph():
    adjacency = dict()
    for line in sys.stdin.readlines():
        if _valid_line(line):
            line = _clean_line(line)
            tokens = _tokenize(line)
            fromNode = tokens[0]
            toNode = tokens[1]
            adjacency.setdefault(fromNode, []).append(toNode)
    return adjacency

def _post_order_traversal(root, adjacency):
    traversal = []
    if root in adjacency:
        for child in adjacency[root]:
            child_subtree = _post_order_traversal(child, adjacency)
            traversal.extend(child_subtree)
    traversal.append(root)
    return traversal
        
def _print_list(nodes):
    for node in nodes:
        print "%s " % node

def main(argv):
    subtree_root = argv[1]
    adjacency = _build_graph()
    traversal = _post_order_traversal(subtree_root, adjacency)
    _print_list(traversal)

main(sys.argv)

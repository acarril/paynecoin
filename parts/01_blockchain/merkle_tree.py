import math
from utils import compute_hash
from typing import List

class Node:
    def __init__(
        self,
        value:int,
        left_child=None,
        right_child=None
    ) -> None:
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

def compute_tree_depth(n_leaves:int) -> int:
    return math.ceil(math.log2(n_leaves))

def fill_leafs(leafs:list):
    n_leafs = len(leafs)
    if math.log2(n_leafs).is_integer():
        return leafs
    n_nodes = 2**compute_tree_depth(n_leafs)
    if n_leafs % 2 == 0:
        for i in range(n_leafs, n_nodes, 2):
            leafs = leafs + [leafs[-2], leafs[-1]]
    else:
        for i in range(n_leafs, n_nodes):
            leafs.append(leafs[-1])
    return leafs

def build_merkle_tree(node_data: List[str]) -> Node:
    complete_set = fill_leafs(node_data)
    old_set_of_nodes = [Node(compute_hash(data)) for data in complete_set]
    tree_depth = compute_tree_depth(len(old_set_of_nodes))

    for i in range(0, tree_depth):
        num_nodes = 2**(tree_depth-i)
        new_set_of_nodes = []
        for j in range(0, num_nodes, 2):
            child_node_0 = old_set_of_nodes[j]
            child_node_1 = old_set_of_nodes[j+1]
            new_node = Node(
                value=compute_hash(f"{child_node_0.value}{child_node_1.value}"),
                left_child=child_node_0,
                right_child=child_node_1
            )
            new_set_of_nodes.append(new_node)
        old_set_of_nodes = new_set_of_nodes
    return new_set_of_nodes[0]
import sys 
sys.path.append('.')

import unittest
from merkle_tree import build_merkle_tree
from utils import compute_hash

class TestMerkleTree(unittest.TestCase):

    def test_build_merkle_tree(self):
        l1 = "blabla data 0"
        l2 = "blabla data 1"
        merkle_tree = build_merkle_tree([l1, l2])
        self.assertEqual(
            merkle_tree.left_child.value,
            compute_hash(l1)
        )
        self.assertEqual(
            merkle_tree.right_child.value,
            compute_hash(l2)
        )
        self.assertEqual(
            merkle_tree.value,
            compute_hash(compute_hash(l1) + compute_hash(l2))
        )

if __name__ == '__main__':
    unittest.main()
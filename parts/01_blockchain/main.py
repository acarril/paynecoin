from block import Block

block0 = Block({'sender': 'Alvaro', 'recipient': 'Bob', 'amount': 42})
block1 = Block({'sender': 'Bob', 'recipient': 'Alvaro', 'amount': 10}, block0, '12am')
block2 = Block({}, block1)



# Merkle


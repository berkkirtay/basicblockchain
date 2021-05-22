from blockchain import *
from p2pserver import *
import socket
import time

address = socket.gethostbyname(socket.gethostname()) # '127.0.0.1'
block1 = blockchain(2,0.2) # Mining Difficulty and reward
newNetwork = p2p(block1, address, 8000)

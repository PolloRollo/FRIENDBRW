import unittest
import math
import networkx as nx
from main import friendbrw_retrace, friendbrw_cycle, new_friendbrw


class FriendbrwTestCase(unittest.TestCase):

    def setUp(self):
        self.G = nx.DiGraph()
        self.H = nx.DiGraph()
        triangle = [(1, 2), (2, 1), (2, 3), (3, 2), (3, 1), (1, 3)]
        self.G.add_edges_from(triangle)
        self.H.add_edges_from(triangle)
        self.H.add_edges_from([(1, 4), (2, 4), (4, 3), (4, 5)])

    def test_frienbrw_01(self):
        friendbrw_retrace(G=self.G)
        assert self.G[1][2]['friendbrw'] == 2.01

    def test_frienbrw_cycle_01(self):
        friendbrw_cycle(G=self.G)
        assert self.G[1][2]['friendbrw_cycle'] == 6.01

    def test_new_friendbrw_01(self):
        new_friendbrw(G=self.G)
        assert self.G[1][2]['friendbrw_cycle'] == 6.01

    def test_frienbrw_02(self):
        friendbrw_retrace(G=self.H)
        assert self.H[1][2]['friendbrw'] == 2.01

    def test_frienbrw_cycle_02(self):
        friendbrw_cycle(G=self.H)
        assert self.H[1][2]['friendbrw_cycle'] == 6.01

    def test_new_friendbrw_02(self):
        new_friendbrw(G=self.H)
        assert self.H[1][2]['friendbrw_cycle'] == 6.01
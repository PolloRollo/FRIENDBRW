import unittest
import math
import networkx as nx
from main import friendbrw_retrace, friendbrw_cycle, new_friendbrw


class FriendbrwTestCase(unittest.TestCase):

    def setUp(self):
        self.G = nx.DiGraph()
        self.H = nx.DiGraph()
        triangle = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)]
        self.G.add_edges_from(triangle)
        self.H.add_edges_from(triangle)
        self.H.add_edges_from([(0, 3), (1, 3), (3, 2), (3, 4)])

    # Test rnbrw random walk
    def test_frienbrw_01(self):
        friendbrw_retrace(G=self.G)
        assert self.G[1][2]['friendbrw'] == 2.01

    def test_frienbrw_cycle_01(self):
        friendbrw_cycle(G=self.G)
        assert self.G[1][2]['friendbrw_cycle'] == 6.01

    def test_new_friendbrw_01(self):
        new_friendbrw(G=self.G)
        assert self.G[1][2]['friendbrw_cycle'] == 6.01

    # Test subgraph
    def test_frienbrw_02(self):
        friendbrw_retrace(G=self.H)
        assert self.H[1][2]['friendbrw'] == 2.01

    def test_frienbrw_cycle_02(self):
        friendbrw_cycle(G=self.H)
        assert self.H[1][2]['friendbrw_cycle'] == 6.01

    def test_new_friendbrw_02(self):
        new_friendbrw(G=self.H)
        assert self.H[1][2]['friendbrw_cycle'] == 6.01

    # Test weighted parameter
    def test_frienbrw_03(self):
        nx.set_edge_attributes(self.G, values=1, name='weight')
        friendbrw_retrace(G=self.G, weighted=True, initial=.01)
        assert self.G[1][2]['friendbrw'] == 4.02

    def test_frienbrw_cycle_03(self):
        nx.set_edge_attributes(self.G, values=1, name='weight')
        friendbrw_cycle(G=self.G, weighted=True, initial=.01)
        assert self.G[1][2]['friendbrw_cycle'] == 12.02

    def test_new_friendbrw_03(self):
        nx.set_edge_attributes(self.G, values=1, name='weight')
        new_friendbrw(G=self.G, weighted='weight', initial=.01)
        assert self.G[1][2]['friendbrw_cycle'] == 12.02

    # Test initial weight
    def test_frienbrw_04(self):
        friendbrw_retrace(G=self.H, initial=.51)
        assert self.H[1][2]['friendbrw'] == 2.51

    def test_frienbrw_cycle_04(self):
        friendbrw_cycle(G=self.H, initial=.51)
        assert self.H[1][2]['friendbrw_cycle'] == 6.51

    def test_new_friendbrw_04(self):
        new_friendbrw(G=self.H, initial=.51)
        assert self.H[1][2]['friendbrw_cycle'] == 6.51

    # Test different weights
    def test_frienbrw_05(self):
        nx.set_edge_attributes(self.G, values=1, name='weight')
        self.G[1][2]['weight'] = 2
        self.G[2][1]['weight'] = 1
        friendbrw_retrace(G=self.G, weighted=True, initial=.01)
        assert round(self.G[1][2]['friendbrw'], 10) == 6.03

    def test_frienbrw_cycle_05(self):
        nx.set_edge_attributes(self.G, values=1, name='weight')
        self.G[1][2]['weight'] = 2
        self.G[2][1]['weight'] = 1
        friendbrw_cycle(G=self.G, weighted=True, initial=.01)
        assert round(self.G[1][2]['friendbrw_cycle'], 10) == 18.03

    def test_new_friendbrw_05(self):
        nx.set_edge_attributes(self.G, values=1, name='weight')
        self.G[1][2]['weight'] = 2
        self.G[2][1]['weight'] = 1
        new_friendbrw(G=self.G, weighted='weight', initial=.01)
        assert round(self.G[1][2]['friendbrw_cycle'], 10) == 18.03

    # Test more iterations
    def test_frienbrw_06(self):
        friendbrw_retrace(G=self.H, t=4)
        assert round(self.H[1][2]['friendbrw'], 10) == 8.01

    def test_frienbrw_cycle_06(self):
        friendbrw_cycle(G=self.H, t=4)
        assert round(self.H[1][2]['friendbrw_cycle'], 10) == 24.01

    def test_new_friendbrw_06(self):
        new_friendbrw(G=self.H, t=4)
        assert round(self.H[1][2]['friendbrw_cycle'], 10) == 24.01
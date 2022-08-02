import numpy as np
import networkx as nx
import random


def random_walk_until_retrace(G, head, tail):
    """
    Beginning with input graph G, we choose a random edge in G.
    Since G is undirected, we randomly decide a head and tail for the edge.
    We then randomly walk, without backtracking until we revisit a node
    OR we visit a node with no edges (besides backtracking).
    """
    path = {tail}
    # Random walk until cycle
    while head not in path:
        neighbors = list(G[head])
        neighbors.remove(tail)
        if head in neighbors:
            neighbors.remove(head)
        if len(neighbors) == 0:
            return False, tail, head
        path.add(head)
        head, tail = random.choice(neighbors), head
    # Return retraced edge
    return True, tail, head


def random_walk_until_cycle(G, head, tail):
    """
    Beginning with input graph G, we choose a random edge in G.
    Since G is undirected, we randomly decide a head and tail for the edge.
    We then randomly walk, without backtracking until we revisit a node
    OR we visit a node with no edges (besides backtracking).
    We return the cycle found by the random walk where the retracing edge connects [0] and [-1]
    """
    path = [tail]
    # Random walk until cycle
    while head not in path:
        neighbors = list(G[head])
        neighbors.remove(tail)
        if head in neighbors:
            neighbors.remove(head)
        if len(neighbors) == 0:
            return False, path
        path.append(head)
        head, tail = random.choice(neighbors), head
    # Return statements (retraced edge or cycle list)
    start = path.index(head)
    cycle = path[start:]
    return True, cycle


def rnbrw(G, t=1, weighted=False, initial=0.01):
    # Update the graph edge attributes for each retraced edge found
    i = 0
    nx.set_edge_attributes(G, values=initial, name='rnbrw')
    for trial in range(t):
        for head, tail in G.edges:
            completed_cycle, t, h = random_walk_until_retrace(G, head, tail)
            if completed_cycle:
                G[t][h]['rnbrw'] += 1
            completed_cycle, t, h = random_walk_until_retrace(G, tail, head)
            if completed_cycle:
                G[t][h]['rnbrw'] += 1
    if weighted:
        for source, target in G.edges:
            G[source][target]['rnbrw'] = G[source][target]['rnbrw'] * G[source][target]['external_weight']
    return True


def cycle_rnbrw(G, t=1, weighted=False, initial=0.01):
    # Update the graph edge attributes for each edge found in a cycle
    nx.set_edge_attributes(G, values=initial, name='cycle_rnbrw')
    for trial in range(t):
        for head, tail in G.edges:
            completed, cycle = random_walk_until_cycle(G, head, tail)
            if completed:
                for node in range(len(cycle)):
                    G[cycle[node]][cycle[node-1]]['cycle_rnbrw'] += 1
            completed, cycle = random_walk_until_cycle(G, tail, head)
            if completed:
                for node in range(len(cycle)):
                    G[cycle[node]][cycle[node-1]]['cycle_rnbrw'] += 1
    if weighted:
        for source, target in G.edges:
            G[source][target]['cycle_rnbrw'] = G[source][target]['cycle_rnbrw'] * G[source][target]['external_weight']
    return True


def friendbrw_retrace(G, t=1, weighted=False, initial=0.01):
    unweighted_adj = nx.to_numpy_array(G, weight=None)
    rec_adj = np.multiply(unweighted_adj, unweighted_adj.T)
    if weighted:
        weighted_adj = nx.to_numpy_array(G, weight="weight")
        sum_weights_adj = weighted_adj + weighted_adj.T
        rec_weighted_adj = np.multiply(rec_adj, sum_weights_adj)
        rec_graph = nx.from_numpy_array(rec_weighted_adj, create_using=nx.Graph())
        weights = nx.get_edge_attributes(rec_graph, 'weight')
        nx.set_edge_attributes(rec_graph, weights, name='external_weight')
    else:
        rec_graph = nx.from_numpy_array(rec_adj, create_using=nx.Graph())
    rnbrw(rec_graph, t, weighted, initial)
    rec_weights = nx.get_edge_attributes(rec_graph, 'rnbrw')
    rev_rec_weights = {(n2,n1):rec_weights[(n1,n2)] for n1,n2 in rec_weights}
    nx.set_edge_attributes(G, values=initial, name='friendbrw')
    nx.set_edge_attributes(G, values=rec_weights, name='friendbrw')
    nx.set_edge_attributes(G, values=rev_rec_weights, name='friendbrw')
    return True


def friendbrw_cycle(G, t=1, weighted=False, initial=0.01):
    unweighted_adj = nx.to_numpy_array(G, weight=None)
    rec_adj = np.multiply(unweighted_adj, unweighted_adj.T)
    if weighted:
        weighted_adj = nx.to_numpy_array(G, weight='weight')
        sum_weights_adj = weighted_adj + weighted_adj.T
        rec_weighted_adj = np.multiply(rec_adj, sum_weights_adj)
        rec_graph = nx.from_numpy_array(rec_weighted_adj, create_using=nx.Graph())
        weights = nx.get_edge_attributes(rec_graph, 'weight')
        nx.set_edge_attributes(rec_graph, weights, name='external_weight')
    else:
        rec_graph = nx.from_numpy_array(rec_adj, create_using=nx.Graph())
    cycle_rnbrw(rec_graph, t, weighted, initial)
    rec_weights = nx.get_edge_attributes(rec_graph, 'cycle_rnbrw')
    rev_rec_weights = {(n2,n1): rec_weights[(n1,n2)] for n1,n2 in rec_weights}
    nx.set_edge_attributes(G, values=initial, name='friendbrw_cycle')
    nx.set_edge_attributes(G, values=rec_weights, name='friendbrw_cycle')
    nx.set_edge_attributes(G, values=rev_rec_weights, name='friendbrw_cycle')
    return True


def new_friendbrw(G, t=1, weighted=None, initial=.01):
    """FRIENDBRW is a method which...
    :param G: The number to multiply.
    :type G: networkx digraph

    :param t: The number of random walks * |E|
    :type t: int

    :param weighted: The name of the multiplier attribute
    :type weighted: string

    :param initial: The inclusivity value
    :type initial: float
    """
    nx.set_edge_attributes(G, values=initial, name='friendbrw_cycle')
    rec_graph = nx.Graph()
    # rec_graph is an undirected subgraph of G, composed of all reciprocal edges
    completed_nodes = set()
    for node in G.nodes:
        completed_nodes.add(node)
        for edge in set(set(G.predecessors(node)) & set(G.successors(node))):
            if edge not in completed_nodes:
                rec_graph.add_edge(node, edge)
                if weighted is not None:
                    weightSum = G[node][edge][weighted] + G[edge][node][weighted]
                    rec_graph[node][edge]['external_weight'] = weightSum
    # Apply CycleRNBRW to the reciprocal subgraph of G
    cycle_rnbrw(rec_graph, t, weighted=(weighted is not None), initial=initial)
    # Add the cycle_rnbrw weights to G
    rec_weights = nx.get_edge_attributes(rec_graph, 'cycle_rnbrw')
    nx.set_edge_attributes(G, values=initial, name='friendbrw_cycle')
    for edge, weight in rec_weights.items():
        G[edge[0]][edge[1]]['friendbrw_cycle'] = weight
        G[edge[1]][edge[0]]['friendbrw_cycle'] = weight
    return True


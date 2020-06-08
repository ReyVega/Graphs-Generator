# -*- coding: utf-8 -*-
#
#    Copyright (C) 2010 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Authors:
#   Nima Mohammadi <nima.irt@gmail.com>
#   Aric Hagberg <hagberg@lanl.gov>
#   Mike Trenfield <william.trenfield@utsouthwestern.edu>
"""
Eulerian circuits and graphs.
"""
from itertools import combinations

import networkx as nx
from ..utils import arbitrary_element, not_implemented_for

__all__ = ['is_eulerian', 'eulerian_circuit', 'eulerize',
           'is_semieulerian', 'has_eulerian_path', 'eulerian_path',
           ]


def is_eulerian(G):
    """Returns True if and only if `G` is Eulerian.

    A graph is *Eulerian* if it has an Eulerian circuit. An *Eulerian
    circuit* is a closed walk that includes each edge of a graph exactly
    once.

    Parameters
    ----------
    G : NetworkX graph
       A graph, either directed or undirected.

    Examples
    --------
    >>> nx.is_eulerian(nx.DiGraph({0: [3], 1: [2], 2: [3], 3: [0, 1]}))
    True
    >>> nx.is_eulerian(nx.complete_graph(5))
    True
    >>> nx.is_eulerian(nx.petersen_graph())
    False

    Notes
    -----
    If the graph is not connected (or not strongly connected, for
    directed graphs), this function returns False.

    """
    if G.is_directed():
        # Every node must have equal in degree and out degree and the
        # graph must be strongly connected
        return (all(G.in_degree(n) == G.out_degree(n) for n in G) and
                nx.is_strongly_connected(G))
    # An undirected Eulerian graph has no vertices of odd degree and
    # must be connected.
    return all(d % 2 == 0 for v, d in G.degree()) and nx.is_connected(G)


def is_semieulerian(G):
    """Return True iff `G` is semi-Eulerian.

    G is semi-Eulerian if it has an Eulerian path but no Eulerian circuit.
    """
    return has_eulerian_path(G) and not is_eulerian(G)


def _find_path_start(G):
    """Return a suitable starting vertex for an Eulerian path.

    If no path exists, return None.
    """
    if not has_eulerian_path(G):
        return None

    if is_eulerian(G):
        return arbitrary_element(G)

    if G.is_directed():
        v1, v2 = [v for v in G if G.in_degree(v) != G.out_degree(v)]
        # Determines which is the 'start' node (as opposed to the 'end')
        if G.out_degree(v1) > G.in_degree(v1):
            return v1
        else:
            return v2

    else:
        # In an undirected graph randomly choose one of the possibilities
        start = [v for v in G if G.degree(v) % 2 != 0][0]
        return start


def _simplegraph_eulerian_circuit(G, source):
    if G.is_directed():
        degree = G.out_degree
        edges = G.out_edges
    else:
        degree = G.degree
        edges = G.edges
    vertex_stack = [source]
    last_vertex = None
    while vertex_stack:
        current_vertex = vertex_stack[-1]
        if degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex)
            last_vertex = current_vertex
            vertex_stack.pop()
        else:
            _, next_vertex = arbitrary_element(edges(current_vertex))
            vertex_stack.append(next_vertex)
            G.remove_edge(current_vertex, next_vertex)


def _multigraph_eulerian_circuit(G, source):
    if G.is_directed():
        degree = G.out_degree
        edges = G.out_edges
    else:
        degree = G.degree
        edges = G.edges
    vertex_stack = [(source, None)]
    last_vertex = None
    last_key = None
    while vertex_stack:
        current_vertex, current_key = vertex_stack[-1]
        if degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex, last_key)
            last_vertex, last_key = current_vertex, current_key
            vertex_stack.pop()
        else:
            triple = arbitrary_element(edges(current_vertex, keys=True))
            _, next_vertex, next_key = triple
            vertex_stack.append((next_vertex, next_key))
            G.remove_edge(current_vertex, next_vertex, next_key)


def eulerian_circuit(G, source=None, keys=False):
    """Returns an iterator over the edges of an Eulerian circuit in `G`.

    An *Eulerian circuit* is a closed walk that includes each edge of a
    graph exactly once.

    Parameters
    ----------
    G : NetworkX graph
       A graph, either directed or undirected.

    source : node, optional
       Starting node for circuit.

    keys : bool
       If False, edges generated by this function will be of the form
       ``(u, v)``. Otherwise, edges will be of the form ``(u, v, k)``.
       This option is ignored unless `G` is a multigraph.

    Returns
    -------
    edges : iterator
       An iterator over edges in the Eulerian circuit.

    Raises
    ------
    NetworkXError
       If the graph is not Eulerian.

    See Also
    --------
    is_eulerian

    Notes
    -----
    This is a linear time implementation of an algorithm adapted from [1]_.

    For general information about Euler tours, see [2]_.

    References
    ----------
    .. [1] J. Edmonds, E. L. Johnson.
       Matching, Euler tours and the Chinese postman.
       Mathematical programming, Volume 5, Issue 1 (1973), 111-114.
    .. [2] https://en.wikipedia.org/wiki/Eulerian_path

    Examples
    --------
    To get an Eulerian circuit in an undirected graph::

        >>> G = nx.complete_graph(3)
        >>> list(nx.eulerian_circuit(G))
        [(0, 2), (2, 1), (1, 0)]
        >>> list(nx.eulerian_circuit(G, source=1))
        [(1, 2), (2, 0), (0, 1)]

    To get the sequence of vertices in an Eulerian circuit::

        >>> [u for u, v in nx.eulerian_circuit(G)]
        [0, 2, 1]

    """
    if not is_eulerian(G):
        raise nx.NetworkXError("G is not Eulerian.")
    if G.is_directed():
        G = G.reverse()
    else:
        G = G.copy()
    if source is None:
        source = arbitrary_element(G)
    if G.is_multigraph():
        for u, v, k in _multigraph_eulerian_circuit(G, source):
            if keys:
                yield u, v, k
            else:
                yield u, v
    else:
        for u, v in _simplegraph_eulerian_circuit(G, source):
            yield u, v


def has_eulerian_path(G):
    """Return True iff `G` has an Eulerian path.

    An Eulerian path is a path in a graph which uses each edge of a graph
    exactly once.

    A directed graph has an Eulerian path iff:
        - at most one vertex has out_degree - in_degree = 1,
        - at most one vertex has in_degree - out_degree = 1,
        - every other vertex has equal in_degree and out_degree,
        - and all of its vertices with nonzero degree belong to a
        - single connected component of the underlying undirected graph.

    An undirected graph has an Eulerian path iff:
        - exactly zero or two vertices have odd degree,
        - and all of its vertices with nonzero degree belong to a
        - single connected component.

    Parameters
    ----------
    G : NetworkX Graph
        The graph to find an euler path in.

    Returns
    -------
    Bool : True if G has an eulerian path.

    See Also
    --------
    is_eulerian
    eulerian_path
    """
    if G.is_directed():
        ins = G.in_degree
        outs = G.out_degree
        semibalanced_ins = sum(ins(v) - outs(v) == 1 for v in G)
        semibalanced_outs = sum(outs(v) - ins(v) == 1 for v in G)
        return (semibalanced_ins <= 1 and
                semibalanced_outs <= 1 and
                sum(G.in_degree(v) != G.out_degree(v) for v in G) <= 2 and
                nx.is_weakly_connected(G))
    else:
        return (sum(d % 2 == 1 for v, d in G.degree()) in (0, 2)
                and nx.is_connected(G))


def eulerian_path(G, source=None, keys=False):
    """Return an iterator over the edges of an Eulerian path in `G`.

    Parameters
    ----------
    G : NetworkX Graph
        The graph in which to look for an eulerian path.
    source : node or None (default: None)
        The node at which to start the search. None means search over all
        starting nodes.
    keys : Bool (default: False)
        Indicates whether to yield edge 3-tuples (u, v, edge_key).
        The default yields edge 2-tuples

    Yields
    ------
    Edge tuples along the eulerian path.

    Warning: If `source` provided is not the start node of an Euler path
    will raise error even if an Euler Path exists.
    """
    if not has_eulerian_path(G):
        raise nx.NetworkXError("Graph has no Eulerian paths.")
    if G.is_directed():
        G = G.reverse()
    else:
        G = G.copy()
    if source is None:
        source = _find_path_start(G)
    if G.is_multigraph():
        for u, v, k in _multigraph_eulerian_circuit(G, source):
            if keys:
                yield u, v, k
            else:
                yield u, v
    else:
        for u, v in _simplegraph_eulerian_circuit(G, source):
            yield u, v


@not_implemented_for('directed')
def eulerize(G):
    """Transforms a graph into an Eulerian graph

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph

    Returns
    -------
    G : NetworkX multigraph

    Raises
    ------
    NetworkXError
       If the graph is not connected.

    See Also
    --------
    is_eulerian
    eulerian_circuit

    References
    ----------
    .. [1] J. Edmonds, E. L. Johnson.
       Matching, Euler tours and the Chinese postman.
       Mathematical programming, Volume 5, Issue 1 (1973), 111-114.
       [2] https://en.wikipedia.org/wiki/Eulerian_path
    .. [3] http://web.math.princeton.edu/math_alive/5/Notes1.pdf

    Examples
    --------
        >>> G = nx.complete_graph(10)
        >>> H = nx.eulerize(G)
        >>> nx.is_eulerian(H)
        True

    """
    if G.order() == 0:
        raise nx.NetworkXPointlessConcept("Cannot Eulerize null graph")
    if not nx.is_connected(G):
        raise nx.NetworkXError("G is not connected")
    odd_degree_nodes = [n for n, d in G.degree() if d % 2 == 1]
    G = nx.MultiGraph(G)
    if len(odd_degree_nodes) == 0:
        return G

    # get all shortest paths between vertices of odd degree
    odd_deg_pairs_paths = [(m,
                            {n: nx.shortest_path(G, source=m, target=n)}
                            )
                           for m, n in combinations(odd_degree_nodes, 2)]

    # use inverse path lengths as edge-weights in a new graph
    # store the paths in the graph for easy indexing later
    Gp = nx.Graph()
    for n, Ps in odd_deg_pairs_paths:
        for m, P in Ps.items():
            if n != m:
                Gp.add_edge(m, n, weight=1/len(P), path=P)

    # find the minimum weight matching of edges in the weighted graph
    best_matching = nx.Graph(list(nx.max_weight_matching(Gp)))

    # duplicate each edge along each path in the set of paths in Gp
    for m, n in best_matching.edges():
        path = Gp[m][n]["path"]
        G.add_edges_from(nx.utils.pairwise(path))
    return G
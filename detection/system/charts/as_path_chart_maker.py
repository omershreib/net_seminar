from detection.system.analysis.asn_path_graphic_analysis import asn_path_graphic_analysis
from detection.utilities.as_relationships import get_as_relationships
import networkx as nx
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

AS_RELATIONSHIPS = get_as_relationships()


def make_edges(nodes):
    """
    make edges from an ordered list of nodes.
    for example, [100, 200, 300] --> [(100, 200), (200, 300)]

    Note:
    -----
    the order of the ASNs in the nodes list is matter and assumed to be
    in the same order of the actual AS-path.

    :param nodes: ASNs nodes list
    :return: edges list
    """
    edges = []

    for i in range(len(nodes) - 1):
        u = nodes[i]
        v = nodes[i + 1]
        edge = (u, v)
        edges.append(edge)

    return edges


def assign_levels(nodes, as_relationships):
    """
    assigning graph nodes levels

    the level of every node will decide its vertical position on the final AS-path chart figure,
    so if, for example, the level of node 100 is 0 and the level 0 node 200 is 1, then node 100
    will appear in a lower position compare to node 200.

    The leveling setup is decided according to the ToRs between neighbor ASN nodes in the given ASN nodes list.

    :param nodes: ASNs nodes list
    :param as_relationships: a dictionary defining the ToRs between ASN nodes
    :return:
    """
    levels = {}
    current_level = 0
    prev_node = None

    for node in nodes:
        if not prev_node:
            prev_node = node
            levels[node] = current_level
            continue

        if node in as_relationships[prev_node]['customers']:
            current_level -= 1
            levels[node] = current_level
            prev_node = node
            continue

        if node in as_relationships[prev_node]['providers']:
            current_level += 1
            levels[node] = current_level
            prev_node = node
            continue

        prev_node = node
        levels[node] = current_level
        continue

    return levels


def get_as_path_chart_fig(title, nodes, edges, as_relationships):
    """
    Get AS-path Chart Figure

    this function creates an AS-path chart figure.

    :param title: chart title
    :param nodes: ASNs nodes list
    :param edges: the nodes' edges list
    :param as_relationships: a dictionary defining the ToRs between ASN nodes
    :return: matplotlib chart figure
    """
    # build graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    levels = assign_levels(nodes, as_relationships)

    # Build positions: spread on x, y = level
    pos = {}
    for i, n in enumerate(nodes):
        pos[n] = (i, levels[n])

    edge_colors, edge_styles, edge_labels, error_nodes = asn_path_graphic_analysis(G, as_relationships)
    node_colors = []

    for n in G.nodes():
        if n in error_nodes:
            node_colors.append('red')
        if n not in error_nodes:
            node_colors.append('lightgray')

    plt.style.use('dark_background')
    fig = plt.figure()

    # draw graph
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
    nx.draw_networkx_labels(G, pos)

    for (u, v), color, style in zip(G.edges(), edge_colors, edge_styles):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, style=style, arrows=True)

    try:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
        plt.axis('off')
        plt.title(title)

        return fig

    except Exception as e:
        print(e)
        return fig
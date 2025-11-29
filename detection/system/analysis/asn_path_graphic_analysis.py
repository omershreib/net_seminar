
def asn_path_graphic_analysis(G, as_relationships):
    """
    ASN Path Graphic Analysis

    this function responsible to set the coloring of a given as-path graph, which include the
    edge colors and style, remark the ToR of every edge and finding error nodes that cause for a
    valley-free route. P2C or C2P ToR edges are colored with green, P2P or unknown ToR edges with blue,
    and invalid (valley-free) section in red.

    :param G: nx.DiGraph() graph object
    :param as_relationships:  dictionary depicting the customer-provider relationship between ASNs in the lab

    :return: edge_colors: list, edge_styles: list, edge_labels: dict, error_nodes: list
    """

    edge_colors = []
    edge_styles = []
    edge_tors = {}
    error_nodes = []

    # this list is for searching for a valley-free
    # by saving the previous two consecutive ToRs
    last_tors = [None, None]

    for u, v in G.edges():
        # default parameters
        this_tor = '?'
        this_color = 'blue'
        this_style = 'dotted'

        if u in as_relationships[v]['customers']:
            this_style = 'solid'
            this_color = 'green'
            this_tor = 'C2P'

            # in case of valley-free, set the previous and the current edge color to red
            if last_tors[0] == 'P2C' and last_tors[1] == 'C2P':
                edge_colors[-1] = 'red'
                this_color = 'red'
                error_nodes.append(u)

        if u in as_relationships[v]['providers']:
            this_tor = 'P2C'
            this_style = 'solid'
            this_color = 'green'

        if u in as_relationships[v]['other_peers']:
            this_tor = 'P2P'
            this_style = 'solid'
            this_color = 'blue'

        edge_colors.append(this_color)
        edge_styles.append(this_style)
        edge_tors[(u, v)] = this_tor
        last_tors[1] = last_tors[0]
        last_tors[0] = this_tor

    return edge_colors, edge_styles, edge_tors, error_nodes

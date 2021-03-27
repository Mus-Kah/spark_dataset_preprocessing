import plotly.graph_objects as go
from .visualization_array import visualization_array
from .random_colors import random_colors
from igraph import Graph, EdgeSeq
from utils.utils import sorted_data, discrete_columns, cols_for_clustering


def visualize_combinations(sorted_cols, sorted_values, title):
    fig = go.Figure(go.Surface(
        contours={
            "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color": "white"},
            "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05}
        },
        x=sorted_cols,

        y=sorted_cols,
        z=visualization_array(sorted_cols, sorted_values)
    )
    )
    fig.update_layout(
        title=title,
        scene={
            "xaxis": {"nticks": 20},
            "zaxis": {"nticks": 4},
            'camera_eye': {"x": 0, "y": -1, "z": 0.5},
            "aspectratio": {"x": 1, "y": 1, "z": 0.2}
        })
    fig.show()

def visualize_cols_stats(data):
    cat_cols = discrete_columns(data)
    cont_cols = cols_for_clustering(data)
    labels = ["Discrete columns", "Continuous columns"]
    values= [len(cat_cols), len(cont_cols)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.show()

def visualize_columns(cols, values, title):
    fig = go.Figure(data=[go.Scatter(
        x=cols, y=values,
        mode='markers',
        marker_size=[60 for i in range(len(cols))],
        marker_color=random_colors(len(cols))
    )
    ]
    )

    fig.update_layout(
        title=title
    )
    fig.show()

def hierarchical_visualization(data, sorted_cols, nbr_patterns):


    from utils.utils import network_vis_array
    data=sorted_data(data, sorted_cols)

    nbr_vis_cols = nbr_patterns//4
    vis_cols = sorted_cols[:nbr_vis_cols]
    values_list=network_vis_array(data, vis_cols)

    G = build_network(values_list, nbr_patterns)
    node_trace, edge_trace = network_components(G)
    set_traces(G, node_trace)

    draw_network(edge_trace, node_trace)


def build_network(cols, nbr_nodes):

    l = cols

    import networkx as nx
    G = nx.Graph()

    for j in range(len(l[0])):
        if G.number_of_nodes() >= nbr_nodes:
            break

        for i in range(len(l)):
            if G.number_of_nodes() < 20 and not (l[i][j] in G.nodes()):
                G.add_node(l[i][j], pos=(i * 2, 10 - j))
                last = j
                if j > 0 and l[i][j - 1] in G.nodes():
                    G.add_edge(l[i][j], l[i][j - 1])
                if j > last:
                    G.add_edge(l[i][j], l[i][last])
        for i in range(len(l) - 1):
            if l[i][j] in G.nodes() and l[i + 1][j] in G.nodes():
                G.add_edge(l[i][j], l[i + 1][j])

    return G

def network_components(G):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=3, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Rainbow',
            reversescale=True,
            color=[],
            size=50,
            colorbar=dict(
                thickness=15,
                title='Hierarchy levels',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    return node_trace, edge_trace

def set_traces(G, node_trace):
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies
    node_trace.text = list(G.nodes)

def draw_network(edge_trace, node_trace):
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Hierachical visualization',
                        titlefont_size=20,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),

                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()


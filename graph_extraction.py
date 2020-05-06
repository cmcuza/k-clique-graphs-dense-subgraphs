import pandas as pd
import matplotlib.pyplot as plt
from greedy_algorithms import *


def create_edges_file():
    df = pd.read_csv("networks/link.csv")
    new_df = df[["Node_Start", "Node_End"]]
    new_df.to_csv("networks/road_segment.txt", sep='\t', index=False)


def subgraph_visualization():
    G = nx.read_edgelist('networks/road_segment.txt', delimiter='\t', nodetype=int)

    G = G.to_undirected()

    # for node in G.nodes_with_selfloops():
    #	G.remove_edge(node, node)

    G1 = nx.Graph()
    for edge in G.edges():
        u = edge[0]
        v = edge[1]
        if u == v:
            print("ignored self loops")
            continue
        if not G1.has_edge(u, v):
            G1.add_edge(u, v, weight=1.0)
        else:
            print("multiple edge same nodes")

    G = G1
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())
    print()

    subg = greedy_quasi_cliques(G, 0.01)
    max_cc = nx.Graph()
    for i, cc in enumerate(nx.connected_components(subg)):
        ccG = nx.Graph()
        ccG.add_nodes_from(cc)
        cc = list(cc)
        for j in range(len(cc)):
            for k in range(len(cc)):
                if subg.has_edge(cc[j], cc[k]):
                    ccG.add_edge(cc[j], cc[k])

        print("----Greedy Edge Surplus with alpha=0.02----")
        print("Degree Density: " + str(degree_density(ccG)))
        print("Density: " + str(density(ccG)))
        print("Triangle Density: " + str(triangle_density(ccG)))
        print("# Nodes: " + str(ccG.number_of_nodes()))
        print()
        nx.draw_networkx(ccG)
        plt.savefig("quasi_cliques_path_{}.png".format(i))  # save as png
        plt.show()
        if ccG.number_of_nodes() > max_cc.number_of_nodes():
            max_cc = ccG

    print("Max component number of nodes ", max_cc.number_of_nodes())
    print("Max component number of nodes ", max_cc.number_of_edges())

    with open("networks/max_dense_subgraph.txt", 'w') as f:
        df = pd.read_csv("networks/link.csv")
        for link in df[["Node_Start", "Node_End"]].values:
            if max_cc.has_edge(link[0], link[1]):
                f.write("{}\t{}\n".format(*link))


if __name__ == "__main__":
    #create_edges_file()
    subgraph_visualization()
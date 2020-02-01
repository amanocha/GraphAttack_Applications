import numpy as np
from scipy.sparse import csr_matrix

def clean_data(filename):
    with open(filename) as edge_list:
        graph_edge_data = np.fromfile(edge_list, count=-1, sep='\t',dtype=np.int64)
        graph_edge_data = np.reshape(graph_edge_data, (int(len(graph_edge_data) / 2), 2))

    graph_edge_data = np.array([[x,y] for (x,y) in graph_edge_data if x!=y])

    return graph_edge_data

def load_csr(graph_edge_data):
    num_nodes = np.max(graph_edge_data) + 1
    num_edges = len(graph_edge_data)

    row = graph_edge_data[:,0]
    column = graph_edge_data[:,1]
    data = np.ones(num_edges)

    S = csr_matrix((data, (column,row)), shape=(num_nodes, num_nodes))
    T = csr_matrix((data, (row,column)), shape=(num_nodes, num_nodes))

    return S, T

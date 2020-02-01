import graph
import numpy as np
import sys
from time import time

def pagerank(S, T, V, E, ret, delta, alpha, epsilon):
    while True:
        curr = np.copy(ret)
        for v in range(V):
            S_v = S.indices[S.indptr[v]:S.indptr[v+1]]
            sum = np.float32(0)
            for w in S_v:
                T_w = T.indptr[w+1] - T.indptr[w]
                sum = sum + curr[w]/T_w
            ret[v] = alpha*sum + (1-alpha)
            delta[v] = abs(ret[v] - curr[v])
        if max(delta) < epsilon:
            break

if __name__ == "__main__":
    t0 = time()

    # get graph
    edge_data = graph.clean_data(sys.argv[1])
    S, T = graph.load_csr(edge_data)
    
    # get graph info
    assert (len(S.indptr) == len(T.indptr))
    assert (len(S. data) == len(T.data))
    num_nodes = len(S.indptr)-1
    num_edges = len(S.data)
    print('Number of nodes:', num_nodes)
    print('Number of edges:', num_edges)

    t1 = time()
    print("Reading graph elapsed time: " + str(t1-t0))

    # kernel initialization
    alpha = np.float32(0.85)
    epsilon = np.float32(0.01)
    ret = (1-alpha)*np.ones(num_nodes, dtype='float32')
    delta = np.zeros(num_nodes, dtype='float32')

    # kernel
    t2 = time()
    pagerank(S, T, num_nodes, num_edges, ret, delta, alpha, epsilon)
    t3 = time()
    print("Kernel time: " + str(t3-t2))

    # write results to file
    pr_file = open("PR_out.txt", "w+")
    for v in range(num_nodes):
        pr_file.write(str(v) + "\t" + str(ret[v]) + "\n")
    pr_file.close()

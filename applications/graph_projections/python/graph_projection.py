import numpy as np
from numba import jitclass, int32, njit, float32    # import the types
from numba import types as nb_types                 # creates type from input
import sys
from DEC_Pipeline import DEC_Pipeline, DEC_Options, decades_launch_kernel
from DEC_Numba_Lib import TriDenseGraph_num_ele_i_rows as num_ele_i_rows
from DEC_Numba_Lib import PyDECADES_barrier
from DEC_Numba_Lib import DecBipartiteGraph, DecBipartiteGraphSpec, LoadDecBipartiteGraph
from time import time
import pdb



@njit((DecBipartiteGraphSpec(),int32[:], int32, int32), nogil=True, pipeline_class=DEC_Pipeline)
def _kernel_(graph, output, tid, num_threads):
    tri_size = graph.tri_size
    for i in range(graph.x_nodes):
        for e1 in range(graph.node_array[i] + tid, graph.node_array[i+1]-1, num_threads):
            y_node1 = graph.edge_array[e1]
            index_before_i = num_ele_i_rows(graph.y_nodes, y_node1, tri_size)
            for e2 in range(e1+1, graph.node_array[i+1]):
                y_node2 = graph.edge_array[e2]
                #assert(y_node1 < y_node2)
                k = index_before_i + y_node2- y_node1 - 1
                #assert(k >= 0)
                #assert(k < graph.projection_size)
                # here to be used decades based increment function for random memory access
                output[k] += 1
                
        PyDECADES_barrier()


if __name__ == "__main__":

    # read input arguments
    file_name = sys.argv[1]
    #projection_type = sys.argv[2]

    # read the graph data
    t=time()
    #pdb.set_trace()
    G = LoadDecBipartiteGraph(file_name)
    print('load time:',time()-t)

    DEC_Options.preset_config()
    output = np.zeros(G.projection_size, dtype=np.int32)
    # compute projection
    t = decades_launch_kernel(_kernel_, G, output)

    print('compute time:',t)
    # save output
    # np.savetxt('projected_graph.txt', projected_graph, fmt="%s")

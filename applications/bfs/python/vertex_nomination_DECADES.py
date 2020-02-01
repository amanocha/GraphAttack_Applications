from __future__ import division, print_function
import argparse
from time import time
import numpy as np
from numba import int64, float32, float64,jitclass, njit, int32
from numba.types import Tuple
from scipy.sparse import csr_matrix

from DEC_Pipeline import DEC_Pipeline, decades_launch_kernel, DEC_Options
from DEC_Numba_Lib import DecSparseGraph, LoadDecSparseGraph, DecSparseGraphSpec, dec_int64_max

@njit(int64[:](DecSparseGraphSpec(), int64[:]), nogil=True, pipeline_class=DEC_Pipeline)
def multi_bfs(graph, roots):
    node_visit_list = np.ones(graph.num_nodes, dtype=np.int64) * np.int64(-1)
    top_layer = list(roots)
    next_layer = [np.int64(x) for x in range(0)]
    hop = 1

    while len(top_layer) > 0:
        for each_node in top_layer:
            for e in graph.indices[graph.indptr[each_node]:graph.indptr[each_node + 1]]:
                if node_visit_list[e] == -1:
                    node_visit_list[e] = hop
                    next_layer.append(e)
        # reset top_layer and next_layer list:            
        top_layer = next_layer
        next_layer = [np.int64(x) for x in range(0)]
        hop += 1

    return node_visit_list


@njit(float64[:](DecSparseGraphSpec(), int64[:]), nogil=True, pipeline_class=DEC_Pipeline)
def getContentScore(graph, roots):
    top_layer = list(roots)
    # get # of direct connection score
    directConnectionScore =  np.zeros(graph.num_nodes, dtype=np.int64)
    for each_node in top_layer:
        for e in graph.indices[graph.indptr[each_node]:graph.indptr[each_node + 1]]:
            directConnectionScore[e] +=1
    directConnectionScore = np.log(directConnectionScore+2)
              
    # get node attribute score
    beta = 0.25
    max_i64 = np.int64(dec_int64_max((graph.node_attr)))
    node_score = beta * np.log10(max_i64/graph.node_attr)
    
              
    contentscore = node_score + directConnectionScore

    return contentscore


@njit((DecSparseGraphSpec(), int64[:],int64[:],float32[:],int32,int32), nogil=True, pipeline_class=DEC_Pipeline)
def vertex_nomination__kernel__(G, seeds, ret_top_nominee, ret_top_score, tid, num_threads):
    if tid == 0:
        
        # context score : computed via distance map from multi BFS
        bfs_results = multi_bfs(G, seeds)
        context_sim = 1/bfs_results
        
        # content score : placeholder computed via a random number generator
        content_sim = getContentScore(G, seeds)

        # fusion score : content_sim * context_sim 
        fusion_score = np.multiply(content_sim, context_sim)

        # remove original seeds from ranking
        for seed in seeds:
            fusion_score[seed] = np.float64(-1)
          
        top_nominee = np.int64(np.argmax(fusion_score))
        top_score = fusion_score[top_nominee]
        
        ret_top_nominee[0] = top_nominee
        ret_top_score[0] = top_score


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpath', type=str, default='_data/enron')
    #parser.add_argument('--inpath', type=str, default='/_data/actor-collaborations')
    parser.add_argument('--seed', type=int, default=123)
    parser.add_argument('--num-runs', type=int, default=1)
    parser.add_argument('--num-seeds', type=int, default=5)
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    t = time()

    # load graph
    G = LoadDecSparseGraph(args.inpath)
    print('load time = %f' % (time() - t))

    # initialize set of seeds
    seeds = set()
    np.random.seed(113)

    # get number of nodes in graph
    num_nodes_connected = len(G.indptr)
    print('number of nodes:',num_nodes_connected)
    print('number of nodes from G:', G.num_nodes)
    # get seeds
    #seed_input = input('Please enter five seeds separated by comma:')
    seed_input = False
    if seed_input:
        seeds = list(map(int,seed_input.split(',')))
        if len(seeds)<5 or all(i >= G.num_nodes for i in seeds):
            print('Incorrect input entry!')
            raise
    else:
        # get random nodes in graph:
        seeds = np.random.choice(num_nodes_connected, 5, replace=False)

    seeds = np.array(list(seeds), dtype=np.int64)
    print('Starting with seeds:', seeds)


    # Vertex Nomination
    ret1 = np.zeros(1, dtype=np.int64)
    ret2 = np.zeros(1, dtype=np.float32)

    #DEC_Options.set_simulator_target()
    DEC_Options.set_num_threads(1)
    #DEC_Options.set_decoupled_mode()
    
    t = decades_launch_kernel(vertex_nomination__kernel__, G, seeds, ret1, ret2)
    print('Top nominee:',ret1[0],';Top score:',ret2[0])
    print("Compute time: " + str(t))    

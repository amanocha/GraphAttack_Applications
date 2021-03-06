#include "stdio.h"
#include "stdlib.h"
#include "assert.h"
#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include "../common/graph.h"

using namespace std;

void _kernel_(csr_graph G, int * ret, unsigned int *in_wl, unsigned int* in_index, unsigned int *out_wl, unsigned int *out_index, int tid, int num_threads) {

  int hop = 1;

  while (in_index[0] > 0) {
    printf("-- epoch %d %d\n", hop, in_index[0]);
    for (int i = 0; i < in_index[0]; i++) {
      int node = in_wl[i];
      //printf("nodes %d \n", node);
      
      for (unsigned int e = G.node_array[node]; e < G.node_array[node+1]; e++) {
	unsigned int edge_index = G.edge_array[e];
	int v = ret[edge_index];
	if (v == -1) {
	  ret[edge_index] = hop;
	  //printf("pushing %d\n", edge_index);
	  //Should be atomic increment
	  int index = out_index[0];
	  out_index[0] = index + 1;
	  assert(index < G.nodes * 2);
	  out_wl[index] = edge_index;
	}
      }
    }
    unsigned int *tmp = out_wl;
    out_wl = in_wl;
    in_wl = tmp;

    in_index[0] = out_index[0];
    out_index[0] = 0;
    hop++;
  }  
}

int main(int argc, char** argv) {

  char *graph_fname;
  csr_graph G;

  assert(argc == 2);
  graph_fname = argv[1];

  G = parse_csr_graph(graph_fname);
  int * ret = (int *) malloc(sizeof(int) * G.nodes * 2);

  for (int i = 0; i < G.nodes * 2; i++) {
    ret[i] = -1;
  }
  
  unsigned int * in_index = (unsigned int *) malloc(sizeof(unsigned int) * 1);
  *in_index = 0;
  unsigned int * out_index = (unsigned int *) malloc(sizeof(unsigned int) * 1);
  *out_index = 0;
  
  unsigned int * in_wl = (unsigned int *) malloc(sizeof(unsigned int) * G.nodes * 2);
  unsigned int * out_wl = (unsigned int *) malloc(sizeof(unsigned int) * G.nodes * 2);

  for (int i = 0; i < SEEDS; i++) {
    int index = *in_index;
    *in_index = index + 1;
    in_wl[index] = i;
    ret[index] = 0;
  }

  printf("\n\nstarting kernel\n");
  auto start = chrono::system_clock::now();

  _kernel_(G, ret, in_wl, in_index, out_wl, out_index, 0 , 1);

  printf("\nending kernel");
  auto end = std::chrono::system_clock::now();
  chrono::duration<double> elapsed_seconds = end-start;
  cout << "\nkernel computation time: " << elapsed_seconds.count() << "s\n";
  

#if defined(OUTPUT_RET)
  ofstream outfile;
  outfile.open ("VE_out.txt");
  for (int i = 0; i < G.nodes; i++) {
    outfile << ret[i] << "\n";
  }
  outfile.close();
  //  return 0;

#endif
  
  free(ret);
  free(in_index);
  free(out_index);
  free(in_wl);
  free(out_wl);
  clean_csr_graph(G);

  return 0;
}

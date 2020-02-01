#include "stdio.h"
#include "stdlib.h"
#include "assert.h"
#include <cmath>
#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include "../common/graph.h"

using namespace std;

void _kernel_(csr_graph S, csr_graph T, float* x, float* r, unsigned int* in_wl, unsigned int* in_index, unsigned int* out_wl, unsigned int* out_index, float alpha, float epsilon, int tid, int num_threads) {

  int v, T_v, w;
  float r_old;

  while (*in_index > 0) {
    // pop worklist
    v = in_wl[*in_index-1];
    *in_index = *in_index - 1;
    
    x[v] = x[v] + r[v];    
    T_v = T.node_array[v+1]-T.node_array[v];
    
    for (int i = T.node_array[v]; i < T.node_array[v+1]; i++) {
      w = T.edge_array[i];
      r_old = r[w];
      r[w] = r[w] + r[v]*alpha/T_v;
      if (r[w] >= epsilon && r_old < epsilon) {
        // push to worklist
        int index = out_index[0];
        out_wl[index] = w;
        out_index[0] = index + 1;
      }
    }

    // swap worklists
    if (*in_index == 0) {
      unsigned int *tmp = out_wl;
      out_wl = in_wl;
      in_wl = tmp;
      in_index[0] = out_index[0];
      out_index[0] = 0;
    }

    r[v] = 0;
  }  
}

int main(int argc, char** argv) {

  char *graph_fname;
  pr_graph graph;
  csr_graph S, T;
  float alpha = 0.85;
  float epsilon = 0.01;

  assert(argc >= 2);
  graph_fname = argv[1];

  if (argc >= 3) {
    alpha = atof(argv[2]);
  }
  if (argc >= 4) {
    epsilon = atof(argv[3]);
  }

  // Create data structures
  graph = create_pr_graph(graph_fname);
  S = graph.S;
  T = graph.T;
  int V = T.nodes;
  
  float * x = (float *) malloc(sizeof(float) * V);
  float * r = (float *) malloc(sizeof(float) * V);

  unsigned int * in_index = (unsigned int *) malloc(sizeof(unsigned int) * 1);
  *in_index = 0;
  unsigned int * out_index = (unsigned int *) malloc(sizeof(unsigned int) * 1);
  *out_index = 0;
  
  unsigned int * in_wl = (unsigned int *) malloc(sizeof(unsigned int) * V);
  unsigned int * out_wl = (unsigned int *) malloc(sizeof(unsigned int) * V);

  // Kernel initialization
  for (int v = 0; v < V; v++) {
    x[v] = 1 - alpha;
    r[v] = 0;
  }
  
  for (int v = 0; v < V; v++) {
    for (int i = S.node_array[v]; i < S.node_array[v+1]; i++) {
        int w = S.edge_array[i];
        r[v] = r[v] + 1.0/(T.node_array[w+1]-T.node_array[w]);
    }
    r[v] = (1-alpha)*alpha*r[v];
  
    int index = *in_index;
    in_wl[index] = v;
    *in_index = index + 1;
  }

  // Kernel execution
  printf("\n\nstarting kernel\n");
  auto start = chrono::system_clock::now();

  _kernel_(S, T, x, r, in_wl, in_index, out_wl, out_index, alpha, epsilon, 0 , 1);

  printf("\nending kernel");
  auto end = std::chrono::system_clock::now();
  chrono::duration<float> elapsed_seconds = end-start;
  cout << "\nkernel computation time: " << elapsed_seconds.count() << "s\n";
  
#if defined(OUTPUT_RET)
  ofstream outfile;
  outfile.open ("PR_out.txt");
  for (int v = 0; v < V; v++) {
    outfile << v << "\t" << x[v] << "\n";
  }
  outfile.close();
  //  return 0;
#endif
  
  free(x);
  free(r);
  free(in_index);
  free(out_index);
  free(in_wl);
  free(out_wl);
  clean_pr_graph(graph);

  return 0;
}

#include <iostream>
#include <assert.h>
#include <fstream>
#include <chrono>
#include <string>

using namespace std;

// CSR graph
class csr_graph {
public:
  unsigned int nodes;
  unsigned int edges;
  unsigned int *node_array;
  unsigned int *edge_array;
  int *node_data;
};

csr_graph to_check;

// Parsing a bipartite graph
csr_graph parse_csr_graph(char *fname) {
  csr_graph ret;
  fstream reader(fname);
  string line;
  char comment;
  unsigned int first, second;
  float weight;

  // first line is just a comment.
  //reader >> fake;
  // getline( reader, line );

  // use second line to get edges, nodes, etc.

  auto start = chrono::system_clock::now();
  reader >> comment >> first >> second;

  cout << "graph: " << fname << "\nedges: " << first << "\ngraph_nodes: " << second << "\n\n";

  ret.nodes = second;
  ret.edges = first;
  ret.node_array = (unsigned int*) malloc(sizeof(unsigned int) * (ret.nodes + 1));
  ret.edge_array = (unsigned int*) malloc(sizeof(unsigned int) * (ret.edges));
  ret.node_data = (int*) malloc(sizeof(int) * (ret.edges));
  //ret.edge_data = (float*) malloc(sizeof(float) * (ret.edges));

  unsigned int node = 0;
  ret.node_array[0] = 0;
  for(unsigned int i = 0; i < ret.edges; i++ ) {
    if (i % 100000 == 0) {
      printf("reading %% %.2f finished\r", (float(i)/float(ret.edges)) * 100);
      fflush(stdout);
    }
    reader >> first >> second >> weight;
    //if (first == 232770) {
    //  printf("%d %d\n", first, second);
    //}
    if (first != node) {
      while (node != first) {
	node++;
	ret.node_array[node] = i;
      }
    }
    ret.edge_array[i] = second;
    ret.node_data[i] = (int) weight;
  }
  printf("reading %% 100.00 finished\n");
  ret.node_array[ret.nodes] = ret.edges;

  auto end = std::chrono::system_clock::now();
  chrono::duration<double> elapsed_seconds = end-start;
  cout << "Reading graph elapsed time: " << elapsed_seconds.count() << "s\n";


  return ret;
}

void print_binary_file(csr_graph to_print, string base) {

  ofstream num_nodes_edges;
  num_nodes_edges.open(base + "num_nodes_edges.txt");
  
  if (!num_nodes_edges.is_open()) {
    assert(0);
  }

  num_nodes_edges << to_print.nodes << "\n";
  num_nodes_edges << to_print.edges << "\n";
  num_nodes_edges.close();

  ofstream node_array_file;
  node_array_file.open(base + "node_array.bin", ios::out | ios::binary);
  
  if (!node_array_file.is_open()) {
    assert(0);
  }

  node_array_file.write((char *)to_print.node_array, (to_print.nodes + 1) * sizeof(unsigned int));
  
  node_array_file.close();

  ofstream edge_array_file;
  edge_array_file.open(base + "edge_array.bin", ios::out | ios::binary);

  if (!edge_array_file.is_open()) {
    assert(0);
  }

  edge_array_file.write((char*)to_print.edge_array, to_print.edges * sizeof(unsigned int));

  edge_array_file.close();

  ofstream edge_values_file;
  edge_values_file.open(base + "edge_values.bin", ios::out | ios::binary);
  if (!edge_values_file.is_open()) {
    assert(0);
  }

  edge_values_file.write((char*)to_print.node_data, sizeof(int) * to_print.edges);
    
  edge_values_file.close();        
}

csr_graph parse_bin_files(string base) {
  csr_graph ret;
  ifstream nodes_edges_file(base + "/num_nodes_edges.txt");
  unsigned int nodes, edges;

  auto start = chrono::system_clock::now();
  
  nodes_edges_file >> nodes;
  nodes_edges_file >> edges;
  nodes_edges_file.close();
  cout << "found " << nodes << " " << edges << "\n";
  
  ret.nodes = nodes;
  ret.edges = edges;
  ret.node_array = (unsigned int*) malloc(sizeof(unsigned int) * (ret.nodes + 1));
  ret.edge_array = (unsigned int*) malloc(sizeof(unsigned int) * (ret.edges));
  ret.node_data = (int*) malloc(sizeof(int) * (ret.edges));

  ifstream node_array_file;
  node_array_file.open(base + "node_array.bin", ios::in | ios::binary);
  
  if (!node_array_file.is_open()) {
    assert(0);
  }

  node_array_file.read((char *)ret.node_array, (ret.nodes + 1) * sizeof(unsigned int));

  node_array_file.close();

  ifstream edge_array_file;
  edge_array_file.open(base + "edge_array.bin", ios::in | ios::binary);
  
  if (!edge_array_file.is_open()) {
    assert(0);
  }
  
  edge_array_file.read((char*)ret.edge_array, ret.edges * sizeof(unsigned int));
  
  edge_array_file.close();

  ifstream edge_values_file;
  edge_values_file.open(base + "edge_values.bin", ios::in | ios::binary);
  if (!edge_values_file.is_open()) {
    assert(0);
  }

  edge_values_file.read((char*)ret.node_data, sizeof(int) * ret.edges);
    
  edge_values_file.close();        

  


  auto end = std::chrono::system_clock::now();
  chrono::duration<double> elapsed_seconds = end-start;
  cout << "Reading graph elapsed time: " << elapsed_seconds.count() << "s\n";


#define CHECK
#ifdef CHECK
  assert(to_check.nodes == ret.nodes);
  assert(to_check.edges == ret.edges);
  for (int i = 0; i < ret.nodes + 1; i++) {
    assert(ret.node_array[i] == to_check.node_array[i]);
  }

  for (int i = 0; i < ret.edges + 1; i++) {
    assert(ret.edge_array[i] == to_check.edge_array[i]);
    assert(ret.node_data[i] == to_check.node_data[i]);
  }

#endif

  return ret;
  
  
}


int main(int argc, char** argv) {
  char *graph_fname, *base_name;
  csr_graph G;

  graph_fname = argv[1];
  if (argc > 2) {
    base_name = argv[2];
  } else {
    base_name = (char*) "./";
  }
  G = parse_csr_graph(graph_fname);
  to_check = G;
  print_binary_file(G, base_name);
  parse_bin_files(base_name);

  return 0;
}

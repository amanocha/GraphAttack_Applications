#include "stdio.h"
#include "stdlib.h"
#include "assert.h"
#include <iostream>
#include <string>
#include <fstream>
#include <chrono>

#define OUTPUT_RET

using namespace std;

// CSR sparse matrix
struct csr_sparse {
  unsigned int nodes;
  unsigned int size;  
  unsigned int *shape;
  unsigned int *indptr;
  unsigned int *indices;
  double       *data;
};

// Parsing a dense matrix
double* parse_dense_matrix(char *fname) {
  fstream in(fname);
  unsigned int m, n;
  
  if (!in) {
    cout << "Cannot open file.\n";
  }
  
  auto start = chrono::system_clock::now();
  in >> m >> n;

  cout << "dense matrix: " << fname << "\nrows: " << m << "\ncolumns: " << n << "\n\n";
  
  double* dense_matrix = (double*) malloc(sizeof(double) * m * n) ;
  //double dense_matrix[m * n];
  
  for (unsigned int i = 0; i < m; i++) {
    for (unsigned int j = 0; j < n; j++) {
      in >> dense_matrix[i*n + j];
      if ((i*n +j) % 100000 ==0){
	//cout << "reading element " << i*n + j << ":" << dense_matrix[i*n + j]  << "\n\n";
      }
    }
  }
  
  in.close();

  printf("reading %% 100.00 finished\n");
  
  auto end = std::chrono::system_clock::now();
  chrono::duration<double> elapsed_seconds = end-start;
  cout << "Reading dense matrix elapsed time: " << elapsed_seconds.count() << "s\n";
  
  return dense_matrix;
}


csr_sparse parse_csr_sparse(char *fname) {

  csr_sparse ret;
  fstream reader(fname);
  string line;
  unsigned int m, n, s;
  unsigned int first, second;
  double third;
  ret.shape =  (unsigned int*) malloc(sizeof(unsigned int) * 2);

  // first line is just a comment.
  //reader >> fake;
  // getline( reader, line );


  auto start = chrono::system_clock::now();

  reader >> m >> n >> s;

  cout << "sparse: " << fname << "\nrows: " << m << "\ncolumns: " << n << "\nsize: " << s <<"\n\n";

  ret.shape[0] = m;  
  ret.shape[1] = n;
  ret.size = s;
  ret.indptr = (unsigned int*) malloc(sizeof(unsigned int) * (ret.shape[0] + 1));
  ret.indices = (unsigned int*) malloc(sizeof(unsigned int) * (ret.size));
  ret.data = (double*) malloc(sizeof(double) * (ret.size));
  
  ret.indptr[0] = 0;
  cout << "length of array:" << ret.size << "\n\n";
  
  for (unsigned int i = 0; i < ret.size; i++ ) {

    reader >> first >> second >> third;
    //if (i <20 ){
    // cout << "reading element " << i << ":" << third  << "\n\n";
    // cout << "print first second third:" << first << "\t" << second << "\t" << third << "\n\n";
    // }
    ret.indptr[first+1]++;
    ret.indices[i] = second;
    ret.data[i]=third;
  }
  for (unsigned int j =1; j< ret.shape[0]+1; j++) {
    ret.indptr[j] += ret.indptr[j-1];
  }
  
  printf("reading %% 100.00 finished\n");

  //for (unsigned int j =0; j< ret.size; j++) {
  // cout<< "j="<< j << ", data[j]:\t"<< ret.data[j] << "\n\n";
  //  cout<< "\t\t indices[j]:\t"<< ret.indices[j] << "\n\n";
  //}

  //for (unsigned int j =0; j< ret.shape[0]+1; j++) {
  //  cout<< "indptr[i] for i=" << j << ":\t" << ret.indptr[j] << "\n\n";
  //}

  
  //cout << "first 5 elements of indices array:" << ret.indices[0] << "\t" << ret.indices[1] <<  "\t" << ret.indices[2] <<  "\t" << ret.indices[3] <<  "\t" << ret.indices[4] << "\n\n";
  //cout << "first 5 elements of indptr array:" << ret.indptr[0] <<  "\t" << ret.indptr[1] <<  "\t" << ret.indptr[2] <<  "\t" << ret.indptr[3] <<  "\t" << ret.indptr[4] << "\n\n";
  //cout << "first 5 elements of data array:" << ret.data[0] <<  "\t" << ret.data[1] <<  "\t" << ret.data[2] <<  "\t" << ret.data[3] <<  "\t" << ret.data[4] << "\n\n";

  auto end = std::chrono::system_clock::now();
  chrono::duration<double> elapsed_seconds = end-start;
  cout << "Reading sparse matrix elapsed time: " << elapsed_seconds.count() << "s\n";
  
  return ret;
}


void clean_csr_sparse(csr_sparse in) {
  free(in.indices);
  free(in.indptr);
  free(in.data);
  free(in.shape);
  //free(in.size);
}


void _kernel_(csr_sparse G, double * M, csr_sparse result) {
  int col = 0;
  unsigned int counter = 0;
  for (int i = 0; i < 5; i++) {
    cout <<  "indptr[i] for i=" << i << ":\t" << G.indptr[i] << "\n\n";
  }

  for (int i = 0; i < 4; i++) {
    cout <<  "data[i] for i=" << i << ":\t" << G.data[i] << "\n\n";
    cout <<  "indices[i] for i=" << i << ":\t" << G.indices[i] << "\n\n";
    
  }

  
  for (int i = 0; i < result.shape[0]; i++) {
    int offset = G.indptr[i+1]-G.indptr[i];
    for (int j = 0; j < offset; j++) {
      col = G.indices[counter];
      result.data[counter] = G.data[counter] * M[i*G.shape[1]+col];
      result.indices[counter] = col;
      counter++;
    }
  }
}

int main(int argc, char** argv) {

  char *sparse_fname, *dense_fname;
  csr_sparse G;
  double* M;
  
  assert(argc == 3);
  sparse_fname = argv[1];
  dense_fname = argv[2];
  

  G = parse_csr_sparse(sparse_fname);
  M = parse_dense_matrix(dense_fname);

  csr_sparse result;
  result.shape = G.shape;  
  result.size = G.size;
  result.indptr = G.indptr;
  result.indices = (unsigned int*) malloc(sizeof(unsigned int) * (result.size));
  result.data = (double*) malloc(sizeof(double) * (result.size));
  result.indptr[0] = 0;


  printf("\n\nstarting kernel\n");
  auto start = chrono::system_clock::now();

  _kernel_(G, M, result);

  printf("\nending kernel");
  auto end = std::chrono::system_clock::now();
  chrono::duration<double> elapsed_seconds = end-start;
  cout << "\nkernel computation time: " << elapsed_seconds.count() << "s\n";
  

  #if defined(OUTPUT_RET)
  ofstream outfile1;
  outfile1.open ("out_indptr.txt");
  for (int i = 0; i < result.shape[0]+1; i++) {
    outfile1 << result.indptr[i] << "\n";
  }
  outfile1.close();


  ofstream outfile2;
  outfile2.open ("out_indices.txt");
  for (int i = 0; i < result.size; i++) {
    outfile2 << result.indices[i] << "\n";
  }
  outfile2.close();

  ofstream outfile3;
  outfile3.open ("out_data.txt");
  for (int i = 0; i < result.size; i++) {
    outfile3 << result.data[i] << "\n";
  }
  outfile3.close();
  

  #endif
  //  
  delete M;
  // clean_csr_sparse(G);
  // clean_csr_sparse(result);
  //delete G;
  //delete result;
  ////free(G);
  ////free(result);
  //return 0;
}

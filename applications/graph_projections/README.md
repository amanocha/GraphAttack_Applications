# Graph Projections 

Graph projections is a graph algorithm that takes a bipartite graph as input, and relates nodes in one partition based on neighbors they share in the other partition. 

For more information on the algorithm, see https://en.wikipedia.org/wiki/Bipartite_network_projection.

## Gathering the Data

1. Select a dataset from /_data/graph_projections. These datasets come from http://konect.uni-koblenz.de/downloads/ (see below for details). 
2. Locate the out.* file in your dataset of choice and navigate back to the graph projections directory (this directory) and to the utils/ directory:

        cd /decades/applications/graph_projections/utils
        
3. Run the following:

        ./complete_flow.sh /_data/graph_projections/[dataset]/out.[dataset out.* filename]

4. Navigate back to the dataset directory. You should now have x_to_y_graph.txt and y_to_x_graph.txt edgelist files, which are the bipartite graphs from the dataset. DECADES kernels can run on either. 

## Example Datasets

- Small: http://konect.uni-koblenz.de/downloads/tsv/brunson_revolution.tar.bz2
- Also pretty small (probably a good one to simulate on): http://konect.uni-koblenz.de/downloads/tsv/moreno_crime.tar.bz2
- Medium (simulate on this one if you feel brave!): http://konect.uni-koblenz.de/downloads/tsv/opsahl-collaboration.tar.bz2
- Pretty big: http://konect.uni-koblenz.de/downloads/tsv/dbpedia-writer.tar.bz2
- Even bigger: http://konect.uni-koblenz.de/downloads/tsv/youtube-groupmemberships.tar.bz2

## Compiling Graph Projections

There are 2 variants of the algorithm:

- Bit Flag (gp_bit_flag): a projection with a binary edge
- Counter (gp_count): a projection that counts how many times the relation was seen

-----

Each variant contains three directories:

- baseline: a standard version of the algorithm that can be compiled with g++ or DEC++ "n" (native) mode

        g++ -O3 -std=c++11 main.cpp -o main
        
  or 

        DEC++ -m n main.cpp

  which generates an executable `decades_native/native`.
  
- decades: a multithreaded parallel version of the algorithm that can be compiled with DEC++ "db" (decades base) or "di" (decades decoupled implicit) mode and a set number of threads

        DEC++ -m [mode] -t [num_threads] main.cpp 

  which generates an executable `decades_base/decades_base` (decades base) or `decades_decoupled_implicit/decades_decoupled_implicit` (decades decoupled implicit).
  
- decades_bit_serial: a SIMD parallel version of the algorithm that can be compiled with DEC++ "b" (biscuit) mode

        DEC++ -m b -s [sync mode] -sps [scratchpad size] main.cpp
        
  where `sync mode` is either 0 to run kernel and biscuit computation asynchronously (faster) or 1 to run kernel and biscuit computation synchronously (slower), and `scratchpad size` is the size of the local scratchpad in biscuit (default is 8192 bytes). An executable `decades_biscuit/decades_biscuit` is generated.
  
For more details on the compiler and its compilation modes, see [1] in the documentation repository.

## Running Graph Projections

If you compiled one of our variants (any main.cpp file) with DEC++, you only need to input one graph to run the executable, depending on which direction of projection (x or y) you want

        ./decades_exec <PATH_TO_DATA>/x_to_y_graph.txt
        
  or
        
        ./decades_exec <PATH_TO_DATA>/y_to_x_graph.txt

## Interpreting The Results

If you compiled with "n" (native) or "db" (decades base) mode, then you will see output similar to the following (the graph information will be different depending on which dataset you decide to use):

        graph: ../../data/youtube-groupmemberships/y_to_x_graph.txt
        edges: 293360
        x_graph_nodes: 30087
        y_graph_nodes: 94238

        Running kernel
        Elapsed time: 3.65026s
        Finished hash: 66399082.000
        
This output highlights how many nodes are in each of the graph partitions (x and y), how long the kernel takes to run, and the hash (used to verify that the program is running correctly). Note: you should see the same hash for different DEC++ variants if they are run on the same input (i.e. Youtube y-to-x projection).

-----

If you compiled with "di" (decades decoupled implicit) mode, then you will see output similar to the following (with dataset differences in mind):

        graph: ../../data/youtube-groupmemberships/y_to_x_graph.txt
        edges: 293360
        x_graph_nodes: 30087
        y_graph_nodes: 94238
        
        Running kernel
        Elapsed time: 119.813s
        finished hash: 66399082.000
        
        
        -----
        decoupled runtime information:
        -----
        total predicate swaps: 0
        
        -----
        total stores: 66399082
          stores i32    : 66399082
          stores i64    : 0
          stores ptr    : 0
          stores float  : 0
          stores double : 0

        -----
        total loads: 133121616
          loads i32    : 133121613
          loads i64    : 1
          loads ptr    : 2
          loads float  : 0
          loads double : 0
        
        -----
        total opt. loads: 66399082 (33.28%)
          opt. loads i32    : 66399082 (33.28%)
          opt. loads i64    : 0 (0.00%)
          opt. loads ptr    : 0 (0.00%)
          opt. loads float  : 0 (0.00%)
          opt. loads double : 0 (0.00%)

You will see the same graph outputs from before, but you will also see decoupling information, including how many stores, loads, and optimized loads (terminal loads) took place, and the data types that these memory accesses operated on.

-----

If you compiled with "b" (biscuit) mode, then you will see output similar to the following (with dataset differences in mind):

        graph: ../../data/youtube-groupmemberships/y_to_x_graph.txt
        edges: 293360
        x_graph_nodes: 30087
        y_graph_nodes: 94238

        Running kernel
        Elapsed time: 4.23129s
        Finished hash: 66399082.000
        
        ------
        Bit Serial Stats:
        -
        Total # of items sent to bit serial: 66399082
        Sent in N batches: 81625
        Average size of batch: 813.47
        Max size of batch: 1024
        Min size of batch: 1
        Total amount of time compute spends waiting: 3.46
        Average amount of time compute spends waiting: 0.037
        Total amount of time spent on memcpy: 0.04
        ------

You will see the same graph outputs from before, but you will also see biscuit information, include how many computations were sent to the bit-serial processor, how many batches of computation were sent, the average size of these batches, and the smallest and largest batch sizes. You will also see the total and average amount of time that the computation kernel spends waiting for bit-serial batch computation, as well as the total amount of time that biscuit spends transferring data from the computation kernel to its scratchpad.

## Python Implementation

Navigate to the `gp_python/` folder to learn about this implementation.

## Demo

For a video demonstration detailing this application and how to compile and run it with DEC++, see https://youtu.be/vGHEbp-VaIc

## References
 [1] DECADES_Doc_and_Specs.pdf

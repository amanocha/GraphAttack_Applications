# FAST-LLAMAs

This repository contains 3 main directories:
1. **applications**: C++ benchmarks used to evaluate FAST-LLAMAs
2. **graphit_frontend**: frontend files from [GraphIt](https://graphit-lang.org/)
3. **utils**: vertex programmable application common files and dataset conversion scripts to generate binary files

The DECADES compiler, [DEC++](https://github.com/PrincetonUniversity/DecadesCompiler), was use to compile these applications. This compiler is coupled with the DECADES simulator, [MosaicSim](https://github.com/PrincetonUniversity/MosaicSim), which was used to evaluate FAST-LLAMAs by providing performance estimates.

## Applications

**Elementwise Sparse-Dense (EWSD)**: Multiplication between a sparse and a dense matrix. \
**Bipartite Graph Projections (GP)**: Relate nodes in one partition based on common neighbors in the other.

##### Vertex-programmable (VP) graph processing primitives:

**Breadth-First Search (BFS)**: Determine the distance (number of node hops) to all nodes. \
**Single-Source Shortest Paths (SSSP)**: Determine the shortest distance (sum of path edge weights) to all nodes. \
**PageRank (PR)**: Determine node ranks based on the distributed ranks of neighbors.

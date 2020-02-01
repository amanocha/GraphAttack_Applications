# Vertex Nomination:

## Algorithm

Given a graph and a set of "seed" vertices as input, the goal of the vertex nomination algorithm is to find similar vertices. In order to acheve this, the algorithm combines two different pieces of statistical information on vertices of a graph:

1. Context : The distance to seed vertices
2. Content : A variety of node attributes

After generating a score for each of these statistics, the two scores can then be combined in different ways (addition, multiplication, etc.)

Read more about the algorithm here: https://arxiv.org/abs/1201.4118

Here we provide the original application provided to us (SDH_main.py), which uses the snap software package, as well as the DECADES version with algorithmic improvements (vertex_nomination.py). This version can be compiled with Numba and has the capability to have DEC++ in its compilation pathway.

## Running Vertex Nomination

The default data path points to the provided data folder, so a data path input (edgelist) is optional. Here is how to run the two versions via the command line:

DECADES:

    python3.7m vertex_nomination.py [PATH_TO_DATA_INPUT]
    

Original:

    python2 SDH_main.py [PATH_TO_DATA_INPUT]

## Demo

For a video demonstration detailing this application and how to compile and run it with DEC++, see https://youtu.be/cilW-gVaMsc

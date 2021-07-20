# Distance Vector Routing Protocol - Simulation

This project demonstrates (superficially) the evolution of routing tables at points on a network. These tables successfully and correctly converge upon shortest paths across networks where edges are positively weighted. 

## Issues

At present the simulator does not cope well wth 'negative distances', running into a 'count-to-infinity' problem. An implementation of the *split horizon* mode goes some way towards mitigating this problem but further work is required.

In some networks with negatively weighted edges, stability can be achieved with the commands which allow for changing and deletion of edges during simulations. The ‘view path’ operation also works accurately, identifying the best route between nodes (except in a few edge cases where it loops infinitely).

## Usage

Networks are described by simple .txt files - the first line is a space-separated sequence of nodes on the network, and each subsequent line describes a weighted, undirected edge between two nodes. Examples can be found in this repository. Simply run the Python script and enter the path to a .txt file to begin a simulation.

import random
import numpy as np


def randomwalk(edges, a, iters):

    # Histogram to return
    histogram = [0, 0, 0, 0, 0, 0, 0]

    # Set including all possible starting nodes
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])

    # Start at random node
    current_node = random.sample(nodes, 1)[0]

    # Iterate
    for _ in range(iters):
        # Potential nodes list, will randomly pick from list later, to go to next node
        potential_nodes = []

        # Search through all edges to find nodes connecting to starting node
        for edge in edges:
            if (current_node == edge[0]):
                # Add to potential nodes collection 
                potential_nodes.append(edge[1])

        # Probability to not randomly teleport
        if random.random() > a:
            # Pick a random node to visit next from current node
            current_node = random.choice(potential_nodes)
        # Else teleport to random page
        else:
            # Pick a random node
            current_node = random.sample(nodes, 1)[0]

        # Add visted node to histogram
        histogram[current_node] = histogram[current_node] + 1

    # Loop through histogram values to normalize values from 0 to 1
    total = (sum(histogram))
    for index, value in enumerate(histogram):
        histogram[index] = round(value/total, 6) # Round to 6dp

    # Return histogram result
    return histogram


def pagerank(edges, a, iters):

    # Set of all nodes (0-6)
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])

    # Empty array
    P = np.empty((0,len(nodes)), float)

    # Iterate through every node (0-6)
    # Calculate row of probabilities (to jump to from current node)
    for node in nodes:
        connecting_edges = []
        for edge in edges:
            # Find all nodes in given edges set
            if (node == edge[0]):
                # Add (the connecting edges) to a list
                connecting_edges.append(edge[1])

        l = []
        # Iterate through nodes again (0-6) to build row of jump probabilities (in list l)
        for n in nodes:
            # Connecting nodes have probability of '1-a'.
            # If 'a' was 10%, they'll have 90% probability combined
            if n in connecting_edges:
                x = (1 - a) / len(connecting_edges)
                l.append(x)
            # Non connecting nodes have probability of 'a' to add random teleportation
            # Both connecting and non-connecting together will have total probability of 1
            else:
                x = a / (len(nodes) - len(connecting_edges))
                l.append(x)

        # Add list 'l' to transition probability matrix as new row 
        P = np.append(P, np.array([l]), axis=0)

    # Probability vector (1/n)
    x = np.array([[1/len(nodes), 1/len(nodes), 1/len(nodes), 1/len(nodes), 1/len(nodes), 1/len(nodes), 1/len(nodes)]])

    # Iterate 'iters' times to find steady state, xP^iters
    for _ in range(iters):
        x = x.dot(P)
    
    # Return resulting vector
    return x[0]

# Webpages edges
edges = {(0, 2),(1, 1),(1, 2),(2, 0),(2, 2),(2, 3),(3, 3),(3, 4),(4, 6),(5, 5),(5, 6),(6, 4),(6, 6)}
# For Q4, add more outlinks from node 1
#edges = {(0, 2),(1, 0),(1, 1),(1, 2),(1, 3),(1, 4),(1, 5),(1, 6),(2, 0),(2, 2),(2, 3),(3, 3),(3, 4),(4, 6),(5, 5),(5, 6),(6, 4),(6, 6)}

# Function calls
print("Random Walk -", randomwalk(edges, 0.1, 10))
print("Page Rank -", pagerank(edges, 0.1, 100))

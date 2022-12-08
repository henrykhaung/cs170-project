import networkx as nx
import numpy as np
import os
import json
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from pathlib import Path
from tqdm.auto import tqdm
from starter import *

# does not work and is not completed: IGNORE
def k_(G: nx.Graph, k, D=None):
    if k == 1:
        for node in G.nodes:
            G.nodes[node]['team'] = 1
    elif k == 2:
        for node in G.nodes:
            if node in D:
                G.nodes[node]['team'] = 1
            else:
                G.nodes[node]['team'] = 2
    return score(G)

def if_even_D(G: nx.Graph, k, D, even):
    if even:
        D_nodes_per_team = len(D) // k # can |D| be 0 or 1 or 2?
        i, j = 0, D_nodes_per_team
        for team_id in range(1, k + 1):
            for node in D[i:j]:
                G.nodes[node]['team'] = team_id
            i, j = j, j + j
        return G
    else:
        D_nodes_per_team = len(D) // k
        remaining_D = len(D) % k
        i, j = 0, D_nodes_per_team
        for team_id in range(1, k + 1):
            for node in D[i:j]:
                G.nodes[node]['team'] = team_id
            i, j = j, j + j
        
        # for now just add the remaining r to the first r teams
        for team_id in range(1, remaining_D):
            # for node in D
            pass
        return G

# Find the dominating set D
# All the nodes in D will all be in one team and the rest will be in another team if k == 2
# if k == 1, D does not matter
# for k > 2, try to evenly split |D| and put them into different teams
# Once done, start with the team 1 and its nodes:
#       dfs/bfs greedily through their neighbors (these neighbors should not be in D)
#       decide which team besides team 1/current team to put these neighbor nodes in
# After this, might have to check whether the teams are even or not:
#       find how many teams there are (should be easy)
#       find sizes of each team
#       redistribute nodes to get roughly even teams if possible
def solve_(G: nx.Graph):
    """Assign: G.nodes[v]['team'] = team_id
       Access: team = G.nodes[v]['team']"""
    D = list(nx.dominating_set(G))
    V = G.number_of_nodes()
    min_cost = k_(G.copy(), 1)                   # k == 1
    min_cost = min(min_cost, k_(G.copy(), 2), D) # k == 2
    # k >= 3
    possible_k = list(range(3, 2 * math.ceil(V**(1/2))))
    for k in possible_k:
        G_copy = G.copy()
        # if D evenly divisible or not, 
        # ALSO: it could be possible that some D nodes share disputes (add later)
        if len(D) % k == 0:
            G_copy = if_even_D(G_copy, k, D, True)
        else:
            G_copy = if_even_D(G_copy, k, D, False)
        # assign neighbors to teams as well

        


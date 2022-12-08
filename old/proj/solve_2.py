import networkx as nx
import numpy as np
import os
import json
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from pathlib import Path
from tqdm.auto import tqdm
import tarfile
from starter import *

# Idea: sort nodes by max degree, perform DFS, sort neighboring edges by max weight, assign current node to the minimum neighboring team
# Scores:  small = 6849.769492693513
#         medium = 4730.799291193902
#          large = 35264.476756954864
# Note: optimal k does not necessarily have to divide evenly into V ? (could also imply k's that divide V could be even more optimal)
#       worst performing tests have huge third term
# Questions: Where to stop k? (upper-bound for possible k ?)
#            Can min_cost decrease after increasing ? (ie. can min_cost have multiple local minimums instead of being "quadratic" ?)
def solve_2(G: nx.Graph):
    V = G.number_of_nodes()
    possible_k = list(range(1, 2*math.ceil(V**(1/2)))) # OPTIMIZE: what upper-bound to use for k?
    # possible_k = list(range(1, V))
    min_cost = float('inf')
    min_G = G.copy()
    
    for k in possible_k:
        G_copy = G.copy()
        nodes = sorted(G_copy.degree(weight="weight"), key=lambda x: x[1])
        stack = [i[0] for i in nodes]
        
        while stack:
            curr = stack.pop()
            edges = sorted(G_copy.edges(curr, data=True), key=lambda t: t[2].get('weight', 1), reverse=True)
            adj_team_counter = {i:0 for i in range(1, k+1)}
            for i in edges:
                neighbor = i[1]
                if "team" in G_copy.nodes[neighbor]:
                    adj_team_counter[G_copy.nodes[neighbor]["team"]] += i[2]["weight"]
            smallest_team = min(adj_team_counter, key=adj_team_counter.get)
            G_copy.nodes[curr]["team"] = smallest_team
        
        curr_cost = score(G_copy)
        if curr_cost <= min_cost:
            min_cost = curr_cost
            min_G = G_copy.copy()

    for i in min_G.nodes:
        G.nodes[i]['team'] = min_G.nodes[i]['team']
    return

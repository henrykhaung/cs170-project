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

# CLEAN VERSION
from itertools import combinations
import math

def solve_clean(G: nx.Graph) -> None:
   V = G.number_of_nodes()

   possible_k = [i for i in range(1, math.ceil(math.sqrt(V + 1)))]
   # possible_k = [i for i in range(1, V + 1) if V % i == 0]
   min_cost = float('inf')
   min_G = G.copy()

   best_teams = None
   # print('possible_k', possible_k)
   for k in possible_k:
      G_copy = G.copy()
      # all nodes are unassigned at first (unassigned teamid = 0)
      for i in range(G_copy.number_of_nodes()):
         if "team" not in G_copy.nodes[i]:
            G_copy.nodes[i]["team"] = 0

      nodes = sorted(G_copy.degree(weight="weight"), key=lambda x: x[1]) # sort all nodes by a node's sum of edges
      visited = [False] * V
      max_degree_node = nodes.pop()[0]
      # stack = [max_degree_node]
      stack = [i[0] for i in nodes]
      
      teams = set()

      while len(stack) != 0:
         curr = stack.pop()
         neighbors = G_copy.neighbors(curr) # neighbors = iterator

         # remove neighboring teams from possible teams
         # then set current node's team to the smallest team from non-neighboring teams
         if not visited[curr]:
            adj_team_counter = {i:0 for i in range(1, k+1)} # {teamid, num of nodes in team}
            for i in neighbors:
               if G_copy.nodes[i]['team'] != 0: # if neighbor node has a team
                  adj_team_counter[G_copy.nodes[i]["team"]] += 1

               if not visited[i]:
                  stack.append(i)

            smallest_team = min(adj_team_counter, key=adj_team_counter.get)
            G_copy.nodes[curr]["team"] = smallest_team
            teams.add(smallest_team)
               
            visited[curr] = True


      curr_cost = score(G_copy)
      if curr_cost <= min_cost:
         min_cost = curr_cost
         min_G = G_copy.copy()
         best_teams = teams

   # print(best_teams)
   teamid_nodes = {}
   for i in min_G.nodes:
      team_id = min_G.nodes[i]['team']
      if team_id not in teamid_nodes:
         teamid_nodes[team_id] = [i]
      else:
         teamid_nodes[team_id].append(i)
      
   # print(teamid_nodes)
   # print(len(teamid_nodes))
   # print(len(teamid_nodes[1]), len(teamid_nodes[2]))
   # for i in range(1, len(teamid_nodes)):
   #    print('len ', i, ' ',len(teamid_nodes[i]))
   
   # if there are unassigned teams, assign them greedily
   print(teamid_nodes)
   if 0 in teamid_nodes:
      G_copy = min_G.copy()
      unassigned_nodes = teamid_nodes[0]
      teams = [i for i in range(1, len(teamid_nodes))]
      print('teams ', teams)
      possibles = list(combinations(teams, len(unassigned_nodes)))
      print(f'possibles: {possibles}')
      # find best combination
      prev_cost = [None, score(min_G)]
      for team_ids in possibles:
         for unassigned_node, team_id in zip(unassigned_nodes, team_ids):
            G_copy.nodes[unassigned_node]['team'] = team_id
         
         combination_score = score(G_copy)
         if combination_score < prev_cost[1]:
            prev_cost = [team_ids, combination_score]

         print("prev_cost ", prev_cost)
      
      # assign best teams for the unassigned
      print("final prev_cost ", prev_cost)
      for unassigned_node, team_id in zip(unassigned_nodes, prev_cost[0]):
         G_copy.nodes[unassigned_node]['team'] = team_id

      min_G = G_copy.copy()
      
   # print(teamid_nodes)

   for i in min_G.nodes:
      G.nodes[i]['team'] = min_G.nodes[i]['team']
   return
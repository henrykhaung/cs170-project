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

def get_cluster(G: nx.Graph) -> nx.Graph:
   """
   Input G should be a copy, we should not modify the original graph
   if check, return G; else, separate into clusters and return those
   """
   def check(G: nx.Graph, E: set):
      """Needs more than 1/2 of nodes to cluster"""
      return len(E) > G.number_of_nodes() / 2

   
   E = nx.algorithms.connectivity.cuts.minimum_edge_cut(G)
   if not check(G, E):
      # remove edges in E
      for e in E:
         G.remove_edge(e)
      clusters = [G.subgraph(c).copy() for c in nx.connected_components(G)]
      if len(clusters) == 2:
         res = get_cluster(clusters[0])
         res1 = get_cluster(clusters[1])

         G = nx.compose(res, res1)
   
   return G

from itertools import combinations
import math

def solve_1(G: nx.Graph):
   # TODO implement this function with your solver
   # Assign a team to v with G.nodes[v]['team'] = team_id
   # Access the team of v with team_id = G.nodes[v]['team']
   """
   1. We would like the tournament to resolve disputes, 
      so it is best to put disputing penguins on different teams.
   2. There should be as few teams as possible, so the tournament can be over quickly.
   3. Teams should be roughly equal in size, so no team has a competitive advantage.

   group/cluster nodes with a lot of disputes
   """
   # G_copy = get_cluster(G.copy())
   # sub_graphs = [G.subgraph(c).copy() for c in nx.connected_components(G_copy)]
   # labels = np.zeros(shape=(len(G)), dtype=np.uint16)

   # for _class, _cluster in enumerate(sub_graphs, 1):
   #    c = list(_cluster.nodes)
   #    labels[c] = _class

   # print(labels)

   V = G.number_of_nodes()
   # for line in nx.gener
   # for u, v in G.edges:
      # print(u, v, " ", G.edges[u, v]['weight'])
   # for i in range(math.ceil(math.sqrt(V))):


def solve(G: nx.Graph) -> None:
   # TODO implement this function with your solver
   # Assign a team to v with G.nodes[v]['team'] = team_id
   # Access the team of v with team_id = G.nodes[v]['team']
   V = G.number_of_nodes()

   # possible_k = [i for i in range(2, int((V ** (1/2) + 1))) if V % i == 0] # OPTIMIZE: STOP AT |V| OR rad(|V|) ?
   # possible_k = [i for i in range(1, V + 1) if V % i == 0]
   possible_k = [i for i in range(1, math.ceil(math.sqrt(V + 1)))]
   min_cost = float('inf')
   min_G = G.copy()

   ###________TRY_POPPING_NODES_BY_MAX_DEGREE_INSTEAD_OF_EDGES_BY_MAX_WEIGHT______###
   best_teams = None
   print('possible_k', possible_k)
   for k in possible_k:
      G_copy = G.copy()
      # all nodes are unassigned at first (unassigned teamid = 0)
      for i in range(G_copy.number_of_nodes()):
         if "team" not in G_copy.nodes[i]:
            G_copy.nodes[i]["team"] = 0

      p = V // k # is never used?
      nodes = sorted(G_copy.degree(weight="weight"), key=lambda x: x[1]) # sort all nodes by a node's sum of edges
      visited = [False] * V
      max_degree_node = nodes.pop()[0]
      # stack = [max_degree_node]
      stack = [i[0] for i in nodes]
      
      teams = set()

      while len(stack) != 0:
      # while not all(visited):
         curr = stack.pop()
         # print(f'curr node {curr}')
         neighbors = G_copy.neighbors(curr) # neighbors = iterator

         # remove neighboring teams from possible teams
         # then set current node's team to the smallest team from non-neighboring teams
         if not visited[curr]:
            adj_team_counter = {i:0 for i in range(1, k+1)} # {teamid, num of nodes in team}
            for i in neighbors:
               # print(f"iteration: {k} and {G_copy.nodes[i]['team']}")
               if G_copy.nodes[i]['team'] != 0: # if neighbor node has a team
                  adj_team_counter[G_copy.nodes[i]["team"]] += 1

               if not visited[i]:
                  stack.append(i)

            # decide which team to put current node in
            # put node in each possible team and compute cost
            # then choose the smallest cost team
            # smallest_team = min(adj_team_counter, key=adj_team_counter.get)
            # G_copy.nodes[curr]["team"] = smallest_team
            # cost = score(G_copy)
            # for team_id, count in adj_team_counter.items():
            #    G_copy.nodes[curr]['team'] = team_id
            #    team_score = score(G_copy)
            #    if team_score < cost:
            #       cost = team_score
            #       smallest_team = team_id
            
            # G_copy.nodes[curr]['team'] = smallest_team
            # teams.add(smallest_team)

            smallest_team = min(adj_team_counter, key=adj_team_counter.get)
            G_copy.nodes[curr]["team"] = smallest_team
            teams.add(smallest_team)

            # curr_cost = score(G_copy)
            # redistribute teams?, assign curr node to team with no nodes instead of team with min nodes
            # for team_id, count in adj_team_counter.items():
            #    if count == 0:
            #       G_copy.nodes[curr]['team'] = team_id
            #       newteam_cost = score(G_copy)
            #       break
            # # if assigning to new team is better, assign to that team
            # # if not, assign to team with min nodes
            # if curr_cost < newteam_cost:
            #    G_copy.nodes[curr]["team"] = smallest_team
            #    teams.add(smallest_team)
            # else:
            #    teams.add(team_id)
               
            visited[curr] = True

      # print(f'iteration: {k} and teams: {teams}')

      curr_cost = score(G_copy)
      # print(f'k is: {k} and curr_cost: {curr_cost}')
      if curr_cost <= min_cost:
         min_cost = curr_cost
         min_G = G_copy.copy()
         best_teams = teams

   print(best_teams)
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
   if 0 in teamid_nodes:
      G_copy = min_G.copy()
      unassigned_nodes = list(teamid_nodes[0])
      teams = [i for i in range(1, len(teamid_nodes))]
      possibles = list(combinations(teams, len(unassigned_nodes)))

      # find best combination
      prev_cost = [None, score(min_G)]
      for team_ids in possibles:
         for unassigned_node, team_id in zip(unassigned_nodes, team_ids):
            G_copy.nodes[unassigned_node]['team'] = team_id
         
         combination_score = score(G_copy)
         if combination_score < prev_cost[1]:
            prev_cost = [team_ids, combination_score]
      
      # assign best teams for the unassigned
      for unassigned_node, team_id in zip(unassigned_nodes, prev_cost[0]):
         G_copy.nodes[unassigned_node]['team'] = team_id

      min_G = G_copy.copy()
      
   print(teamid_nodes)

   for i in min_G.nodes:
      G.nodes[i]['team'] = min_G.nodes[i]['team']
   return
   
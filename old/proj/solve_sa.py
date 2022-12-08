import networkx as nx
import random
from starter import *
from greedy import *
from simulated_annealing import *

# solve_2hard is a solution with hardcoded solutions for bipartite solutions
# Idea: sort nodes by max degree, perform DFS, sort neighboring edges by max weight, 
#       assign current node to the minimum neighboring team


def solve_sa_main(G: nx.Graph):
    """Simulated Annealing solution"""
    # def initial_temp(G: nx.Graph):
    #     V = G.number_of_nodes()
    #     # list(range(1, 2*math.ceil(V**(1/2))))
    #     # return (2 * math.ceil(V**(1/2)))
    #     return V

    def initial_solution(G: nx.Graph):
        """
        # randomly choose a partition number k (1 to |V|) and
        # make a graph (does not have to be optimal)
        # This means this function will make teams randomly
        #   ie randomly assign each node a team but each team will at least have one node
        #   if k == |V| is an edge case
        # Since we cannot just randomly assign teams (this can possibly get us teams with no members),
        # we record which teams the nodes are randomly assigned to.
        # Then, after all nodes are assigned, we check if there are teams with no members;
        # if there are teams with no members, we randomly pick from teams with at least 2 members and
        # reassign them to these teams.
        
        # returns Graph and number of teams/partitions
        """

        k = random.randint(2, G.number_of_nodes()) # should not start with 1 since neighbor operator needs at least 2 teams for swap
        teams = {i: [] for i in range(1, k + 1)}
        G_copy = G.copy()
        for node in G_copy:
            id = random.randint(1, k)
            G_copy.nodes[node]['team'] = id
            teams[id].append(node)

        # find teams with no members if any
        teams_with_0 = []
        teams_with_2more = {}
        for id in teams:
            if teams[id] == []:
                teams_with_0.append(id)
            elif len(teams[id]) >= 2:
                teams_with_2more[id] = teams[id]
        
        if not teams_with_0:
            return G_copy, len(teams)
        else:
            # randomly choose from teams with 2 or more
            # from that team, randomly choose teammates
            reassign_nodes = []
            amount_choose = len(teams_with_0)
            while amount_choose:
                id = random.choice(list(teams_with_2more.keys()))
                reassign = random.choice(teams_with_2more[id])
                reassign_nodes.append((id, reassign))
                
                if len(teams_with_2more[id]) >= 1:
                    teams_with_2more[id].remove(reassign)
                    if len(teams_with_2more[id]) == 0:
                        del teams_with_2more[id]

                amount_choose -= 1

            # reassign nodes and assign same teams to nodes
            G_copy = G.copy()
            for id, node in reassign_nodes:
                G_copy.nodes[node]['team'] = id
            for id in teams_with_2more:
                for node in teams_with_2more[id]:
                    G_copy.nodes[node]['team'] = id
            
            return G_copy, len(get_teams(G_copy))

    def get_teams(G: nx.Graph):
        teams = {}
        for node in G.nodes:
            # print(f"G.nodes[node]['team']:   {G.nodes[node]}")
            if not G.nodes[node]: # no team is originally assigned, there should be no team 0's though..
                teams[0] = [node]
            else:
                id = G.nodes[node]['team']
                if id not in teams:
                    teams[id] = [node]
                else:
                    teams[id].append(node)
        return teams
    
    def neighbor_operator(G: nx.Graph):
        """
        Randomly choose whether to increase or decrease partitions by 1.
        Make sure graph is changed accordingly. There should be at least 1 member for each team.
        """
        change = random.randint(0, 1)
        G_copy = G.copy()
        teams = get_teams(G_copy)
        if change:
            # choose a random team to add
            available_teams = []
            for i in range(1, max(list(teams.keys()))):
                if i not in teams:
                    available_teams.append(i)
            add_teamid = random.choice(available_teams)

            # randomly choose how many nodes to add to new team
            # there should be at least 1
            teams_withatleast2 = []
            for i in teams:
                if len(teams[i]) >= 2:
                    teams_withatleast2.append(i)
            add_fromteam = random.choice(teams[random.choice(teams_withatleast2)])
            G_copy.nodes[add_fromteam]['team'] = add_teamid
            
            print("add")
            visualize(G_copy)
        else:
            # choose a random team to get rid of/
            available_teams = []
            for i in range(1, max(list(teams.keys()))):
                if i in teams:
                    available_teams.append(i)
            remove_teamid = random.choice(available_teams)
            remove_fromteam = teams[remove_teamid]

            # randomly choose a team to add the soon-to-be-removed team's nodes to
            available_teams.remove(remove_teamid)
            reassign = random.choice(available_teams)
            for node in remove_fromteam:
                G_copy.nodes[node]['team'] = reassign

            print("remove")
            visualize(G_copy)

        return G_copy

    # def neighbor_operator(G: nx.Graph, amount=1):
    #     # just randomly swap two penguins each from different teams
    #     # create a new graph based on this^ for an arbritary amount
    #     # when swapping,
        
    #     swapped_graphs = []
    #     teams = get_teams(G)
    #     swapped_node = []
    #     while amount:
    #         # randomly find nodes to swap
    #         G_copy = G.copy()
    #         swap_teams = random.sample(list(teams.keys()), 2)
    #         team_1 = swap_teams[0]
    #         team_2 = swap_teams[1]
    #         swap_node1 = random.choice(teams[team_1])
    #         swap_node2 = random.choice(teams[team_2])
            
    #         # ensure we are not swapping duplicate nodes
    #         team_keys = list(teams.keys())
    #         # may have to consider the edge case where there are odd number of teams before and after removal
    #         # as well as after amount variable is decreased
    #         # for now, keep amount variable small
    #         while ((swap_node1, swap_node2) in swapped_node or (swap_node2, swap_node1) in swapped_node):
    #             team_keys.remove(team_1)
    #             team_keys.remove(team_2)

    #             swap_teams = random.sample(team_keys, 2)
    #             team_1 = swap_teams[0]
    #             team_2 = swap_teams[1]
    #             swap_node1 = random.choice(teams[team_1])
    #             swap_node2 = random.choice(teams[team_2])

    #         swapped_node.append((swap_node1, swap_node2))
    #         swapped_node.append((swap_node2, swap_node1))

    #         # swap
    #         # print(f"swapping {G_copy[swap_node1]['team']}")
    #         G_copy.nodes[swap_node1]['team'] = team_2
    #         G_copy.nodes[swap_node2]['team'] = team_1
            
    #         swapped_graphs.append(G_copy)
    #         amount -= 1

    #     return swapped_graphs

        

    # only runs this once
    # should run this indefinitely and record the solutions and change if there is a better solution
    #   run all inputs and record their solutions
    #   run all inputs again and record their solutions wrt input number and if any of them is better, replace
    
    initialSolution, initialTemp = initial_solution(G)
    print(f"initial temp: {initialTemp} and initial solution visualized below")
    # print(f"initial teams = {get_teams(initialSolution)}")
    visualize(initialSolution)
    # initialTemp = initial_temp(G)
    finalTemp = 10
    tempReduction = "slowDecrease"
    iterationPerTemp = 100 * initialTemp #G.number_of_nodes() # arbritary number
    alpha = 1
    # res = neighbor_operator(initialSolution)
    # print(f"neighbor teams = {get_teams(res)}")
    sa = SimulatedAnnealing(initialSolution=initialSolution, solutionEvaluator=solve_greedy, initialTemp=initialTemp, finalTemp=finalTemp, tempReduction=tempReduction, neighborOperator=neighbor_operator, iterationPerTemp=iterationPerTemp, alpha=alpha)
    sol = sa.run()
    teams = get_teams(sol)
    for id in teams:
        for node in teams[id]:
            G.nodes[node]['team'] = id
    return
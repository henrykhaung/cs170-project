import random
from starter import *
from solve_2hard import *
from greedy import *
import math

class SimulatedAnnealing:
    def __init__(self, initialSolution, solutionEvaluator, initialTemp, finalTemp, tempReduction, neighborOperator, iterationPerTemp=100, alpha=10, beta=5):
        self.solution = initialSolution
        self.evaluate = solutionEvaluator
        self.currTemp = initialTemp
        self.finalTemp = finalTemp
        self.iterationPerTemp = iterationPerTemp
        self.alpha = alpha
        self.beta = beta
        self.neighborOperator = neighborOperator

        if tempReduction == "linear":
            self.decrementRule = self.linearTempReduction
        elif tempReduction == "geometric":
            self.decrementRule = self.geometricTempReduction
        elif tempReduction == "slowDecrease":
            self.decrementRule = self.slowDecreaseTempReduction
        else:
            self.decrementRule = tempReduction

    def linearTempReduction(self):
        self.currTemp -= self.alpha

    def geometricTempReduction(self):
        self.currTemp *= self.alpha

    def slowDecreaseTempReduction(self):
        self.currTemp = self.currTemp / (1 + self.beta * self.currTemp)

    def isTerminationCriteriaMet(self):
        # can add more termination criteria
        return self.currTemp <= self.finalTemp or self.neighborOperator(self.solution) == 0

    def run(self):
        G_copy = None
        while not self.isTerminationCriteriaMet():
            print("is this even working")
            # iterate that number of times
            for i in range(self.iterationPerTemp):
                # get all of the neighbors (return a list)
                neighbors = self.neighborOperator(self.solution)
                # pick a random neighbor
                newSolution = random.choice(neighbors)
                # get the cost between the two solutions
                old_graph, new_graph = self.evaluate(self.solution), self.evaluate(newSolution)
                cost = score(old_graph) - score(new_graph)
                # if the new solution is better, accept it
                if cost >= 0:
                    self.solution = newSolution
                    G_copy = new_graph
                    print(f"Current graph replaced with better one: {G_copy}")
                # if the new solution is not better, accept it with a probability of e^(-cost/temp)
                else:
                    print("new graph is worse")
                    if random.uniform(0, 1) < math.exp(-cost / self.currTemp):
                        self.solution = newSolution
                        G_copy = new_graph
            # decrement the temperature
            self.decrementRule()

        # return self.solution
        return G_copy
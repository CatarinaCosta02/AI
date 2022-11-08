# Catarina Costa -> nmec: 103696 

from tree_search import *
from cidades import *
from blocksworld import *


def func_branching(connections,coordinates):
    #IMPLEMENT HERE
    avg_number = 0
    count1 = 0
    count2 = 0
    count_total = 0

    cities = []
    for city in coordinates:
        cities.append(city)
    
    for city in coordinates:
        for (C1,C2,d) in connections:
            if city == C1:
                count1 += 1
            if city == C2:
                count2 += 1
    
    count_total = count1 + count2
    avg_number = (count_total/len(cities)) - 1

    return avg_number

class MyCities(Cidades):
    def __init__(self,connections,coordinates):
        super().__init__(connections,coordinates)
        # ADD CODE HERE IF NEEDED

class MySTRIPS(STRIPS):
    def __init__(self,optimize=False):
        super().__init__(optimize)

   

    def simulate_plan(self,state,plan):
        #IMPLEMENT HERE
        for action in plan:
            self.result(state,action)
            state = self.result(state,action)
        return state
        



        

 
class MyNode(SearchNode):
    def __init__(self,state,parent, cost = 0, heuristic = 0,depth = 0):
        super().__init__(state,parent)
        #ADD HERE ANY CODE YOU NEED
        self.cost = cost
        self.heuristic = heuristic
        self.depth = depth

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',optimize=0,keep=0.25): 
        super().__init__(problem,strategy)
        #ADD HERE ANY CODE YOU NEED
        self.optimize = optimize
        if self.optimize == 0:
            print('optimize = 0')
            root = MyNode(problem.initial, None)
        if self.optimize == 1:
            print('optimize == 1')
            #(state,parent,cost,heuristic,depth)
            root = (problem.initial, None, 0, 0, 0)
        
        if self.optimize == 2:
            print('optimize == 2')
            #(state,parent,cost,heuristic,depth)
            root = (problem[1], None, 0, 0, 0) 
        if self.optimize == 4:
            print('optimize == 4')
            root = (problem[1], None, 0, 0, 0)
                  
        self.all_nodes = [root]
        self.open_nodes = [0]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0
        self.keep = keep

    def astar_add_to_open(self,lnewnodes):
        # esta merda ainda nao esta a dar certa
        #IMPLEMENT HERE
        if self.optimize == 0:
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key= lambda n: self.all_nodes[n].cost + self.all_nodes[n].heuristic)
        else:
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key= lambda n: self.all_nodes[n][2] + self.all_nodes[n][3])

        
    def get_path(self,node):
        if isinstance(node,MyNode):
            return super().get_path(node)
        else:
            if node[1] == None:
                return [node[0]]
            path = self.get_path(self.all_nodes[node[1]])
            path += [node[0]]
            return(path)
        


    # remove a fraction of open (terminal) nodes
    # with lowest evaluation function
    # (used in Incrementally Bounded A*)
    def forget_worst_terminals(self):
        #IMPLEMENT HERE
        pass

    # procurar a solucao
    def search2(self):
        #IMPLEMENT HERE
        if self.optimize == 0:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node.state):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    if newstate not in self.get_path(node):
                        #print(node.cost,node.heuristic,node.depth)
                        newnode = MyNode(newstate,nodeID,node.cost + self.problem.domain.cost(node.state,a),self.problem.domain.heuristic(newstate, self.problem.goal),node.depth + 1)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)

                self.add_to_open(lnewnodes)
    

        if self.optimize == 1:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node[0]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node[0]):
                    newstate = self.problem.domain.result(node[0],a)
                    if newstate not in self.get_path(node):
                        newnode = (newstate,nodeID,node[2] + self.problem.domain.cost(node[0],a),self.problem.domain.heuristic(newstate, self.problem.goal),node[4] + 1)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)

        if self.optimize == 2:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem[0][4](node[0], self.problem[2]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):
                    newstate = self.problem[0][1](node[0],a)
                    if newstate not in self.get_path(node):
                        newnode = (newstate,nodeID,node[2] + self.problem[0][2](node[0],a),self.problem[0][3](newstate, self.problem[2]),node[4] + 1)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)

        if self.optimize == 4:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem[0][4](node[0], self.problem[2]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):
                    #if self.problem[0][4](node[0], self.problem[2]):
                    newstate = self.problem[0][1](node[0],a)
                    if newstate not in self.get_path(node):
                        #print(node.cost,node.heuristic,node.depth)
                        newnode = (newstate,nodeID,node[2] + self.problem[0][2](node[0],a),self.problem[0][3](newstate, self.problem[2]),node[4] + 1)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)

        return None
        

# If needed, auxiliary functions can be added

# function to be used in the exercise 5

def graph_search (self,problem,curent_state, target_state,visited = None):

    solution = []
    
    if self.visited == None:
        return []
    solution.append(curent_state)
    
    if curent_state == target_state:
        return solution

    for close_state in problem[curent_state]:
        if close_state not in solution:

            caminho = graph_search(problem,curent_state, target_state,visited)
            if caminho:
                return caminho

    #pass





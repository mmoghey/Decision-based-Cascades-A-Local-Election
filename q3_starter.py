################################################################################
# Starter code for Problem 3
# Author: yarora@stanford.edu, tonyekim@stanford.edu
# Last Updated: Oct 8, 2017
################################################################################

import snap
import matplotlib.pyplot as plt

# Setup
num_voters = 10000
decision_period = 10

def read_graphs(path1, path2):
    """
    :param - path1: path to edge list file for graph 1
    :param - path2: path to edge list file for graph 2
    
    return type: snap.PUNGraph, snap.PUNGraph
    return: Graph 1, Graph 2
    """
    ############################################################################
    # TODO: Your code here!
    Graph1 = snap.LoadEdgeList(snap.PUNGraph, path1, 0, 1)
    Graph2 = snap.LoadEdgeList(snap.PUNGraph, path2, 0, 1)
    ############################################################################
    return Graph1, Graph2


def initial_voting_state(Graph):
    """
    Function to initialize the voting preferences. 

    :param - Graph: snap.PUNGraph object representing an undirected graph
    
    return type: Python dictionary
    return: Dictionary mapping node ids to initial voter preference ('A', 'B', or 'U')
    
    Note: 'U' denotes undecided voting preference. 

    Example: Some random key-value pairs of the dict are {0 : 'A', 24 : 'B', 118 : 'U'}.
    """
    voter_prefs = {}
    ############################################################################
    # TODO: Your code here!
    for NI in Graph.Nodes():
        voter = NI.GetId()
        ldig = voter % 10
        if (ldig == 0 or ldig == 1 or ldig == 2 or ldig == 3):
            voter_prefs[voter] = 'A'
        elif (ldig == 4 or ldig == 5 or ldig == 6 or ldig == 7):
            voter_prefs[voter] = 'B'
        else:
            voter_prefs[voter] = 'U'
            
       
    ###########################################################################
    assert(len(voter_prefs) == num_voters)
    return voter_prefs


def iterate_voting(Graph, init_conf):
    """
    Function to perform the 10-day decision process. 

    :param - Graph: snap.PUNGraph object representing an undirected graph
    :param - init_conf: Dictionary object containing the initial voting preferences (before any iteration of the decision process)
    
    return type: Python dictionary
    return: Dictionary containing the voting preferences (mapping node ids to 'A','B' or 'U') after the decision process.

    Hint: Use global variables num_voters and decision period to iterate. 
    """
    curr_conf = init_conf.copy()
    curr_alternating_vote = 'A'
    ############################################################################
    # TODO: Your code here!
    for round in range (decision_period):
        #print (round)
        for voter in range(num_voters):
            if (init_conf[voter] == 'U'):
                NI = Graph.GetNI(voter)
                deg = NI.GetDeg()
                a, b = 0, 0
                for i in range(deg):
                    nbrId = NI.GetNbrNId (i)
                    if (curr_conf[nbrId] == 'A'):
                        a += 1
                    elif (curr_conf[nbrId] == 'B'):
                        b += 1
                if (a > b):
                    curr_conf[voter] = 'A'
                elif (b > a):
                    curr_conf[voter] = 'B'
                elif (a == b):
                    curr_conf[voter] = curr_alternating_vote
                    if curr_alternating_vote == 'A':
                        curr_alternating_vote = 'B'
                    else :
                        curr_alternating_vote = 'A'
                    #print ('curr_alternating_vote', curr_alternating_vote)
                    
                #print (curr_conf[voter])
        #print (winner(curr_conf))
    ############################################################################
    return curr_conf


def sim_election(Graph):
    """
    Function to simulate the election process, takes the Graph as input and 
    gives the final voting preferences (dictionary) as output. 
    """
    init_conf = initial_voting_state(Graph)
    conf = iterate_voting(Graph, init_conf)
    return conf


def winner(conf):
    """
    Function to get the winner of election process.
    :param - conf: Dictionary object mapping node ids to the voting preferences
    
    return type: char, int
    return: Return candidate ('A','B') followed by the number of votes by which the candidate wins. 
            If there is a tie, return 'U', 0 
    """
    ############################################################################
    # TODO: Your code here!
    a, b = 0, 0
    cand = 'U'
    votes = 0
    for key, value in conf.iteritems():
        if value == 'A':
            a += 1
        elif value == 'B': 
            b += 1
        
    if a > b:
        cand = 'A'
        votes = a - b
    elif b > a:
        cand = 'B'
        votes = b - a
    
            
    return cand, votes
    ############################################################################


def Q3_1():
    Gs = read_graphs('graph1.txt', 'graph2.txt')    # List of graphs
    final_confs = [sim_election(G) for G in Gs]     # Simulate election process for both graphs to get final voting preference
    res = [winner(conf) for conf in final_confs]    # Get the winner of the election, and the difference in votes for both graphs
    for i in xrange(2):
        print "In graph %d, candidate %s wins by %d votes"%(i+1, res[i][0], res[i][1])


def Q3_2sim(Graph, k):
    """
    Function to simulate the effect of advertising.
    :param - Graph: snap.PUNGraph object representing an undirected graph
             k: amount to be spent on advertising 
    
    return type: int
    return: The number of votes by which A wins (or loses), i.e. (number of votes of A - number of votes of B)

    Hint: Feel free to use initial_voting_state and iterate_voting functions. 
    """
    ############################################################################
    # TODO: Your code here!
    init_conf = initial_voting_state(Graph)
    count = 3000 + (k / 100) 
    for i in range (3000, count):
        init_conf[i] = 'A'
    conf = iterate_voting(Graph, init_conf)
    wnr , votes = winner (conf)
    
    if wnr == 'A':
        return votes
    else:
        return -1 * votes
     
    ############################################################################


def find_min_k(diff):
    """
    Function to return the minimum amount needed for A to win
    :param - diff: list of values by which A wins(or loses) i.e. (A-B), for different values of k. 

    return type: int
    return: The minimum amount needed for A to win
    """
    ############################################################################
    # TODO: Your code here!
    count = 0
    for val in diff:
        if val < 0:
            count += 1 
        if val > 0:
            count += 1
            break
    
    return 1000 * (count)
    ############################################################################


def Q3_plot(Ks, res, title):
    """
    Function to plot the amount spent and the number of votes the candidate wins by
    :param - Ks: The list of amount spent
             res: The list of difference in votes (A-B) for both graphs, for each value of k
             title: The title of the plot
    """
    ############################################################################
    # TODO: Your code here!
    plt.plot(Ks, res[0], 'rx--')
    plt.plot(Ks, res[1], 'go--')
    
    ############################################################################
    plt.plot(Ks, [0.0] * len(Ks), ':', color='black')
    plt.xlabel('Amount spent ($)')
    plt.ylabel('#votes for A - #votes for B')
    plt.title(title)
    plt.legend()
    plt.show()


def Q3_2():
    Gs = read_graphs('graph1.txt', 'graph2.txt')    # List of graphs
    Ks = [x * 1000 for x in range(1, 10)]           # List of amount of $ spent
    res = [[Q3_2sim(G, k) for k in Ks] for G in Gs] # List of (List of diff in votes (A-B)) for both graphs
    min_k = [find_min_k(diff) for diff in res]      # List of minimum amount needed for both graphs
   
    for i in xrange(2):
        print "On graph %d, the minimum amount you can spend to win the election is %s"%(i+1, min_k[i])

    Q3_plot(Ks, res, 'TV Advertising')


def Q3_3sim(Graph, k):
    """
    Function to simulate the effect of a dining event.
    :param - Graph: snap.PUNGraph object representing an undirected graph
             k: amount to be spent on the dining event 
    
    return type: int
    return: The number of votes by which A wins (or loses), i.e. (number of votes of A - number of votes of B)

    Hint: Feel free to use initial_voting_state and iterate_voting functions. 
    """
    ############################################################################
    # TODO: Your code here!
    init_conf = initial_voting_state(Graph)
    deg_list = []
    for i in range (Graph.GetNodes()):
        deg_list.append(Graph.GetNI(i).GetDeg())
        
    for x in range (k/1000):
 
        max_deg = max(deg_list)
        voter = deg_list.index(max_deg)
        init_conf[voter] = 'A'
        deg_list[voter] = 0
    conf = iterate_voting(Graph, init_conf)
    
    wnr , votes = winner (conf)
    
    if wnr == 'A':
        return votes
    else:
        return -1 * votes
        

    ############################################################################


def Q3_3():
    Gs = read_graphs('graph1.txt', 'graph2.txt')    # List of graphs
    Ks = [x * 1000 for x in range(1, 10)]           # List of amount of $ spent
    res = [[Q3_3sim(G, k) for k in Ks] for G in Gs] # List of (List of diff in votes (A-B)) for both graphs
    min_k = [find_min_k(diff) for diff in res]      # List of minimum amount needed for both graphs
    
    for i in xrange(2):
        print "On graph %d, the minimum amount you can spend to win the election is %s"%(i+1, min_k[i])
    
    Q3_plot(Ks, res, 'Wining and Dining')


def Q3_4():
    """
    Function to plot the distributions of two given graphs on a log-log scale.
    """
    ############################################################################
    # TODO: Your code here!
    
    ############################################################################


def main():
    Q3_1()
    Q3_2()
    Q3_3()
    Q3_4()


if __name__ == "__main__":
    main()








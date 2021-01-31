import numpy as np
import matplotlib.pyplot as plt
import random as rnd

#Set random seeds so that any randomness is reproducible

rnd.seed(0)
np.random.seed(0)

key = ["R", "P", "S"]
strats = ["always_rock", "always_scissors", "always_paper", "human", "anti-human"]
#Define general function to play RPS from the perspective of player 1
def RPS(move_p1, move_p2):
    ind1 = key.index(move_p1)
    ind2 = key.index(move_p2)
    if ind1 == ind2:
        return 'D', 'D'
    elif ind1 == (ind2 + 1) or ind1 == (ind2 - 2):
        return 'W', 'L'
    else:
        return 'L', 'W'
#RPS is kinda cyclical, might be an even nicer/shorter implementation using levi cevita


#Class to create a new player
class Player:
    #strategy contains a string which will define the type of strat used
    #n is the number of games per plaeer
    def __init__(self, strategy, n, location=[0, 0]):
        self.strat = strategy   # strategy for player
        self.loc = location   # location# y location
        #self.score = 0   # score of player
        # lists to store players previous results
        #Note we play games starting from R, and proceeding clockwise
        #i.e. R, DR, D, DL, L, UL, U, UR, 
        self.results = np.empty((8,n), dtype='str')
        self.moves = np.empty((8,n), dtype='str')
        
        #note we store the results and moves played in arrays, with 8 rows, and n columns,
        #where the rows denote sets of games against a single player, so row 1 = vs player 2
        #row 2 = vs player 3, etc...
        
        self.prev_move = ','
        self.prev_res = ','
        
        #Define variables to store the last move thrown by a player, for use in memory based strategies
        #this can be gener
    

    
    
    #the function that decides on what move to play, in general will look at the strategy of the player
    #and which opponent it is playing, and its previous moves and results in the current set of play
    def choose_move(self, i, p):
        if self.strat == "always_rock":
            return "R"
        elif self.strat == "always_paper":
            return "P"
        elif self.strat == "always_scissors":
            return "S"
        elif self.strat == "human":
            if p == 0:
                return rnd.choice(key)
            else:
                res = self.prev_res
                if res == 'W':
                    return self.prev_move
                elif res == 'D':
                    return rnd.choice(key)
                else:
                    ind = (key.index(self.prev_move)-1)%3
                    return key[ind]
        elif self.strat == "anti-human":
            if p == 0:
                return rnd.choice(key)
            else:
                res = self.prev_res
                if res == 'W':
                    ind = (key.index(self.prev_move)-1)%3
                    return key[ind]
                elif res == 'D':
                    return rnd.choice(key)
                else:
                    ind = (key.index(self.prev_move)-1)%3
                    return key[ind]
        
        
    #Define a function which acts on the player itself, and takes an opposition player object as an input
    #we also need to know which game this is for player 1, ith game, so that we can calculate which
    #game this will be for player 2
    #(i.e. the game verus the player below me will be my 3rd set of matches, but it will be his 7th set of matches)
    def play(self, player2, i, n):   # play N games
        
        for p in range(0, n):
            p1_move = self.choose_move(i, p)
            p2_move = player2.choose_move(i, p)
            res = RPS(p1_move, p2_move)
            self.results[i, p] = res[0]
            self.moves[i, p] = p1_move
            #note, we only update the results array for the player playing the game
            #the previous move variable is a temporary variable for memory based strats
            self.prev_move = p1_move
            self.prev_res = res[0]
            #note, player 2 also needs to remember its last move for when it chooses its move
            player2.prev_move = p2_move
            player2.prev_res = res[1]
            
            
            

class Simulation:
    #initialise an NxN grid of players, with n games per clock tick
    def __init__(self, N, n):
        self.grid = np.array([]).reshape((0,N))
        self.N = N
        self.n = n
        
        for i in range(N):
            #Append rows one at a time
            row = np.array([])
            for j in range(N):
                row = np.append(row, Player(rnd.choice(strats),n, [i, j]))
            row = row.reshape(1, N)
            self.grid = np.append(self.grid, row, axis=0)
            
            
    
    #Define a function to play a round of n games versus a players nearest 8 neighbours
    def play_round(self, player1):
        pl = player1.loc
        for i in range(0, 8):
            #I've implemented this using a rounded trig, so we circularly rotate around
            p2_loc = pl + [round(np.sin(-45*i)), round(np.cos(-45*i))]
            player2 = self.grid[p2_loc[0]%self.N, p2_loc[1]%self.N]
            player1.play(player2, i, self.n)
            
    def clock_tick(self):
        #Compute a global clock tick
        for i in self.grid:
            for j in i:
                self.play_round(j)
                
        
                
    
            
sim = Simulation(3, 3)
sim.clock_tick()

            
        
    
    
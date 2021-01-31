import numpy as np
import random as rnd
import matplotlib.pyplot as plt

# Set random seeds so that any randomness is reproducible
rnd.seed(0)
np.random.seed(0)

key = ["R", "P", "S"]
strats = ["always_rock", "always_scissors", "always_paper", "human", 
          "anti-human"]

# Define function to play RPS from the perspective of player 1
# Returns 'result for player 1', 'result for player 2'
def RPS(move_p1, move_p2):
    
    ind1 = key.index(move_p1)
    ind2 = key.index(move_p2)
    
    if ind1 == ind2:
        return 'D', 'D'
    
    elif ind1 == (ind2 + 1) or ind1 == (ind2 - 2):
        return 'W', 'L'
    
    else:
        return 'L', 'W'


# Class to create a new player
class Player:
    
    '''
    Initialise a player with a strategy, location, and number of games per
    clock tick
    e.g. player1 = Player("strategy", [x, y], n)
    
    Strategy should be a string which will define the type of strategy used
    picked from the following strategies ["always_rock", "always_scissors",
    "always_paper", "human", "anti-human"]
    
    Location will be a list of two elements consisting of x and y coordinates
    
    n is the number of games played per clock tick
    '''
    
    def __init__(self, strategy, location=[0, 0], n=1):
        self.strat = strategy   # strategy of player
        self.loc = location   # location of player
        
        # lists to store players previous results and moves
        # Note: we play games starting from R, and proceeding clockwise
        #       i.e. R, DR, D, DL, L, UL, U, UR, 
        self.results = np.empty((8,n), dtype='str')
        self.moves = np.empty((8,n), dtype='str')
        
        # Note: we store the results and moves played in arrays, with 8 rows,
        #       and n columns, where the rows denote sets of games against a
        #       single player, so row 0 = vs R, row 1 = vs DR, etc...
        
        # Variables to store last move chosen by player
        self.prev_move = ','
        self.prev_res = ','
    
    
    # Function that decides on what move to play
    # Will look at the strategy of the player and which opponent its playing,
    # and its previous moves and results in the current set of play
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

            
        
    
    
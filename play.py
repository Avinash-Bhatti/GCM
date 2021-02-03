import numpy as np
import random as rnd
from copy import deepcopy

# Set random seeds so that any randomness is reproducible
rnd.seed(0)
np.random.seed(0)


key = ["R", "P", "S"]
strats = ["always_rock", "always_scissors", "always_paper", "human", 
          "anti-human"]


def RPS(move_p1, move_p2):
    
    '''
    A function to play RPS from the persepctive of player 1.
    Returns 'result for player 1', 'result for player 2'
    '''
    
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
    
    def __init__(self, strategy, location, n):
        self.strat = strategy   # strategy of player
        self.loc = location   # location of player
        
        # lists to store players previous results and moves
        # Note: we play games starting from R, and proceeding clockwise
        #       i.e. R, DR, D, DL, L, UL, U, UR, 
        # Note: we store the results and moves played in arrays, with 8 rows,
        #       and n columns, where the rows denote sets of games against a
        #       single player, so row 0 = vs R, row 1 = vs DR, etc...
        self.results = np.empty((8, n), dtype='str')
        self.moves = np.empty((8, n), dtype='str')
        #self.overallResult = np.empty(8, dtype='str')
        self.losses = 0
        
        # Variables to store last move chosen by player
        self.prev_move = ''
        self.prev_res = ''
        # we don't need a variable for this? can just index [-1]???
    
    

    def choose_move(self, p):
        
        '''
        Function that decides on what move to play.
        
        Will look at the strategy of the player and which opponent it is
        playing, as well as its previous moves and results.
        
        Argument 'p' represents how many games have been played in the clock
        tick.
        '''
        
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
                

    def play(self, player2, i, n):   # play N games
        
        '''
        Function which simulates 'games' between self and 'player2'

        Argument 'i' represents what relative player is being played moving in
        a clockwise direction starting with "R". Where 'i' = 0 represents
        the player on the right of self.
        '''
        
        for p in range(n):
            p1_move = self.choose_move(p)
            p2_move = player2.choose_move(p)
            res = RPS(p1_move, p2_move)
            
            # update tuples of results and moves
            self.results[i, p] = res[0]
            self.moves[i, p] = p1_move
            
            # update temporary variables for results and moves 
            self.prev_move = p1_move
            self.prev_res = res[0]
            player2.prev_move = p2_move
            player2.prev_res = res[1]
            
            
    def change_strategy(self, strategy):
        
        '''
        Change the strategy of a Player object taking argument 'strategy'
        '''
        
        self.strat = strategy

          

class Simulation:
    
    '''
    Class to initialise a grid of NxN players, playing n games per clock tick
    '''
    
    def __init__(self, N, n):
        
        self.grid = []
        self.N = N
        self.n = n
        
        # Create N-1 x N-1 grid of Player objects
        for i in range(N):
            row = []
            for j in range(N):
                row.append(Player(rnd.choice(strats), [i, j], n))
            self.grid.append(row)
            
        self.grid = np.array(self.grid)
        

    def clock_tick(self):
        
        '''
        Function to play a round of n games vs nearest 8 neighbours
        '''
        
        for i in range(self.N):
            for j in range(self.N):
                player = self.grid[i][j]   # cycle through all players
                
                player.play(self.grid[(i+1)%self.N][j], 0, self.n)
                player.play(self.grid[(i+1)%self.N][(j-1)%self.N], 1, self.n)
                player.play(self.grid[i][(j-1)%self.N], 2, self.n)
                player.play(self.grid[(i-1)%self.N][(j-1)%self.N], 3, self.n)
                player.play(self.grid[(i-1)%self.N][j], 4, self.n)
                player.play(self.grid[(i-1)%self.N][(j+1)%self.N], 5, self.n)
                player.play(self.grid[i][(j+1)%self.N], 6, self.n)
                player.play(self.grid[(i+1)%self.N][(j+1)%self.N], 7, self.n)
                
                
                '''
                # no boundary conditions (middle players)
                if pl[0] != 0 and pl[0] != self.N-1 \
                                    and pl[1] != 0 and pl[1] != self.N-1:
                    player.play(self.grid[i+1][j], 0, self.n)
                    player.play(self.grid[i+1][j-1], 1, self.n)
                    player.play(self.grid[i][j-1], 2, self.n)
                    player.play(self.grid[i-1][j-1], 3, self.n)
                    player.play(self.grid[i-1][j], 4, self.n)
                    player.play(self.grid[i-1][j+1], 5, self.n)
                    player.play(self.grid[i][j+1], 6, self.n)
                    player.play(self.grid[i+1][j+1], 7, self.n)
                    
                # lower left corner (0, 0)
                elif pl[0] == 0 and pl[1] == 0:
                    player.play(self.grid[1][0], 0, self.n)
                    player.play(self.grid[1][self.N-1], 1, self.n)
                    player.play(self.grid[0][self.N-1], 2, self.n)
                    player.play(self.grid[self.N-1][self.N-1], 3, self.n)
                    player.play(self.grid[self.N-1][0], 4, self.n)
                    player.play(self.grid[self.N-1][1], 5, self.n)
                    player.play(self.grid[0][1], 6, self.n)
                    player.play(self.grid[1][1], 7, self.n)
                    
                # upper left corner (0, N-1)
                elif pl[0] == 0 and pl[1] == self.N-1:
                    player.play(self.grid[1][self.N-1], 0, self.n)
                    player.play(self.grid[1][self.N-2], 1, self.n)
                    player.play(self.grid[0][self.N-2], 2, self.n)
                    player.play(self.grid[self.N-1][self.N-2], 3, self.n)
                    player.play(self.grid[self.N-1][self.N-1], 4, self.n)
                    player.play(self.grid[self.N-1][0], 5, self.n)
                    player.play(self.grid[0][0], 6, self.n)
                    player.play(self.grid[1][0], 7, self.n)
                    
                # upper right corner (N-1, N-1)
                elif pl[0] == self.N-1 and pl[1] == self.N-1:
                    player.play(self.grid[0][self.N-1], 0, self.n)
                    player.play(self.grid[0][self.N-2], 1, self.n)
                    player.play(self.grid[self.N-1][self.N-2], 2, self.n)
                    player.play(self.grid[self.N-2][self.N-2], 3, self.n)
                    player.play(self.grid[self.N-2][self.N-1], 4, self.n)
                    player.play(self.grid[self.N-2][0], 5, self.n)
                    player.play(self.grid[self.N-1][0], 6, self.n)
                    player.play(self.grid[0][0], 7, self.n)
                    
                # lower right corner (N-1, 0)
                elif pl[0] == self.N-1 and pl[1] == 0:
                    player.play(self.grid[0][0], 0, self.n)
                    player.play(self.grid[0][self.N-1], 1, self.n)
                    player.play(self.grid[self.N-1][self.N-1], 2, self.n)
                    player.play(self.grid[self.N-2][self.N-1], 3, self.n)
                    player.play(self.grid[self.N-2][0], 4, self.n)
                    player.play(self.grid[self.N-2][1], 5, self.n)
                    player.play(self.grid[self.N-1][1], 6, self.n)
                    player.play(self.grid[0][1], 7, self.n)
                    
                # bottom edge (i, 0)
                elif pl[1] == 0:
                    player.play(self.grid[i+1][0], 0, self.n)
                    player.play(self.grid[i+1][self.N-1], 1, self.n)
                    player.play(self.grid[i][self.N-1], 2, self.n)
                    player.play(self.grid[i-1][self.N-1], 3, self.n)
                    player.play(self.grid[i-1][0], 4, self.n)
                    player.play(self.grid[i-1][1], 5, self.n)
                    player.play(self.grid[i][1], 6, self.n)
                    player.play(self.grid[i+1][1], 7, self.n)
                    
                # left edge (0, j)
                elif pl[0] == 0:
                    player.play(self.grid[1][j], 0, self.n)
                    player.play(self.grid[1][j-1], 1, self.n)
                    player.play(self.grid[0][j-1], 2, self.n)
                    player.play(self.grid[self.N-1][j-1], 3, self.n)
                    player.play(self.grid[self.N-1][j], 4, self.n)
                    player.play(self.grid[self.N-1][j+1], 5, self.n)
                    player.play(self.grid[0][j+1], 6, self.n)
                    player.play(self.grid[1][j+1], 7, self.n)
                    
                # top edge (i, N-1)
                elif pl[1] == self.N-1:
                    player.play(self.grid[i+1][self.N-1], 0, self.n)
                    player.play(self.grid[i+1][self.N-2], 1, self.n)
                    player.play(self.grid[i][self.N-2], 2, self.n)
                    player.play(self.grid[i-1][self.N-2], 3, self.n)
                    player.play(self.grid[i-1][self.N-1], 4, self.n)
                    player.play(self.grid[i-1][0], 5, self.n)
                    player.play(self.grid[i][0], 6, self.n)
                    player.play(self.grid[i+1][0], 7, self.n)
                    
                # right edge (N-1, j)
                elif pl[0] == self.N-1:
                    player.play(self.grid[0][j], 0, self.n)
                    player.play(self.grid[0][j-1], 1, self.n)
                    player.play(self.grid[self.N-1][j-1], 2, self.n)
                    player.play(self.grid[self.N-2][j-1], 3, self.n)
                    player.play(self.grid[self.N-2][j], 4, self.n)
                    player.play(self.grid[self.N-2][j+1], 5, self.n)
                    player.play(self.grid[self.N-1][j+1], 6, self.n)
                    player.play(self.grid[0][j+1], 7, self.n)
                '''

    def changeAllStrategies(self):
        
        '''
        Change all strategies of players based on number of losses
        '''
        
        for i in range(self.N):
            for j in range(self.N):
                player = self.grid[i][j]    # cycle through all players
                player.losses = 0           # initialise variable to 0
                for k in range(8):
                    res = player.results[k]   # cycle through 8 opponents
                    
                    # count as a loss if lost more than n/2 games
                    if np.count_nonzero(res == 'L') >= (self.n/2):
                        player.losses += 1
                
                # if the player lost to at least 4 opponents, change strategy
                if player.losses >= 4:
                    loc_strats = deepcopy(strats)
                    loc_strats.remove(player.strat)
                    player.change_strategy(rnd.choice(loc_strats))
                    
    
    def play(self, n):
        
        '''
        Simulate RPS over n clock ticks
        '''
        
        for i in range(n):
            self.clock_tick()
            self.changeAllStrategies()
        
#%%     
   
sim = Simulation(3, 10)
sim.grid[0][0].change_strategy('always_paper')
sim.grid[1][0].change_strategy('always_paper')
sim.grid[2][0].change_strategy('always_paper')
sim.grid[0][1].change_strategy('always_paper')
sim.grid[1][1].change_strategy('always_rock')
sim.grid[2][1].change_strategy('always_paper')
sim.grid[0][2].change_strategy('always_paper')
sim.grid[1][2].change_strategy('always_paper')
sim.grid[2][2].change_strategy('always_paper')

#%%

sim.clock_tick()

#%%

sim.changeAllStrategies()



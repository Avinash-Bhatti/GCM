import numpy as np
import random as rnd
import matplotlib.pyplot as plt

# Set random seeds so that any randomness is reproducible
rnd.seed(0)
np.random.seed(0)

key = ["R", "P", "S"]
"""
strats = ["always_rock", "always_scissors", "always_paper", "human", 
          "anti-human"]
strat_key = np.array([0,1,2,3,4])

strat_array = np.array(strats)


strats = ["always_rock", "always_scissors", "always_paper"]

strat_key = np.array([0,1,2])

strat_array = np.array(strats)
"""

strats = ["always_rock", "always_scissors", "always_paper", "human", 
          "anti-human"]

strat_key = np.array([3,4])

strat_array = np.array(strats)

# Define function to play RPS from the perspective of player 1
# Returns 'result for player 1', 'result for player 2'
def RPS(move_p1, move_p2):
    
    ind1 = key.index(move_p1)
    ind2 = key.index(move_p2)
    
    if ind1 == ind2:
        return 'D', 'D', 0
    
    elif ind1 == (ind2 + 1) or ind1 == (ind2 - 2):
        return 'W', 'L', 1
    
    else:
        return 'L', 'W', -1


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
        self.loc = np.array(location)  # location of player
        
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
        
        self.score = 0
    
    
    # Function that decides on what move to play
    # Will look at the strategy of the player and which opponent its playing,
    # and its previous moves and results in the current set of play
    def choose_move(self, p):
        
        if self.strat == strats.index("always_rock"):
            return "R"
        
        elif self.strat == strats.index("always_paper"):
            return "P"
        
        elif self.strat == strats.index("always_scissors"):
            return "S"
        
        elif self.strat == strats.index("human"):
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
                
        elif self.strat == strats.index("anti-human"):
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
        
        temp_score = 0
        for p in range(0, n):
            p1_move = self.choose_move(p)
            p2_move = player2.choose_move(p)
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
            
            temp_score += res[2]
        if temp_score > 0:
            self.score += 1
        elif temp_score == 0:
            pass
        else:
            self.score -= 1
        
            
            

class Simulation:
    #initialise an NxN grid of players, with n games per clock tick
    def __init__(self, N, n, T):
        self.grid = np.array([]).reshape((0,N))
        self.N = N
        self.n = n
        self.T = T
        self.debug = 0
        self.ims = np.empty((T,N,N))
        
        for i in range(N):
            #Append rows one at a time
            row = np.array([])
            for j in range(N):
                row = np.append(row, Player(rnd.choice(strat_key),[i, j], n))
            row = row.reshape(1, N)
            self.grid = np.append(self.grid, row, axis=0)
            
            
    
    #Define a function to play a round of n games versus a players nearest 8 neighbours
    def play_round(self, player1):
        pl = player1.loc
        
    
            
        player2 = self.grid[(pl[0]+1)%self.N, (pl[1])%self.N]
        player1.play(player2, 0, self.n)
        
        player2 = self.grid[(pl[0]+1)%self.N, (pl[1]+1)%self.N]
        player1.play(player2, 1, self.n)
        
        player2 = self.grid[(pl[0])%self.N, (pl[1]+1)%self.N]
        player1.play(player2, 2, self.n)
        
        player2 = self.grid[(pl[0]-1)%self.N, (pl[1]+1)%self.N]
        player1.play(player2, 3, self.n)
        
        player2 = self.grid[(pl[0]-1)%self.N, (pl[1])%self.N]
        player1.play(player2, 4, self.n)
        
        player2 = self.grid[(pl[0]-1)%self.N, (pl[1]-1)%self.N]
        player1.play(player2, 5, self.n)
        
        player2 = self.grid[(pl[0])%self.N, (pl[1]-1)%self.N]
        player1.play(player2, 6, self.n)                                   
        
        player2 = self.grid[(pl[0]+1)%self.N, (pl[1]-1)%self.N]
        player1.play(player2, 7, self.n)
        
            
    def clock_tick(self):
        #Compute a global clock tick
        for i in self.grid:
            for j in i:
                self.play_round(j)
                
    def update_strats(self):
        #Compute a global clock tick
        for i in self.grid:
            for j in i:
                if j.score >= 0:
                    pass
                else:
                    j.strat = rnd.choice(strat_key[strat_key[:] != j.strat])
                
                j.score = 0
                
    def extract_data(self, i):
        self.ims[i] = np.array([[j.strat for j in i] for i in sim.grid])
        
    def run(self):
        #run N clock ticks
        for i in range(self.T):
            self.clock_tick()
            self.extract_data(i)
            self.update_strats()
                
    
            
sim = Simulation(20, 5, 100)
sim.run()



import numpy as np
import matplotlib
matplotlib.use("Agg")


import matplotlib.animation as animation


# Fixing random state for reproducibility
np.random.seed(19680801)


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)




fig2 = plt.figure()

x = np.arange(-0.5, 20.5, 1)
y = np.arange(-0.5, 20.5, 1).reshape(-1, 1)
base = np.hypot(x, y)
ims = []
for i in np.arange(30):
    ims.append((plt.pcolor(x, y, sim.ims[i], vmin=3, vmax=4),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=200, repeat_delay=3000,
                                   blit=True)
im_ani.save('im.mp4', writer=writer)      
        
    
    
import numpy as np
import random as rnd
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import os

# Set random seeds so that any randomness is reproducible
rnd.seed(0)
np.random.seed(0)


key = ["R", "P", "S"]
strats = ["always_rock", "always_paper", "always_scissors", "human", 
          "anti-human", "random_choice"]


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
    
    n is the number of games played per clock tick vs each opponent
    '''
    
    def __init__(self, strategy, location, n):
        self.strat = strategy   # strategy of player
        self.loc = location   # location of player
        
        # lists to store players previous results, moves, and scores vs all 8
        # players
        self.results = np.empty((8, n), dtype='str')
        self.moves = np.empty((8, n), dtype='str')
        self.scores = np.zeros(8)
        
        # list to store general result against each player
        self.res = np.empty(8, dtype='str')   # array to store results
        
        # Variables to store last move chosen by player
        self.prev_move = ''
        self.prev_res = ''    
    

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
                
        elif self.strat == "random_choice":
            return rnd.choice(key)
                

    def play(self, player2, i, n):   # play n games
        
        '''
        Function which simulates games between self and 'player2'

        Argument 'i' represents what relative player is being played moving in
        a clockwise direction starting with "R". Where 'i' = 0 represents
        the player on the right of self.
        '''
        
        score = 0
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
            
            if res[0] == 'W':
                score += 1
            elif res[0] == 'L':
                score -= 1
        
        self.scores[i] = score   # store the score
        if score > 0:
            self.res[i] = 'W'
        elif score < 0:
            self.res[i] = 'L'
        else:
            self.res[i] = 'D'
            
            
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
        self.N = N   # N players in each dimension
        self.n = n   # n games played per clock tick
        
        # Create N x N grid of Player objects
        for i in range(N):
            row = []
            for j in range(N):
                row.append(Player(rnd.choice(strats), [i, j], n))
            self.grid.append(row)
            
        self.grid = np.array(self.grid)
        
        self.clockTicks = 0   # count the number of clock ticks
        
        # list to store strats for imshow
        self.Z = []
        # list to store population of strats for plotting
        self.strats = []
        for i in range(6):
            self.strats.append([])
        
        
    def storeStrats(self):
        
        '''
        Store the strategies for plotting 
        '''
        
        # create NxN list
        l = []
        for i in range(self.N):
            l.append([])
            
        # storing the strat via index for imshow
        for j in range(self.N):
            for i in range(self.N):
                l[j].append(strats.index(self.grid[i][j].strat))   
        self.Z.append(l)
        
        # store the population of strats
        all_strats = []
        for x in range(self.N):
            for y in range(self.N):
                player = self.grid[x][y]
                all_strats.append(player.strat)
        all_strats = np.array(all_strats)
        count = ([np.count_nonzero(all_strats==i) for i in strats])
        for i in range(6):
            self.strats[i].append(count[i])


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
        
        self.clockTicks += 1

    def changeAllStrategies(self):
        
        '''
        Change all strategies of players based on points
        '''
        
        for i in range(self.N):
            for j in range(self.N):
                player = self.grid[i][j]    # cycle through all players
                
                score = 0
                for k in range(8):
                    res = player.res[k]
                    if res == 'W':
                        score += 1
                    elif res == 'L':
                        score -= 1
                        
                # if score < 0, change strategy
                if score < 0:
                    ind=np.where(player.scores==np.amin(player.scores))[0][0]
                    new_strat = ''
                    if ind == 0:
                        new_strat=self.grid[(i+1)%self.N][j].strat
                    elif ind == 1:
                        new_strat=self.grid[(i+1)%self.N][(j-1)%self.N].strat
                    elif ind == 2:
                        new_strat=self.grid[i][(j-1)%self.N].strat
                    elif ind == 3:
                        new_strat=self.grid[(i-1)%self.N][(j-1)%self.N].strat
                    elif ind == 4:
                        new_strat=self.grid[(i-1)%self.N][j].strat
                    elif ind == 5:
                        new_strat=self.grid[(i-1)%self.N][(j+1)%self.N].strat
                    elif ind == 6:
                        new_strat=self.grid[i][(j+1)%self.N].strat
                    elif ind == 7:
                        new_strat=self.grid[(i+1)%self.N][(j+1)%self.N].strat
                    
                    player.change_strategy(new_strat)

        # store strats for plotting
        self.storeStrats()
        

                    
    
    def play(self, t):
        
        '''
        Simulate RPS over t clock ticks
        '''
        
        self.storeStrats()
        
        for i in range(t):
            self.clock_tick()
            self.changeAllStrategies()
        
        # plotting
        fig1 = plt.figure(1)
        fig1.add_axes([0.1, 0.11, 0.6, 0.8])
        im = plt.imshow(self.Z[0], aspect='equal', origin='lower', \
                                                        vmin=0, vmax=5)
        plot_strats = ["Always Rock", "Always Paper", "Always Scissors",
                           "Human", "Anti-human", "Random"]
        vals = np.arange(0, len(plot_strats))
        colours = [im.cmap(im.norm(value)) for value in vals]
        patches = [mpatches.Patch(color=colours[i], label="{}"\
                    .format(plot_strats[i])) for i in range(len(plot_strats))]
        plt.legend(handles=patches, bbox_to_anchor=(1.02,1), loc=2)
        plt.xticks(np.arange(0, self.N))
        plt.yticks(np.arange(0, self.N))
        plt.xlabel('x coordinate')
        plt.ylabel('y coordinate')
        plt.title('{}x{} grid of players playing {} clock ticks'\
                  .format(self.N, self.N, t))
        
        def animate_func(i):
            im.set_array(self.Z[i])
            return [im]

        ani1 = animation.FuncAnimation(fig1,animate_func,frames=len(self.Z),\
                                       interval=500, repeat=False, blit=True)
        ani1.save('{}x{}_{}ticks.mp4'.format(self.N,self.N,t),writer='ffmpeg')
        
        #####
        
        x = np.arange(0, t+1, 1)
        y = self.strats
        
        fig2, ax2 = plt.subplots()
        line1, = ax2.plot(x[:1], y[0][:1], label='Always Rock')
        line2, = ax2.plot(x[:1], y[1][:1], label='Always Paper')
        ax2.set(xlabel='Clock ticks', ylabel='Population', \
                xlim=(-1, t+1), xticks=np.arange(0, t+1, 1), \
                    ylim=(-5, (self.N**2)+5), \
                    title='Population variation with clock ticks')
        ax2.grid()
        ax2.legend(loc='upper right')
        
        def update(i, x, y, line1, line2):
            line1.set_data(x[:i+1], y[0][:i+1])
            line2.set_data(x[:i+1], y[1][:i+1])
            return [line1, line2]

        ani2 = animation.FuncAnimation(fig2, update, frames=len(self.Z), \
               fargs = [x, y, line1, line2], \
                   interval=250, repeat=False, blit=True)
        ani2.save('{}x{}_{}ticksPopulation.mp4'\
                  .format(self.N,self.N,t),writer='ffmpeg')
        
        
        cd = os.getcwd()
        print("MP4 files saved in {}".format(cd))
        
        plt.show()


##############################################################################

sim = Simulation(20, 10)
for x in range(20):
    for y in range(20):
        sim.grid[x][y].change_strategy('always_rock')
sim.grid[2][2].change_strategy('always_paper')
sim.play(20)


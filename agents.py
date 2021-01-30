import numpy as np
import matplotlib.pyplot as plt
import random as rnd

#Set random seeds so that any randomness is reproducible

rnd.seed(0)
np.random.seed(0)

key = ["R", "P", "S"]
#Define general function to play RPS from the perspective of player 1
def RPS(move_p1, move_p2):
    ind1 = key.index(move_p1)
    ind2 = key.index(move_p2)
    if ind1 == ind2:
        return 'D'
    elif ind1 == (ind2 + 1) or ind1 == (ind2 - 2):
        return 'W'
    else:
        return 'L'
#RPS is kinda cyclical, might be an even nicer/shorter implementation using levi cevita


#Class to create a new player
class Player:
    
    def __init__(self, strategy, n, location=[0, 0]):
        self.strat = strategy   # strategy for player
        self.loc = location   # location# y location
        #self.score = 0   # score of player
        # lists to store players previous results
        #Note we play games starting from U, and proceeding clockwise
        #i.e. U, UR, R, DR, D, DL, L, UL
        self.results_curr = np.empty((8,n), dtype='str')
        self.results_prev = np.empty((8,n), dtype='str')
        
        self.moves_curr = np.empty((8,n), dtype='str')
        self.moves_prev = np.empty((8,n), dtype='str')
        
    

    
    
    
    def choose_move(self, results, moves):
        return "R"
            
    
    def play(self, player2, i, n, N):   # play N games
        results_temp = np.array([])
        moves_temp = np.array([])
        for p in range(0, n):
            p1_move = self.choose_move(self.results_prev[i], self.moves_prev[i])
        
        
            p2_move = player2.choose_move(player2.results_prev[(i+4)%N], player2.moves_prev[(i+4)%N])
        
            results_temp = np.append(results_temp, RPS(p1_move, p2_move))
            moves_temp = np.append(moves_temp, p1_move)
        results_temp = results_temp.reshape(1, n)
        moves_temp = moves_temp.reshape(1, n)
        self.results_curr[i] = results_temp
        self.moves_curr[i] = moves_temp
            


class Simulation:
    
    def __init__(self, N, n):
        self.grid = np.array([]).reshape((0,N))
        self.N = N
        self.n = n
        
        for i in range(N):
            #Append rows one at a time
            row = np.array([])
            for j in range(N):
                row = np.append(row, Player('R',n, [i, j]))
            row = row.reshape(1, N)
            self.grid = np.append(self.grid, row, axis=0)
            
            
    def update_vars():
        for i in self.grid:
            for j in i:
                j.results_prev = j.results_curr
                j.moves_prev = j.moves_curr
                
    def play_round(player1):
        pl = player1.loc
        for i in range(0, 8):
            p2_loc = pl + [round(np.sin(-45*i)), round(np.cos(-45*i))]
            player2 = self.grid[p2_loc[0]%self.N, p2_loc[1]%self.N]
            player1.play(player2, i, self.n, self.N)
            
            
    
            
sim = Simulation(5, 8)

            
        
    
    
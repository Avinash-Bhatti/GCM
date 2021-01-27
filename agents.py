import random

class player:
    
    """
    Class to create a new player
    """
    
    def __init__(self, strategy, location=[0, 0]):
        self.strat = strategy   # strategy for player
        self.locX = location[0]   # x location
        self.locY = location[1]   # y location
        self.score = 0   # score of player
        self.rounds = 0   # number of games
        
        # lists to store players previous results
        self.U = []
        self.D = []
        self.L = []
        self.R = []
        self.UL = []
        self.UR = []
        self.LL = []
        self.LR = []

    def xcoord(self):   # return x location
        return self.locX
    
    def ycoord(self):   # return y location
        return self.locY
    
    def win(self):   # when winning a game
        self.score += 3
    
    def lose(self):   # when losing a game
        self.score = self.score
        
    def draw(self):   # when drawing a game
        self.score += 1
        
    def getScore(self):   # return score
        return self.score
    
    def getRounds(self):   # return number of rounds
        return self.rounds
    
    def getGames(self):   # return number of games
        return 8*self.rounds
    
    def avgScore(self):   # return the average score
        return self.getScore() / self.getGames()
    
    def changeStrat(self, strategy):   # change the strategy of the player
        self.strat = strategy
    
    def game(self, choice, opp):   # simulate a game
       
        if choice == "R":
            if opp == "R":
                self.draw()
            elif opp == "P":
                self.lose()
            elif opp == "S":
                self.win()
                
        elif choice == "P":
            if opp == "R":
                self.win()
            elif opp == "P":
                self.draw()
            elif opp == "S":
                self.lose()
            
        elif choice == "S":
            if opp == "R":
                self.lose()
            elif opp == "P":
                self.win()
            elif opp == "S":
                self.draw()
            
    
    def playRound(self):   # play the game with all 8 neighbours
        
        options = ["R", "P", "S"]
        # all 8 opponents given a random choice
        self.U.append(random.choice(options))
        self.D.append(random.choice(options))
        self.L.append(random.choice(options))
        self.R.append(random.choice(options))
        self.UL.append(random.choice(options))
        self.UR.append(random.choice(options))
        self.LL.append(random.choice(options))
        self.LR.append(random.choice(options))
    
        # always rock
        if self.strat == "always rock":
            
            self.game("R", self.U[-1])   # playing vs U
            self.game("R", self.D[-1])   # playing vs D
            self.game("R", self.L[-1])   # playing vs L
            self.game("R", self.R[-1])   # playing vs R
            self.game("R", self.UL[-1])   # playing vs UL
            self.game("R", self.UR[-1])   # playing vs UR
            self.game("R", self.LL[-1])   # playing vs LL
            self.game("R", self.LR[-1])   # playing vs LR
            
        
        # always paper
        elif self.strat == "always paper":
            
            self.game("P", self.U[-1])   # playing vs U
            self.game("P", self.D[-1])   # playing vs D
            self.game("P", self.L[-1])   # playing vs L
            self.game("P", self.R[-1])   # playing vs R
            self.game("P", self.UL[-1])   # playing vs UL
            self.game("P", self.UR[-1])   # playing vs UR
            self.game("P", self.LL[-1])   # playing vs LL
            self.game("P", self.LR[-1])   # playing vs LR
            
             
        # always scissors
        elif self.strat == "always scissors":
            
            self.game("S", self.U[-1])   # playing vs U
            self.game("S", self.D[-1])   # playing vs D
            self.game("S", self.L[-1])   # playing vs L
            self.game("S", self.R[-1])   # playing vs R
            self.game("S", self.UL[-1])   # playing vs UL
            self.game("S", self.UR[-1])   # playing vs UR
            self.game("S", self.LL[-1])   # playing vs LL
            self.game("S", self.LR[-1])   # playing vs LR
            
            
        # random choice out of R, P, or S
        elif self.strat == "random":
            
            self.game(random.choice(options), self.U[-1])   # playing vs U
            self.game(random.choice(options), self.D[-1])   # playing vs D
            self.game(random.choice(options), self.L[-1])   # playing vs L
            self.game(random.choice(options), self.R[-1])   # playing vs R
            self.game(random.choice(options), self.UL[-1])   # playing vs UL
            self.game(random.choice(options), self.UR[-1])   # playing vs UR
            self.game(random.choice(options), self.LL[-1])   # playing vs LL
            self.game(random.choice(options), self.LR[-1])   # playing vs LR
            

        # strategy to beat opponent based on previous game starting with a
        # random choice
        elif self.strat == "TFT":
            
            if self.rounds == 0:   # implement random choice
                self.game(random.choice(options), self.U[-1]) # playing vs U
                self.game(random.choice(options), self.D[-1]) # playing vs D
                self.game(random.choice(options), self.L[-1]) # playing vs L
                self.game(random.choice(options), self.R[-1]) # playing vs R
                self.game(random.choice(options), self.UL[-1]) # playing vs UL
                self.game(random.choice(options), self.UR[-1]) # playing vs UR
                self.game(random.choice(options), self.LL[-1]) # playing vs LL
                self.game(random.choice(options), self.LR[-1]) # playing vs LR
                
            else:   # implement TFT
                if self.U[-2] == "R":   # playing vs U
                    self.game("P", "R")
                elif self.U[-2] == "P":
                    self.game("S", "P")
                elif self.U[-2] == "S":
                    self.game("R", "S")
            
                if self.D[-2] == "R":   # playing vs D
                    self.game("P", "R")
                elif self.D[-2] == "P":
                    self.game("S", "P")
                elif self.D[-2] == "S":
                    self.game("R", "S")
                
                if self.L[-2] == "R":   # playing vs L
                    self.game("P", "R")
                elif self.L[-2] == "P":
                    self.game("S", "P")
                elif self.L[-2] == "S":
                    self.game("R", "S")
            
                if self.R[-2] == "R":   # playing vs R
                    self.game("P", "R")
                elif self.R[-2] == "P":
                    self.game("S", "P")
                elif self.R[-2] == "S":
                    self.game("R", "S")
                    
                if self.UL[-2] == "R":   # playing vs UL
                    self.game("P", "R")
                elif self.UL[-2] == "P":
                    self.game("S", "P")
                elif self.UL[-2] == "S":
                    self.game("R", "S")
            
                if self.UR[-2] == "R":   # playing vs UR
                    self.game("P", "R")
                elif self.UR[-2] == "P":
                    self.game("S", "P")
                elif self.UR[-2] == "S":
                    self.game("R", "S")
                
                if self.LL[-2] == "R":   # playing vs LL
                    self.game("P", "R")
                elif self.LL[-2] == "P":
                    self.game("S", "P")
                elif self.LL[-2] == "S":
                    self.game("R", "S")
            
                if self.LR[-2] == "R":   # playing vs LR
                    self.game("P", "R")
                elif self.LR[-2] == "P":
                    self.game("S", "P")
                elif self.LR[-2] == "S":
                    self.game("R", "S")
                 
                
        self.rounds += 1   # increment counter for number of rounds


    def play(self, numOfRounds=1):   # play multiple rounds
        
        for i in range(numOfRounds):
            self.playRound()
            
        
    
    
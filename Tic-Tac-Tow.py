import random


max_depth = 9




class instance:
    def __init__(self,value=[],depth=0):
        self.board = value
        self.depth = depth
    
    def __eq__(self,other):
        if self.board[0] != other.board[0]:
            return False
        if self.board[1] != other.board[1]:
            return False
        if self.board[2] != other.board[2]:
            return False
        return True
    
    def copy(self):
        temp_list=[]
        temp_list.append(self.board[0].copy())
        temp_list.append(self.board[1].copy())
        temp_list.append(self.board[2].copy())
        temp=instance(temp_list)
        return temp        

    def make_move(self,move,letter):
        self.board[move[0]][move[1]] = letter

    def possible_moves(self):
        moves = []
        for row in range(0,3):
            for cell in range(0,3):
                if self.board[row][cell] is None:
                    moves.append([row,cell])
        return moves

    def active_turn(self):
        if self.depth % 2 == 1:
            return "O"
        else:
            return "X"


    def print_cur(self):
        for f in self.board:
                print(f)
        print('\n')
        
    
    def score(self):
        if self.goal_reached() == "X":
            return 10 - self.depth 
        elif self.goal_reached() == "O":
            return self.depth - 10
        else:
            return 0



    def game_over(self):
        for row in self.board:
            for cell in row:
                if cell == None:
                    return False
            
        return True
        

    def goal_reached(self):
        Winner_X = ["X", "X", "X"]
        Winner_O = ["O", "O", "O"]
        game_count = 0
        temp1=[]
        temp2=[]
        temp3=[]
        temp4=[]
        temp5=[]
        #check the rows for a winner
        for row in self.board:
            if row == Winner_X:
                return "X"
            elif row == Winner_O:
                return "O"
        #check the columns for a winner
        for row in self.board:
            temp1.append(row[0])
            temp2.append(row[1])
            temp3.append(row[2])
        if temp1 == Winner_X or temp2 == Winner_X or temp3 == Winner_X:
            del temp1, temp2, temp3
            return "X"
        elif temp1 == Winner_O or temp2 == Winner_O or temp3 == Winner_O:
            del temp1, temp2, temp3
            return "O"
        #check the diagonals for a winner
        if self.board:
            temp4.append(self.board[0][0])
            temp4.append(self.board[1][1])
            temp4.append(self.board[2][2])
            temp5.append(self.board[0][2])
            temp5.append(self.board[1][1])
            temp5.append(self.board[2][0])
        if temp4 == Winner_X or temp5 == Winner_X:
            del temp4
            del temp5
            return "X"
        elif temp4 == Winner_O or temp5 == Winner_O:
            del temp4
            del temp5
            return "O"
        #check end of game
        return self.game_over()
         

instance()

empty_board = instance([[None, None, None],[None, None, None],[None, None, None]])
board1 = instance([[None, None, None],[None, None, None],[None, None, None]])



def minimax(game, depth, isMaximize):
    if game.goal_reached() != False:
        return game.score()
    depth+=1

    if isMaximize:
        bestX = -100
        for move in game.possible_moves():
            temp=game.copy()
            temp.make_move(move,"X")
            temp.depth=depth
            bestX = max(bestX, minimax(temp, depth,False))
        return bestX
    else:
        bestO = 100
        for move in game.possible_moves():
            temp=game.copy()
            temp.make_move(move,"O")
            temp.depth=depth
            bestO = min(bestO, minimax(temp, depth, True))

        return bestO



def Best_XMove(player,depth):
    best = 100
    bestMove=[None,None]

    for i in range(0,3):
        for j in range(0,3):
            if board1.board[i][j] == None:
                board1.board[i][j] = player
                moveVal = minimax(board1,depth,True)
                board1.board[i][j] = None
                if moveVal < best:
                    bestMove=[i,j]
                    best = moveVal
    return bestMove
                
def Best_OMove(player,depth):
    best = -100
    bestMove=[None,None]

    for i in range(0,3):
        for j in range(0,3):
            if board1.board[i][j] == None:
                board1.board[i][j] = player
                moveVal = minimax(board1,depth,False)
                board1.board[i][j] = None
                if moveVal > best:
                    bestMove=[i,j]
                    best = moveVal

    return bestMove


def make_random_move(game, player):
    random1 = random.randint(1,3)
    random2 = random.randint(1,3)
    while game.board[random1-1][random2-1] == None:
        game.make_move([random1-1,random2-1], player)
        


def start():
    depth = 0
    if board1 == empty_board:
        make_random_move(board1,"X")
        depth+=1
    
    while not board1.goal_reached():  
        board1.print_cur()
        board1.make_move(Best_OMove("O",depth),"O")
        if board1.goal_reached() == "X" or board1.goal_reached() =="O":
           break
        board1.print_cur()
        depth+=1
        board1.make_move(Best_XMove("X",depth),"X")
        if board1.goal_reached() == "X" or board1.goal_reached() =="O":
           break
        depth+=1


    board1.print_cur()
    if board1.score() == 10:
        print("X Wins")
    elif board1.score() == -10:
        print ("O Wins")
    else:
        print("It's a Tie!")


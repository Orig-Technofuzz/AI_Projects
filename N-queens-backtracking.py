import random

board = []
soln1 = []
N=22


class instance:
    def __init__(self, value=[],depth=0,assigned=[]):
        self.board = value
        self.depth = depth
        self.assigned=assigned

    def check_placement(self,coordx,coordy):
        for row in range(0,N):
            for col in range(0,N):
                if row == coordx:
                    if (self.board[row][col] == "Q"):
                        return False
                elif col == coordy:
                    if (self.board[row][col] == "Q"):
                        return False
                elif row + col == coordx + coordy:
                    if (self.board[row][col] == "Q"):
                        return False
                elif row - col == coordx - coordy:
                    if (self.board[row][col] == "Q"):
                        return False
        return True
    def copy(self):
        temp_list=[]
        for lists in self.board:
            temp_list.append(lists.copy())
        temp=instance(temp_list)
        return temp  
    
    def possible_moves(self,move):
        temp=[]
        for i in range(0,N):
            if i != move[1]:
                temp.append([move[0]+1,i])
        return temp
        

    def assign(self, coordx, coordy):
        self.board[coordx][coordy] = "Q"
    
    def game_over(self):
        if self.depth == N:
            return True
        return False

def backtracker(game, depth, move):
    if game.game_over() or depth == N-1:
        game.assigned.append(move)
        return game
    depth+=1
   
    moves = game.possible_moves(move)
    #if moves is None:
        #return None
    for mover in moves:
        if game.check_placement(mover[0],mover[1]):
            temp=game.copy()
            temp.assign(mover[0],mover[1])
            temp.depth=depth
            temp.assigned.append(move)
            result = backtracker(temp, depth, mover)
            if result is not None:
                return result
            temp.assigned.pop()
    #return None


def build_board():
    for i in range(0,N):
        board.append([])
    for i in range(0,N):
        for j in range(0,N):
            board[i].append(None)
    temp=0
    temp = random.randint(0,N-1)
    board[0][temp]="Q"
    return temp


def main():
    soln_count = 0
    while(soln_count < 4):
        init = build_board()
        state = instance(board)
        soln=backtracker(state, 0, [0,init])
        print(soln.assigned)
        soln.assigned.clear()
        board.clear()
        soln_count+=1
main()

    

import copy
import gc
import time
import heapq

#------------------------------------------------------------------------------------------
move_list= {
    (0,0): [[0,1], [1,0]],
    (0,1): [[0,0],[0,2],[1,1]],
    (0,2): [[0,1],[1,2]],
    (1,0): [[0,0],[2,0],[1,1]],
    (1,1): [[1,0],[0,1],[1,2],[2,1]],
    (1,2): [[0,2],[2,2],[1,1]],
    (2,0): [[1,0],[2,1]],
    (2,1): [[2,0],[2,2],[1,1]],
    (2,2): [[1,2],[2,1]],
        }
soln_loc={
    0: [0,0],
    1: [0,1],
    2: [0,2],
    3: [1,0],
    4: [1,1],
    5: [1,2],
    6: [2,0],
    7: [2,1],
    8: [2,2],
}


IDS_moves=[]
BFS_moves=[]
IDS_times=[]
BFS_times=[]
ASM_moves=[]
ASM_times=[]
ASrch_moves=[]
ASrch_times=[]

max_depth = 50
expandedarr = [set() for _ in range(max_depth)]
frontierarr = [list() for _ in range(max_depth)]
hasharr = [set() for _ in range(max_depth)]
frontier=[]
frontier_hash=set()
expanded=set()
visited=set()
result = []

#------------------------------------------------------------------------------------------
class instance:
    def __init__(self,value=[]):
        self.puzzle = value

    def __eq__(self,other):
        match = 0
        for j in range(0,3):
            if (self.puzzle[j] == other.puzzle[j]):
                match+=1
            else:
                break
        if (match == 3):
            return True
        else:
            return False 

        
    def zero_location(self):
        for i in range(0,3):
            for j in range(0,3):
                if (self.puzzle[i][j]==0):
                    return [i,j]
        

    def make_move(self,blank,new_loc):
        temp = self.puzzle[new_loc[0]][new_loc[1]]
        self.puzzle[new_loc[0]][new_loc[1]] = self.puzzle[blank[0]][blank[1]]
        self.puzzle[blank[0]][blank[1]]=temp

    def possible_moves(self):
        zl = self.zero_location()
        ml = move_list[(zl[0],zl[1])]
        ml.append(zl)
        return ml

    def print_cur(self):
        print(self.puzzle)
    
    def goal_reached(self):
        if soln == self:
            return True
        return False
         

instance()


#------------------------------------------------------------------------------------------
class state():
    def __init__(self,value=instance(None)):
        self.left = None
        self.right = None
        self.down = None
        self.up = None
        self.parent = None
        self.cost = 0
        self.cur = value
        
    def key(self):
        temp = self.cur.puzzle[0].copy()
        temp.extend(self.cur.puzzle[1].copy())
        temp.extend(self.cur.puzzle[2].copy())
        s=0
        for i in temp:
            s += temp[i] * (10 ** i)
        return s
    

    def __eq__(self,other):
        
        return other is not None and self.cur == other.cur

    def __cmp__(self,other):
        return cmp(self.cost,other.cost)
    
    def __lt__(self,other):
        return self.cost < other.cost

    def build_BFS_branch(self,mode):
        pm = self.cur.possible_moves()
        zl = pm.pop()
        # for each possible move, create new node and insert into
        # the graph, then add the item into the frontier
        for i in pm:

            temp_puz=[]
            temp_puz.append(self.cur.puzzle[0].copy())
            temp_puz.append(self.cur.puzzle[1].copy())
            temp_puz.append(self.cur.puzzle[2].copy())
            temp_state = state(instance(temp_puz))
            #temp_state = state(instance(copy.deepcopy(self.cur.puzzle)))
            temp_state.cur.make_move(zl,i)
            if(temp_state.check_parent()):
                continue
            if(temp_state.check_frontier()):
                continue
            if(expanded):
                if (temp_state.key() in expanded):
                    continue 
            temp_state.left = None
            temp_state.right = None
            temp_state.down = None
            temp_state.up = None
            temp_state.parent=self
            if mode == 1:
                temp_state.cost=temp_state.manhattan_func()+temp_state.depth()
            elif mode == 2:
                temp_state.cost=temp_state.misplaced_func()+temp_state.depth()            
            
            #put new state into an empty location
            #append item to frontier
            frontier_hash.add(temp_state.key())
            if mode == 0:
                frontier.append(temp_state)
            else:
                heapq.heappush(frontier,temp_state)

            if (self.left == None):
                self.left = temp_state
            elif (self.right == None):
                self.right = temp_state
            elif (self.down == None):
                self.down = temp_state
            elif (self.up == None):
                self.up = temp_state
    
    #get list of children
    def children(self):
        children=[]
        if (self.left != None):
            children.append(self.left)
        if (self.right != None):
            children.append(self.right)
        if (self.down != None):
            children.append(self.down)
        if (self.up != None):
            children.append(self.up)
        return children
    
    #build children of state
    def build_DFS_branch(self,maxd):
        #get move list and zero location
        pm = self.cur.possible_moves()
        zl = pm.pop()
        # for each possible move, create new node and insert into
        # the graph, then add the item into the frontier
        
        for i in pm:
           temp_puz=[]
           temp_puz.append(self.cur.puzzle[0].copy())
           temp_puz.append(self.cur.puzzle[1].copy())
           temp_puz.append(self.cur.puzzle[2].copy())
           temp_state = state(instance(temp_puz))
           #temp_state = state(instance(copy.deepcopy(self.cur.puzzle)))
           temp_state.cur.make_move(zl,i)
           #if(hasharr[maxd]):
           #if (temp_state.key() in hasharr[maxd]):
           #continue
           if(temp_state.check_parent()):
               continue
           if(expanded):
                if (temp_state.key() in expanded):
                    continue 
           temp_state.left = None
           temp_state.right = None
           temp_state.down = None
           temp_state.up = None
           temp_state.parent=self
           
           
           
           #put new state into an empty location
           #append item to frontier
           hasharr[maxd].add(temp_state.key())
           visited.add(temp_state.key())
           frontierarr[maxd].append(temp_state)
           if (self.left == None):
               self.left = temp_state
           elif (self.right == None):
               self.right = temp_state
           elif (self.down == None):
               self.down = temp_state
           elif (self.up == None):
               self.up = temp_state
     
    def manhattan_func(self):
        distance = 0
        for x in range(0,3):
            for y in range(0,3):
                s = soln_loc[self.cur.puzzle[x][y]]
                distance += abs(x - s[0])
                distance += abs(y - s[1])
        return distance
             
    def misplaced_func(self):
        match = 0
        for j in range(0,3):
            for i in range(0,3):
                if (self.cur.puzzle[j][i] == soln.puzzle[j][i]):
                    match+=1
        return 2 * (8-match)

    def depth(self):
        d = 0
        cur=self
        while cur.parent:
            cur = cur.parent
            d+=1
        return d
    
    def check_frontier(self):
        if(frontier_hash):
            if (self.key() in frontier_hash):
                return True 
            else:
                return False
    
    def check_visited(self):
        if(visited):
            if (self.key() in visited):
                return True 
            else:
                return False

    def check_parent(self):
        if self.parent == None:
            return False
        
        if(self.key() == self.parent.key()):
            return True
        else:
            return False

    
state()
#------------------------------------------------------------------------------------------
soln = instance([[0,1,2],[3,4,5],[6,7,8]])

#print all states from root to goal
def print_result(answer):
    BFSavgT = None
    BFSavgS = None
    IDSavgT = None
    IDSavgS = None
    ASMavgT = None
    ASMavgS = None
    ASrchavgT = None
    ASrchavgS = None
    while True:
        print_node(answer.pop())
        if not answer:
            break 
        print("to") 
    if len(BFS_moves) != 0 and len(BFS_times) != 0:
        BFSavgT = sum(BFS_times)/len(BFS_times)
        BFSavgS = sum(BFS_moves)/len(BFS_moves)
    if len(IDS_moves) != 0 and len(IDS_times) != 0:
        IDSavgT = sum(IDS_times)/len(IDS_times)
        IDSavgS = sum(IDS_moves)/len(IDS_moves)
    if len(ASM_moves) != 0 and len(ASM_times) != 0:
        ASMavgT = sum(ASM_times)/len(ASM_times)
        ASMavgS = sum(ASM_moves)/len(ASM_moves)
    if len(ASrch_moves) != 0 and len(ASrch_times) != 0:
        ASrchavgT = sum(ASrch_times)/len(ASrch_times)
        ASrchavgS = sum(ASrch_moves)/len(ASrch_moves)

    print ("\t\tAverage Steps\tAverage_Time\n")
    #print ("IDS \t\t{}\t\t{}".format(IDSavgS,IDSavgT))
    #print ("BFS \t\t{}\t\t{}".format(BFSavgS,BFSavgT))
    print ("ASM \t\t{}\t\t{}".format(ASMavgS,ASMavgT))
    print ("ASrch \t\t{}\t\t{}".format(ASrchavgS,ASrchavgT))             
    
#print each state
def print_node(node):
    if isinstance(node, str):
        print(node)
        return
    for i in range(3):
        print (node.cur.puzzle[i])

def BFS_soln():

    #build the state graph
    while frontier:
        
        exists = False
        #pop from the frontier
        cur_state = frontier.pop(0)
        #check expanded to see if state exists
        if(expanded):
            if (cur_state.key() in expanded):
                exists = True 
            else:
                exists = False
        if cur_state.key() == 876543210:
            break
        #if the state does not exist add to expanded
            #and build the branch of the state
        if (not exists):
            expanded.add(cur_state.key())
            cur_state.build_BFS_branch(0)
    #return the goal state
    return cur_state


def IDS_soln(new_initial):

    solution = False

    for i in range(max_depth):       
        #append the root to the frontier to rebuild
        #the state graph, if solution was found on
        #the last search
        frontierarr[i].append(new_initial)
        if solution == True:
            break
        #start building the state graph
        while frontierarr[i]:
        
            exists = False
            #pop from the frontier
            cur_state = frontierarr[i].pop()
            if cur_state.key() == 876543210:
                solution=True
                break
            #get the current depth
            if cur_state.depth() == i:
                continue
            #check expanded to see if state exists
            if(expandedarr[i]):
                if (cur_state.key() in expandedarr[i]):
                    exists = True 
                else:
                    exists = False
            
            #if the state does not exist add to expanded
            #and build the branch of the state
            if not exists :
                expandedarr[i].add(cur_state.key())
                cur_state.build_DFS_branch(i)
        #if no solution, increase max depth
        
    #return the goal state
    return cur_state

def A_star_manhattan():
    #build the state graph
    while frontier:
        
        exists = False
        #reheapify frontier and
        #pop from the priority queue
        #heapq.heapify(frontier)
        cur_state = heapq.heappop(frontier)
        #check expanded to see if state exists
        if(expanded):
            if (cur_state.key() in expanded):
                exists = True 
            else:
                exists = False
        if cur_state.key() == 876543210:
            break
        #if the state does not exist add to expanded
            #and build the branch of the state
        if (not exists):
            expanded.add(cur_state.key())
            cur_state.build_BFS_branch(1)
    #return the goal state
    return cur_state

def A_star_misplaced():
    #build the state graph
    while frontier:
        
        exists = False
        #reheapify frontier and
        #pop from the priority queue
        #heapq.heapify(frontier)
        cur_state = heapq.heappop(frontier)
        #check expanded to see if state exists
        if(expanded):
            if (cur_state.key() in expanded):
                exists = True 
            else:
                exists = False
        if cur_state.key() == 876543210:
            break
        #if the state does not exist add to expanded
            #and build the branch of the state
        if (not exists):
            expanded.add(cur_state.key())
            cur_state.build_BFS_branch(2)
    #return the goal state
    return cur_state

#add item paths to variable result
def ADD_results(cur_state, soln):
    cur = cur_state
    moves = 0
    result.append(soln)
    while cur.parent:
       result.append(cur)
       cur = cur.parent
       moves+=1


def main():
   puzzle=[] 
   puzzleCases=[] 
   #open the file, and convert the lists of strings
   #into a list of integers and form them into
   #an overall matrix
   with open("Input8PuzzleCases.txt","r") as file:
        for line in file:
            puzzle.clear()
            temp = line.strip('\n')
            temp = temp.replace(" ","")
            numbers = temp.split(',')
            numbers = [ int(x) for x in numbers ]
            puzzle.append(numbers[:3].copy())
            puzzle.append(numbers[3:6].copy())
            puzzle.append(numbers[6:9].copy())
            puzzleCases.append(puzzle.copy())

   puzzle_num = 0 
   while puzzleCases:
        puzzle_num+=1
        if puzzle_num > 20:
            break
        new_puzzle = instance(puzzleCases.pop())
        new_initial = state(new_puzzle)
        frontier.append(new_initial)
        expanded.clear()
        frontier_hash.clear()
#------------------------------------------------------------------------------------------
        #print("Solving Puzzle {} via BFS".format(puzzle_num))
        #time1=time.time()
        #run BFS
        #cur_state = BFS_soln()
        #time2=time.time()
        #BFS_times.append(time2-time1)
        #BFS_moves.append(cur_state.depth())
#------------------------------------------------------------------------------------------
        #if puzzle_num < 2:
           # ADD_results(cur_state, "BFS")
        expanded.clear()
        frontier_hash.clear()
        new_initial=state(new_puzzle)
#------------------------------------------------------------------------------------------
        #print("Solving Puzzle {} via IDS".format(puzzle_num))
        #time3=time.time()
        #run IDS
        #cur_state = IDS_soln(new_initial)
        #time4=time.time()
        #IDS_times.append(time4-time3)
        #IDS_moves.append(cur_state.depth())
#------------------------------------------------------------------------------------------
        print("Solving Puzzle {} via A* Search [Manhattan]".format(puzzle_num))
        time5=time.time()
        #run A* Search with manhattan heuristic function
        cur_state = A_star_manhattan()
        time6=time.time()
        ASM_times.append(time6-time5)
        ASM_moves.append(cur_state.depth())
        
        if puzzle_num < 2:
            ADD_results(cur_state, "ASM")


        expanded.clear()
        frontier_hash.clear()
        new_initial=state(new_puzzle)

        print("Solving Puzzle {} via A* Search [Misplaced]".format(puzzle_num))
        time7=time.time()
        #run A* Search with misplaced heuristic function
        cur_state = A_star_misplaced()
        time8=time.time()
        ASrch_times.append(time8-time7)
        ASrch_moves.append(cur_state.depth())
        
main()

print_result(result)


# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
#--encoding:utf-8--#
import time
import os
import string
from copy import deepcopy



class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = "H"
    AI = "AI"

    def __init__(self, recommend = True):
        self.n = self.define_attrib(list(range(3,11)), "Size of the board [3,10]: ")
        self.b = self.define_attrib(list(range((2*self.n)+1)), "Number of blocks on the board [0,2n]: ")
        self.pos_block = self.get_block_pos()
        self.s = self.define_attrib(list(range(3,self.n+1)), "Winning line-up size [3,n]: ")
        self.t = self.define_attrib(list(range(100)), "Maximum executation time: ")
        print("Information for Player 1:")
        self.p1 = self.define_attrib(["H","AI"], "Play mode(H/AI): ")
        self.a1 = self.define_attrib([0,1], "Use Minimax (0) or Alphabeta (1): ")
        self.d1 = self.define_attrib(list(range(1,11)), "Maximal Depth for Heuristic [1,10]: ")
        self.e_1 = self.define_attrib([1,2], "Evaluation function (1/2): ")
        print("\nInformation for Player 2:")
        self.p2 = self.define_attrib(["H","AI"], "Play mode(H/AI): ")
        self.a2 = self.define_attrib([0,1], "Use Minimax (0) or Alphabeta (1): ")
        self.d2 = self.define_attrib(list(range(1,11)), "Maximal Depth for Heuristic [1,10]: ")
        self.e_2 = self.define_attrib([1,2], "Evaluation function (1/2): ")
        self.initialize_game()
        self.recommend = recommend
        
        # self.n = 8
        # self.b = 6
        # self.pos_block = [('A',0), ('B',3),('F', 7),('D',5),('E',7),('G',2)]
        # self.s = 5
        # self.d1 = 6
        # self.d2 = 6
        # self.t = 5
        # self.p1, self.p2 = ["AI","AI"]
        # self.e_1 = 1
        # self.e_2 = 2
        # self.a1 = 1
        # self.a2 = 1
        # self.initialize_game()
        # self.recommend = recommend
        
        
        self.winner = 0
        self.dict_depth_e1 = {i:0 for i in range(0,self.d1+1)}
        self.dict_depth_e2 = {i:0 for i in range(0,self.d2+1)}
        self.dict_depth_game = {i:0 for i in range(0,max(self.d1, self.d2)+1)}
        self.dict_depth_game_e1 = {i:0 for i in range(0,self.d1+1)}
        self.dict_depth_game_e2 = {i:0 for i in range(0,self.d2+1)}
        self.dict_ard = {i:0 for i in range(0,max(self.d1, self.d2)+1)}
        self.ard_e1 = 0
        self.ard_e2 = 0
        self.nb_state = 0
        self.nb_e1 = 0
        self.nb_e2 = 0
        self.illegal_pos = self.pos_block
        self.exec_time = 0
        self.t_e1 = 0
        self.t_e2 = 0
        self.txt = ''
    
    
    def initialize_game(self):
        self.current_state = list()
        alph = list(string.ascii_uppercase[0:self.n])
        for i in range(self.n):
            self.current_state.append(["." for j in range(self.n)])
        # Player X always plays first
        if self.b != 0:
            for block in self.pos_block:
                self.current_state[alph.index(block[0])][block[1]] = 'X'
        #self.draw_board()
        self.player_turn = 'w'
    
    def define_attrib(self, list_value, sent):
        while(True):
            attribute = input(sent)
            if(not attribute.isdigit() and attribute in list_value): #return str if it's a letter
                return attribute
            elif(attribute.isdigit() and int(attribute) in list_value): #return int if it's a number
                return int(attribute)
            else:
                print("Please, enter a valid value.")
    
    def get_block_pos(self):
        L_block = []
        alph = list(string.ascii_uppercase[0:self.n])
        for i in range(self.b):
            run=1
            while(run):
                x = self.define_attrib(alph, f"x value of block {i+1} (letter): ")
                y = self.define_attrib(list(range(self.n)), f"y value of block {i+1} (int): ")
                if ([x,y] in L_block):
                    print("Existing block, choose different coordinates !")
                    print("\n")
                else:
                    run=0
                    L_block.append([x,y])
            print("\n")
        return L_block
    
    def draw_board(self, board=None):
        print()
        alph = string.ascii_uppercase[0:self.n]
        
        print(f"  {alph}")
        self.txt += f"\n\n  {alph}"
        print(f" +{'-'*self.n}")
        self.txt += f"\n +{'-'*self.n}\n"
        for row,y in enumerate(range(0, self.n)):
            print(f"{row}|", end="")
            self.txt += f"{row}|"
            for x in range(0, self.n):
                if board==None:
                    val = self.current_state[x][y]
                    if(val=='w'):
                        val = u"\u25CB"
                    elif(val=='b'):
                        val = u"\u25CF"
                    print(F"{val}", end="")
                    self.txt += F"{val}"
                else:
                    val = board[x][y]
                    if(val=='w'):
                        val = u"\u25CB"
                    elif(val=='b'):
                        val = u"\u25CF"
                    print(F"{val}", end="")
                    self.txt += F"{val}"
            print()
            self.txt += '\n'
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.n or py < 0 or py > self.n:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        seq_w = 'w'*self.s
        seq_b = 'b'*self.s
        
        # Vertical win
        for i in range(self.n):
            column_i = ''
            for index in range(self.n):
                column_i += self.current_state[i][index]
            if(seq_w in column_i):
                return 'w'
            elif(seq_b in column_i):
                return 'b'
            
       # Horizontal win
        for i in range(self.n):
            row_i = ''
            for index in range(self.n):
                row_i += self.current_state[index][i]
            if(seq_w in row_i):
                return 'w'
            elif(seq_b in row_i):
                return 'b'
            
        # Right descending diagonal win
        for i in range(self.n-self.s+1):
            for j in range(self.n-self.s+1):
                diag_i = ''
                for k in range(self.s):
                    diag_i += self.current_state[j+k][i+k]
                if(seq_w in diag_i):
                    return 'w'
                elif(seq_b in diag_i):
                    return 'b'
            
        # Second diagonal win
        for i in range(self.n-1,self.s-2,-1):
            for j in range(self.n - self.s+1):
                diag_i = ''
                for k in range(self.s):
                    diag_i += self.current_state[i-k][j+k]
                if(seq_w in diag_i):
                    return 'w'
                elif(seq_b in diag_i):
                    return 'b'
        # Is whole board full?
        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def e1(self, board):
        V = 0
        for i in range(self.n):
            row_i = ''
            for j in range(self.n):
                row_i += board[j][i]
            for k in range(self.s, 0, -1):
                if(row_i.count('w')==k):
                    V += 10**k
                    break
                if(row_i.count('b')==k):
                    V -= 10**k
                    break
                    
        for i in range(self.n):
            column_i = ''
            for j in range(self.n):
                column_i += board[i][j]
            for k in range(self.s, 0, -1):
                if(column_i.count('w')==k):
                    V += 10**k
                    break
                if(column_i.count('b')==k):
                    V -= 10**k
                    break
                    
        for i in range(self.n-self.s+1):
            for j in range(self.n-self.s+1):
                diag_i = ''
                for k in range(self.s):
                    diag_i += board[j+k][i+k]
                for l in range(self.s, 0, -1):
                    if(diag_i.count('w')==l):
                        V += 10**l
                        break
                    if(diag_i.count('b')==l):
                        V -= 10**l
                        break
                        
        for i in range(self.n-1,self.s-2,-1):
            for j in range(self.n - self.s+1):
                diag_i = ''
                for k in range(self.s):
                    diag_i += board[i-k][j+k]
                for l in range(self.s, 0, -1):
                    if(diag_i.count('w')==l):
                        V += 10**l
                        break
                    if(diag_i.count('b')==l):
                        V -= 10**l
                        break
        return V
    
    def e2(self, board):
        V = 0
        #rows
        for i in range(self.n):
            wCount = 0
            bCount = 0
            for j in range(self.n):
                if board[i][j] == 'w':
                    wCount+=1
                elif board[i][j] == 'b':
                    bCount += 1
            if wCount > 0 and bCount == 0  :      
                V += wCount**4
            elif bCount > 0 and wCount == 0 :
                V -= bCount**4

        for i in range(self.n):
            wCount = 0
            bCount = 0
            for j in range(self.n):
                if board[j][i] == 'w':
                    wCount+=1
                elif board[j][i] == 'b':
                    bCount += 1
            if wCount > 0 and bCount == 0  :      
                V += wCount**4
            elif bCount > 0 and wCount == 0 :
                V -= bCount**4


        for i in range(self.n-self.s+1):
            for j in range(self.n-self.s+1):
                wCount = 0
                bCount = 0
                diag_i = ''
                for k in range(self.s):
                    if board[j+k][i+k] == 'w':
                        wCount+=1
                    elif board[j+k][i+k] == 'b':
                        bCount += 1
                if wCount > 0 and bCount == 0  :      
                    V += wCount**4
                elif bCount > 0 and wCount == 0 :
                    V -= bCount**4
                    
        for i in range(self.n-1,self.s-2,-1):
            for j in range(self.n - self.s+1):
                wCount = 0
                bCount = 0
                diag_i = ''
                for k in range(self.s):
                    diag_i += board[i-k][j+k]
                    if board[i-k][j+k] == 'w':
                        wCount+=1
                    elif board[i-k][j+k] == 'b':
                        bCount += 1
                if wCount > 0 and bCount == 0  :      
                    V += wCount**4
                elif bCount > 0 and wCount == 0 :
                    V -= bCount**4
        return V
    
    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'w':
                print('The winner is Player 1 (white)!')
                self.txt +='\nThe winner is Player 1 (white)!'
                if self.player_turn == 'w':
                    self.winner = 'w'
                else :
                    self.winner = 'b'
            elif self.result == 'b':
                print('The winner is Player 2 (black)!')
                self.txt +='\nThe winner is Player 2 (black)!'
                if self.player_turn == 'w':
                    self.winner = 'w'
                else :
                    self.winner = 'b'
            
            elif self.result == '.':
                print("It's a tie!")
                self.txt += "\nIt's a tie!"
                if self.player_turn == 'w':
                    self.winner = 0
                else :
                    self.winner = 0
            print("\nFor heuristic 1: ")
            self.txt +="\n\nFor heuristic 1: "
            print(f"    i   Average evaluation time: {self.t_e1/self.nb_e1}s")
            self.txt +=f"\n    i   Average evaluation time: {self.t_e1/self.nb_e1}s"
            print(f"    ii  Number of state evaluate by the heuristic: {sum(self.dict_depth_game_e1.values())}")
            self.txt +=f"\n    ii  Number of state evaluate by the heuristic: {sum(self.dict_depth_game_e1.values())}"
            print(f"    iii Average of the per-move average depth: { {k: v / self.nb_e1 for k, v in self.dict_depth_game_e1.items()} }")
            self.txt +=f"\n    iii Average of the per-move average depth: { {k: v / self.nb_e1 for k, v in self.dict_depth_game_e1.items()} }"
            print(f"    iv  Total number of states evaluated: {self.dict_depth_game_e1}")
            self.txt +=f"\n    iv  Total number of states evaluated: {self.dict_depth_game_e1}"
            print(f"    v   Average ARD: {self.ard_e1/self.nb_e1}")
            self.txt +=f"\n    v   Average ARD: {self.ard_e1/self.nb_e1}"
            print(f"    vi  Total number of moves in the game: {self.nb_e1}")
            self.txt +=f"\n    vi  Total number of moves in the game: {self.nb_e1}"
            print("\nFor heuristic 2: ")
            self.txt +="\n\nFor heuristic 2: "
            print(f"    i   Average evaluation time: {self.t_e2/self.nb_e2}s")
            self.txt +=f"\n    i   Average evaluation time: {self.t_e2/self.nb_e2}s"
            print(f"    ii  Number of state evaluate by the heuristic: {sum(self.dict_depth_game_e2.values())}")
            self.txt +=f"\n    ii  Number of state evaluate by the heuristic: {sum(self.dict_depth_game_e2.values())}"
            print(f"    iii Average of the per-move average depth: { {k: v / self.nb_e2 for k, v in self.dict_depth_game_e2.items()} }")
            self.txt +=f"\n    iii Average of the per-move average depth: { {k: v / self.nb_e2 for k, v in self.dict_depth_game_e2.items()} }"
            print(f"    iv  Total number of states evaluated: {self.dict_depth_game_e2}")
            self.txt +=f"\n    iv  Total number of states evaluated: {self.dict_depth_game_e2}"
            print(f"    v   Average ARD: {self.ard_e2/self.nb_e2}")
            self.txt +=f"\n    v   Average ARD: {self.ard_e2/self.nb_e2}"
            print(f"    vi  Total number of moves in the game: {self.nb_e2}")
            self.txt +=f"\n    vi  Total number of moves in the game: {self.nb_e2}"
            #self.initialize_game()
        return self.result
    
    def input_move(self, player, AI=False, coord=()):
        alph = string.ascii_uppercase[0:self.n]
        if not AI:
            while True:
                print(F'Player {self.player_turn}, enter your move:')
                px = self.define_attrib(alph, 'Enter the x coordinate (letter): ')
                py = int(self.define_attrib(list(range(self.n)), 'Enter the y coordinate (int): '))
                if self.is_valid(alph.index(px), py):
                    self.illegal_pos.append((alph.index(px),py))
                    self.current_state[alph.index(px)][py] = player
                    return (alph.index(px), py)
                else:
                    print('The move is not valid! Try again.\n')
        else:
            self.current_state[coord[0]][coord[1]] = player
            letter = alph[coord[0]]
            self.illegal_pos.append((letter,coord[1]))
            return (alph[coord[0]], coord[1])

    def switch_player(self):
        if self.player_turn == 'w':
            self.player_turn = 'b'
        elif self.player_turn == 'b':
            self.player_turn = 'w'
        return self.player_turn
    
    def get_legal_pos(self):
        alph = list(string.ascii_uppercase[0:self.n])
        legal_pos = list()
        for i in range(self.n):
            for j in range(self.n):
                if((alph[i],j) not in self.illegal_pos):
                    legal_pos.append((alph[i],j))
        return(legal_pos)
    
    def get_ard(self):
        mean = 0
        for ite, val in sorted(self.dict_ard.items(), reverse=True):
            if val != 0:
                mean += ite*val
                mean /= val
        return mean
            
    def save(self):
        self.txt = self.txt.replace("\n", "\n")
        f = open(f"gameTrace-{self.n}{self.b}{self.s}{self.t}.txt", "w", encoding ="utf-8")
        f.write(self.txt)
        f.close()
    
    def minimax(self, parent_board, depth, x=None, y=None, maxi=False):
        # Maximizing for 'w' and minimizing for 'b'
        start = time.time()
        
        result = self.is_end()
        if result == 'w':
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            if self.player_turn == 'w': 
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                end = time.time()
                self.exec_time += end-start
            return (1000000, x, y)
        elif result == 'b':
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            if self.player_turn == 'w': 
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                end = time.time()
                self.exec_time += end-start
            end = time.time()
            self.exec_time += end-start
            return (-1000000, x, y)
        elif result == '.':
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            if self.player_turn == 'w': 
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                end = time.time()
                self.exec_time += end-start
            end = time.time()
            self.exec_time += end-start
            return (0, x, y)
        elif depth == 0:
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            
            if self.player_turn=="w":
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
                if self.e_1 == 1:
                    value = self.e1(parent_board)
                else:
                    value = self.e2(parent_board)
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                if self.e_2 == 1:
                    value = self.e1(parent_board)
                else:
                    value = self.e2(parent_board)
            end = time.time()
            self.exec_time += end-start
            return (value, x, y)
        
        L_move = list()
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if maxi:
                        self.current_state[i][j] = 'w'
                        (v, x, y) = self.minimax(self.current_state, depth=depth-1, x=i, y=j, maxi=False) #(v, x, y)
                        if v==408 and x==408 and y==408:
                            return (408,408,408)
                        L_move.append((v,i,j))
                    else:
                        self.current_state[i][j] = 'b'
                        (v, x, y) = self.minimax(self.current_state, depth=depth-1, x=i, y=j, maxi=True)
                        if v==408 and x==408 and y==408:
                            return (408,408,408)
                        L_move.append((v,i,j))
                    self.current_state[i][j] = '.'
        end = time.time()
        if depth==min(self.d1, self.d2):
            self.exec_time += end-start
        if self.exec_time>self.t:
            return (408,408,408)
        if maxi: #with struct from TA, can return (v, None, None)
            return (sorted(L_move, key=lambda x: x[0])[-1])
        else :
            return (sorted(L_move, key=lambda x: x[0])[0])
    
    def alphabeta(self, parent_board, depth, alpha=-2, beta=2, x=None, y=None, maxi=False):
        # Maximizing for 'w' and minimizing for 'b'
        start = time.time()
        result = self.is_end()
        if result == 'w':
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            if self.player_turn == 'w': 
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                end = time.time()
                #self.exec_time += end-start
            return (1000000, x, y)
        elif result == 'b':
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            if self.player_turn == 'w': 
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                end = time.time()
                self.exec_time += end-start
            end = time.time()
            #self.exec_time += end-start
            return (-1000000, x, y)
        elif result == '.':
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            if self.player_turn == 'w': 
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                end = time.time()
                #self.exec_time += end-start
            end = time.time()
            #self.exec_time += end-start
            return (0, x, y)
        elif depth == 0:
            self.nb_state += 1
            self.dict_depth_game[max(self.d1, self.d2)-depth] +=  1
            self.dict_ard[max(self.d1, self.d2)-depth] +=  1
            
            if self.player_turn=="w":
                self.dict_depth_game_e1[self.d1-depth] +=  1
                self.dict_depth_e1[self.d1-depth] +=  1
                if self.e_1 == 1:
                    value = self.e1(parent_board)
                else:
                    value = self.e2(parent_board)
            else:
                self.dict_depth_game_e2[self.d2-depth] +=  1
                self.dict_depth_e2[self.d2-depth] += 1
                if self.e_2 == 1:
                    value = self.e1(parent_board)
                else:
                    value = self.e2(parent_board)
            return (value, x, y)
        
        
        L_move = list()
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if maxi:
                        self.current_state[i][j] = 'w'
                        (v, x, y) = self.alphabeta(self.current_state, depth=depth-1, alpha=alpha, beta=beta,x=i, y=j, maxi=False)
                        if v==408 and x==408 and y==408:
                            return (408,408,408)
                        L_move.append((v,i,j))
                    else:
                        self.current_state[i][j] = 'b'
                        (v, x, y) = self.alphabeta(self.current_state, depth=depth-1, alpha=alpha, beta=beta,x=i, y=j, maxi=True)
                        if v==408 and x==408 and y==408:
                            return (408,408,408)
                        L_move.append((v,i,j))
                    self.current_state[i][j] = '.'
                    if maxi:
                        L_sorted = sorted(L_move, key=lambda x: x[0])[-1]
                        if L_sorted[0] >= beta:
                            return  L_sorted
                        if L_sorted[0] > alpha:
                            alpha = L_sorted[0]
                    else:
                        L_sorted = sorted(L_move, key=lambda x: x[0])[0]
                        if L_sorted[0] <= alpha:
                            return L_sorted
                        if L_sorted[0] < beta:
                            beta = L_sorted[0]
        end = time.time()
        if depth == min(self.d1, self.d2):
            self.exec_time += end-start
        if self.exec_time>self.t:
            return (408,408,408)
        if maxi: #with struct from TA, can return (v, None, None)
            return (sorted(L_move, key=lambda x: x[0])[-1])
        else :
            return (sorted(L_move, key=lambda x: x[0])[0])

    def play(self):
        print(f"\nn:{self.n}  b:{self.b}  s:{self.s}  t:{self.t}")
        self.txt +=f"\nn:{self.n}  b:{self.b}  s:{self.s}  t:{self.t}\n\n"
        if self.b != 0:
            for block in self.pos_block:
                self.txt += f'{block} | '
            self.txt += '\n'
        self.txt += 'Player 1:\n'
        self.txt += f"    Controlled by {self.p1}\n"
        self.txt += f"    Depth of the search: {self.d1}\n"
        self.txt += f"    Minimax or AlphaBeta (0/1): {self.a1}\n"
        self.txt += f"    Euristic used: e{self.e_1}\n"
        self.txt += 'Player 2:\n'
        self.txt += f"    Controlled by {self.p2}\n"
        self.txt += f"    Depth of the search: {self.d2}\n"
        self.txt += f"    Minimax or AlphaBeta (0/1): {self.a2}\n"
        self.txt += f"    Euristic used: e{self.e_2}\n"
        
        self.draw_board()
        alph = string.ascii_uppercase[0:self.n]
        
        while True:
            self.nb_state = 0   
            self.exec_time = 0 
            self.dict_depth_e1 = {i:0 for i in range(0,self.d1+1)}
            self.dict_depth_e2 = {i:0 for i in range(0,self.d2+1)} 
            self.dict_ard = {i:0 for i in range(0,max(self.d1, self.d2)+1)}
            if self.check_end():
                return
            
            if self.player_turn == 'w':
                self.nb_e1 += 1
                if self.a1 == self.MINIMAX:   
                    (v, x, y) = self.minimax(self.current_state, self.d1, maxi=True)
                else:
                    (v, x, y) = self.alphabeta(self.current_state, self.d1, maxi=True)
                if v==408 and x==408 and y==408:
                        self.switch_player()
                        print(f"Heuristic is too slow, player {self.player_turn} wins !")
                        self.txt +=f"\nHeuristic is too slow, player {self.player_turn} wins !"
                        if self.player_turn == 'w':
                            self.winner = 'w'
                        else :
                            self.winner = 'b'
                        break
            else:
                self.nb_e2 += 1
                if self.a2 == self.MINIMAX:   
                    (v, x, y) = self.minimax(self.current_state, self.d2, maxi=False)
                else:
                    (v, x, y) = self.alphabeta(self.current_state, self.d2, maxi=False)
                if v==408 and x==408 and y==408:
                        self.switch_player()
                        print(f"Heuristic is too slow, player {self.player_turn} wins !")
                        self.txt +=f"\nHeuristic is too slow, player {self.player_turn} wins !"
                        if self.player_turn == 'w':
                            self.winner = 'w'
                        else :
                            self.winner = 'b'
                        break
            
            
            if (self.player_turn == 'w' and self.p1 == self.HUMAN) or (self.player_turn == 'b' and self.p2 == self.HUMAN):
                if self.recommend:
                    self.draw_board()
                    print(F'Recommended move: x = {alph[x]}, y = {y}')
                    self.txt +=F'\nRecommended move: x = {alph[x]}, y = {y}'
                (x,y) = self.input_move(self.player_turn)
                is_ai = False
                print(F'Player {self.player_turn} plays: x = {alph[x]}, y = {y}')
                self.txt +=F'\nPlayer {self.player_turn} plays: x = {alph[x]}, y = {y}'
                self.draw_board()
                print(F'i   Evaluation time: {self.exec_time}s')
                self.txt +=F'\ni   Evaluation time: {self.exec_time}s'
                print(f"ii  Number of state evaluated: {self.nb_state}")
                self.txt +=f"\nii  Number of state evaluated: {self.nb_state}"
                if self.player_turn == "w":
                    self.t_e1 += self.exec_time
                    print(f"iii Number of state evaluated for each depth: {self.dict_depth_e1}")
                    self.txt +=f"\niii Number of state evaluated for each depth: {self.dict_depth_e1}"
                    mean = 0
                    for key, item in self.dict_depth_e1.items():
                        mean += key*item
                    mean /= sum(self.dict_depth_e1.values())
                    print(f"iv  Average evaluation depth: {mean}")
                    self.txt +=f"\niv  Average evaluation depth: {mean}"
                    print(f"v   ARD: {self.get_ard()}")
                    self.txt +=f"\nv   ARD: {self.get_ard()}"
                    self.ard_e1 += self.get_ard()
                else:
                    self.t_e2 += self.exec_time
                    print(f"iii Number of state evaluated for each depth: {self.dict_depth_e2}")
                    self.txt +=f"\niii Number of state evaluated for each depth: {self.dict_depth_e2}"
                    mean = 0
                    for key, item in self.dict_depth_e2.items():
                        mean += key*item
                    mean /= sum(self.dict_depth_e2.values())
                    print(f"iv  Average evaluation depth: {mean}")
                    self.txt +=f"\niv  Average evaluation depth: {mean}"
                    print(f"v   ARD: {self.get_ard()}")
                    self.txt +=f"\nv   ARD: {self.get_ard()}"
                    self.ard_e2 += self.get_ard()
            if (self.player_turn == 'w' and self.p1 == self.AI) or (self.player_turn == 'b' and self.p2 == self.AI):
                if self.recommend:
                    is_ai = True
                    self.input_move(self.player_turn, AI=is_ai, coord=(x,y))
                    print(F'Player {self.player_turn} under AI control plays: x = {alph[x]}, y = {y}')
                    self.txt +=F'\nPlayer {self.player_turn} under AI control plays: x = {alph[x]}, y = {y}'
                    self.draw_board()
                    print(F'i   Evaluation time: {self.exec_time}s')
                    self.txt +=F'\ni   Evaluation time: {self.exec_time}s'
                    print(f"ii  Number of state evaluated: {self.nb_state}")
                    self.txt +=f"\nii  Number of state evaluated: {self.nb_state}"
                if self.player_turn == "w":
                    self.t_e1 += self.exec_time
                    print(f"iii Number of state evaluated for each depth: {self.dict_depth_e1}")
                    self.txt +=f"\niii Number of state evaluated for each depth: {self.dict_depth_e1}"
                    mean = 0
                    for key, item in self.dict_depth_e1.items():
                        mean += key*item
                    mean /= sum(self.dict_depth_e1.values())
                    print(f"iv  Average evaluation depth: {mean}")
                    self.txt +=f"\niv  Average evaluation depth: {mean}"
                    print(f"v   ARD: {self.get_ard()}")
                    self.txt +=f"\nv   ARD: {self.get_ard()}"
                    self.ard_e1 += self.get_ard()
                else:
                    self.t_e2 += self.exec_time
                    print(f"iii Number of state evaluated for each depth: {self.dict_depth_e2}")
                    self.txt +=f"\niii Number of state evaluated for each depth: {self.dict_depth_e2}"
                    mean = 0
                    for key, item in self.dict_depth_e2.items():
                        mean += key*item
                    mean /= sum(self.dict_depth_e2.values())
                    print(f"iv  Average evaluation depth: {mean}")
                    self.txt +=f"\niv  Average evaluation depth: {mean}"
                    print(f"v   ARD: {self.get_ard()}")
                    self.txt +=f"\nv   ARD: {self.get_ard()}"
                    self.ard_e2 += self.get_ard()
                
                
            self.switch_player()
            print("\n---------------------\n")
            self.txt += "\n---------------------\n"

def main(): 
    g = Game(recommend=True)
    g.play()
    #g.play(algo=Game.MINIMAX,player_1=Game.AI,player_2=Game.HUMAN)
    g.save()

if __name__ == "__main__":
    main()


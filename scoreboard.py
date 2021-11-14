# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 05:06:01 2021

@author: BaptLemaire
lemaire.baptiste@outlook.fr

Subject : scoreboard for Line'em up AI
"""

from li import Game


r = 5
nw_e1 = 0
nw_e2 = 0
t_e1 = 0
t_e2 = 0
dict_e1 = {i:0 for i in range(7)} #g.e_1+1
dict_e2 = {i:0 for i in range(7)} #g.e_2+1
nb_state_e1=0
nb_state_e2=0
ard_e1 = 0
ard_e2 = 0
nb_move_e1 = 0
nb_move_e2 = 0
for i in range(r):
    g = Game()
    g.play()
    t_e1 += g.t_e1
    t_e2 += g.t_e2
    for it, val in g.dict_depth_game_e1.items():
        dict_e1[it] += val
    for it, val in g.dict_depth_game_e2.items():
        dict_e2[it] += val
    ard_e1 += g.ard_e1
    ard_e2 += g.ard_e2
    nb_move_e1 += g.nb_e1
    nb_move_e2 += g.nb_e2
    if g.winner=='w':
        nw_e1+=1
    else:
        nw_e2+=1
    
for i in range(r):
    g = Game()
    tmp = g.e_1
    g.e_1 = g.e_2
    g.e_2 = tmp
    tmp = g.a1
    g.a1 = g.a2
    g.a2 = tmp
    tmp = g.d1
    g.d1 = g.d2
    g.d2 = tmp
    g.dict_depth_e1 = {i:0 for i in range(0,g.d1+1)}
    g.dict_depth_e2 = {i:0 for i in range(0,g.d2+1)}
    g.dict_depth_game = {i:0 for i in range(0,max(g.d1, g.d2)+1)}
    g.dict_depth_game_e1 = {i:0 for i in range(0,g.d1+1)}
    g.dict_depth_game_e2 = {i:0 for i in range(0,g.d2+1)}
    g.play()
    t_e1 += g.t_e2
    t_e2 += g.t_e1
    for it, val in g.dict_depth_game_e1.items():
        dict_e2[it] += val
    for it, val in g.dict_depth_game_e2.items():
        dict_e1[it] += val
    ard_e1 += g.ard_e2
    ard_e2 += g.ard_e1
    nb_move_e1 += g.nb_e2
    nb_move_e2 += g.nb_e1
    if g.winner=='w':
        nw_e2+=1
    else:
        nw_e1+=1

tmp = g.e_1
g.e_1 = g.e_2
g.e_2 = tmp
tmp = g.a1
g.a1 = g.a2
g.a2 = tmp
tmp = g.d1
g.d1 = g.d2
g.d2 = tmp


f = open("scoreboard.txt","a",encoding="utf-8")
f.write(f"\n\nn:{g.n}  b:{g.b}  s:{g.s}  t:{g.t}\n")
f.write('Player 1:\n')
f.write(f"    Depth of the search: {g.d1}\n")
f.write(f"    Minimax or AlphaBeta (0/1): {g.a1}\n")
f.write(f"    Heuristic used: e{g.e_1}\n")
f.write('Player 2:\n')
f.write(f"    Depth of the search: {g.d2}\n")
f.write(f"    Minimax or AlphaBeta (0/1): {g.a2}\n")
f.write(f"    Heuristic used: e{g.e_2}\n")

f.write(f"\n2x{r}={2*r} games\n")
f.write(f"\nTotal wins for heuristic e1: {nw_e1} ({(round((nw_e1/(2*r))*100,2))}%)\n")
f.write(f"Total wins for heuristic e2: {nw_e2} ({(round((nw_e2/(2*r))*100,2))}%)\n")
f.write("\nFor Heuristic 1: \n")
f.write(f"i   Average evaluation time: {round(t_e1/(2*r),2)}s\n")
f.write(f"ii  Total heuristic evaluations: {sum(dict_e1.values())}\n")
mean = 0
for key, item in dict_e1.items():
    mean += key*item
mean /= sum(dict_e1.values())
f.write(f"iii Evaluation by depth: {dict_e1}\n")
f.write(f"iv  Average evaluation depth: {mean}\n")
f.write(f"v   Average recursion path: {ard_e1/(2*r)}\n")
f.write(f"vi  Average moves per game: {nb_move_e1/(2*r)}\n")
f.write("\nFor Heuristic 2: \n")
f.write(f"i   Average evaluation time: {round(t_e2/(2*r),2)}s\n")
f.write(f"ii  Total heuristic evaluations: {sum(dict_e2.values())}\n")
mean = 0
for key, item in dict_e2.items():
    mean += key*item
mean /= sum(dict_e2.values())
f.write(f"iii Evaluation by depth: {dict_e2}\n")
f.write(f"iv  Average evaluation depth: {mean}\n")
f.write(f"v   Average recursion path: {ard_e2/(2*r)}\n")
f.write(f"vi  Average moves per game: {nb_move_e2/(2*r)}\n")

f.close()





# COMP472-Assig2
## by Baptiste Lemaire (id: 40216482)

You can find in the repository two python files. "line_em_up_skeleton.py" is the game itself with the two heuristics.
To save a game, you can uncomment the method Game.save() line 778.
The second python file is "scoreboard.py". This file will play 2xr games with the given configuration.
To use "scoreboard.py", the easiest way is to comment all the input in Game.__init__() and to manually gives the parameters. 
By doing that, you don't have to give the parameters for each run. 
You still have to specify *d1+1* and *d2+1* in lines 19,20 before executing the program.
You can find in the folder "quest_2_6" the eight output files asked in the section 2.6.
Last, you can find the text file "performances.txt". There, I discuss about the performances of my two heuristic functiond.


### Execute the code in console
To draw the board, the python files use specific characters (black circle and white circle).
Therefore, the encoding I/O stream needs to be "utf-8". To change the encoding, please input the two following commands :

chcp 65001

set PYTHONIOENCODING=utf-8

Furthermore, many consoles have black background. So the white cirlce can appear black and the black circle can appear white.

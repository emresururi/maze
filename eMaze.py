import df_maze
from df_maze import random
random.seed(371)

import numpy as np
#import copy

class eMaze(df_maze.Maze):
    def __init__(self, nx, ny, ix=0, iy=0):
        df_maze.Maze.__init__(self,nx,ny,ix,iy)
    def update_wall(self,x,y,wall_dir,state):
        "Updates the state wall of the cell at x,y"
        "and its neighbour"
        delta = {"N":(0,-1),"S":(0,1),"W":(-1,0),"E":(1,0)}
        opposite = {"N":"S","S":"N","E":"W","W":"E"}
        this_cell = self.cell_at(x,y)
        #print(this_cell.walls)
        #print(self.nx,self.ny)

        neigh_x,neigh_y = np.array(delta[wall_dir])+np.array([x,y])
        #print(neigh_x,neigh_y)
        if(neigh_x>=0 and neigh_x<self.nx and neigh_y>=0 and neigh_y<self.ny):
            self.cell_at(neigh_x,neigh_y).walls[opposite[wall_dir]]=state
            this_cell.walls[wall_dir] = state
        #print(this_cell.walls)
    def solve_from_to(self,x0y0,x1y1):
        # Solves the path from (x0,y0) to (x1,y1)
        # using cellular automata.
        # Returns the steps' coordinates
        x0 = x0y0[0]
        y0 = x0y0[1]
        x1 = x1y1[0]
        y1 = x1y1[1]
        arr_states = np.full((self.nx,self.ny),"O",dtype=str)
        arr_states[x0,y0] = 'S'
        arr_states[x1,y1] = 'E'
        # Defining a canvas to apply the filter
        # for our playground
        canvas = np.empty((self.nx,self.ny),dtype=object)
        for x in range(self.nx):
            for y in range(self.ny):
                canvas[x,y] = (x,y)

        state2logic = {"S":False,"E":False,"O":False,"X":True}
        neigh2state = ["O","O","O","X"]
        filt = arr_states=="O"
        num_Os = np.sum(filt)

        num_Os_pre = self.nx * self.ny * 10
        while (num_Os < num_Os_pre):
            for xy in canvas[filt]:
                num_Os_pre = num_Os
                x, y = xy
                walls = np.array(list(self.cell_at(x, y).walls.values()))

                # N-S-E-W

                neighbours = np.array([True, True, True, True])
                try:
                    neighbours[0] = state2logic[arr_states[x, y - 1]]
                except:
                    pass
                try:
                    neighbours[1] = state2logic[arr_states[x, y + 1]]
                except:
                    pass
                try:
                    neighbours[2] = state2logic[arr_states[x + 1, y]]
                except:
                    pass
                try:
                    neighbours[3] = state2logic[arr_states[x - 1, y]]
                except:
                    pass
                res = np.logical_or(walls, neighbours)
                arr_states[x, y] = neigh2state[np.sum(res)]
            filt = arr_states == "O"
            num_Os = np.sum(filt)

        pos_start = canvas[arr_states == "S"][0]
        path_line = np.array([pos_start])
        # path_line = append(path_line, pos_start)
        pos_end = canvas[arr_states == "E"][0]
        # print(pos_start)
        pos = pos_start
        pos_pre = (-1, -1)
        step = 0
        arr_path = np.full((self.nx, self.ny), "", dtype=object)
        arr_path[pos_start[0], pos_start[1]] = "S"
        arr_path[pos_end[0], pos_end[1]] = "E"
        while (pos != pos_pre):
            pos_pre = pos
            step += 1
            possible_ways = np.array(list(self.cell_at(pos[0], pos[1]).walls.values())) == False
            dirs = np.array(["N", "S", "E", "W"])
            # print(pos)

            # print(dirs[possible_ways])
            delta = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
            for dir in dirs[possible_ways]:
                if (arr_states[pos[0] + delta[dir][0], pos[1] + delta[dir][1]] == "O" and arr_path[
                    pos[0] + delta[dir][0], pos[1] + delta[dir][1]] == ""):
                    arr_path[pos[0] + delta[dir][0], pos[1] + delta[dir][1]] = "{}".format(step)
                    pos = (pos[0] + delta[dir][0], pos[1] + delta[dir][1])
                    path_line = np.append(path_line, [pos], axis=0)
                    break
        path_line = np.append(path_line, [pos_end], axis=0)
        return path_line
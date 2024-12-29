import numpy 
import random
import copy
from Random_Maze.DFS import Maze_DFS
from Random_Maze.Prime import Maze_Prime


class Maze_Gen:
    ''' Main generation maze with three algorithm DFS, Prime, and Wilson.
        DFS and Prime work in a tree that purpose to random generate a spanning tree from start point to goal.
        In constract, Wilson work on a graph cycle, then it can creat a maze with more than one path from start point to goal.
        ''' 
    def __init__(self, cols , rows, maze_name = 'Maze_DFS'):
        self.cols = cols 
        self.rows = rows 
        self.maze_name = maze_name
        self.maze_algorithm = {'Maze_DFS':Maze_DFS(self.rows, self.cols),
                                'Maze_Prime': Maze_Prime(self.rows, self.cols),
                                'Maze_Prime_Cycle': Maze_Prime(self.rows, self.cols)}
        self.maze = None
        self.start = None 
        self.goal = None 

    def reset_start(self, node_goal, step = 20):
        ''' fix goal, and traversal to new start location ''' 
        new_start = node_goal
        maze_copy = copy.deepcopy(self.maze)
        for t in range(step):
            # random direction
            valid_dir = []
            for dr in [(0,1),(1,0),(-1,0),(0,-1)]:
                x_new, y_new = new_start[0] + dr[0], new_start[1] + dr[1]
                if 0<= x_new < self.rows*2-1 and 0 <= y_new < self.cols*2 -1 :
                    if maze_copy[x_new][y_new] == 0:
                        valid_dir.append((x_new, y_new))
            if valid_dir == []:
                break 
            maze_copy[new_start[0]][new_start[1]] = -1
            new_start = random.choice(valid_dir)

        return new_start

    def reset_goal(self, node_start, step = 20):
        ''' fix start location, and traversal to new goal ''' 
        new_goal = node_start
        maze_copy = copy.deepcopy(self.maze)
        for t in range(step):
            # random direction
            valid_dir = []
            for dr in [(0,1),(1,0),(-1,0),(0,-1)]:
                x_new, y_new = new_goal[0] + dr[0], new_goal[1] + dr[1]
                if 0<= x_new < self.rows*2-1 and 0 <= y_new < self.cols*2 -1 :
                    if maze_copy[x_new][y_new] == 0:
                        valid_dir.append((x_new, y_new))
            if valid_dir == []:
                break 
            maze_copy[new_goal[0]][new_goal[1]] = -1
            new_goal = random.choice(valid_dir)
        return new_goal
    
    def gen(self):
        if self.maze_name == 'Maze_Prime_Cycle':
            self.maze, self.start , self.goal = self.maze_algorithm[self.maze_name].generator(cycle = True)
        else:
            self.maze, self.start , self.goal = self.maze_algorithm[self.maze_name].generator()


if __name__ == '__main__':
    gen = Maze_Gen(cols = 5, rows= 6, maze_name= 'Maze_Prime')

    gen.gen()

    print(gen.maze)
    print(gen.start)
    print(gen.goal)

        
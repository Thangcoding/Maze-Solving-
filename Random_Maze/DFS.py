import random 

class Maze_DFS:
    ''' DFS algorithm purpose for find the path of all node, 
        that mean with find a random spanning tree of a graph cycle.'''
    
    def __init__(self, rows , cols):
        self.rows = rows
        self.cols = cols 

        self.graph = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.maze = [[-1 for _ in range(self.cols*2-1)] for _ in range(self.rows*2-1)]
        self.moves = [(1,0), (0,1), (0,-1),(-1,0)]
        self.start = None 
        self.goal = None 

    def is_valid(self, node):
        ''' check is valid node to traversal '''
        if 0 <= node[0] < self.rows and 0 <= node[1] < self.cols:
            if self.graph[node[0]][node[1]] == None and  node != self.start:
                return True 
        return False 

    def traversal(self, start_node):
        ''' Traversal to find a random spanning tree from cycle graph '''
        stack = [start_node] 
        curr_node = start_node
        space_utilize = self.rows*self.cols - 1 
        while space_utilize > 0: 
        
            neighboors = self.unvisited_node(curr_node)
            if len(neighboors) == 0:
                # all neighboors are visited 
                stack.pop(0)
                if stack == []:
                    return curr_node 
                    break 
                curr_node = stack[0] 
            else:
                next_node = random.choice(neighboors) 
                self.graph[next_node[0]][next_node[1]] = curr_node   
                stack = [next_node] + stack                         
                curr_node = next_node             
                space_utilize -= 1  
        return curr_node 

    def unvisited_node(self,node):
        ''' find all possible neighboors node  '''
        neighboors = []
        for walk in self.moves:
            next_node = (node[0] + walk[0], node[1] + walk[1])
            if self.is_valid(next_node):
                neighboors.append(next_node)
        return neighboors
    
    def generator(self):
        ''' generate maze space by break the location and the wall between each node follow by the path generated '''
        self.start = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
        self.goal = self.traversal(self.start)
        # mapping node of graph in maze (i, j) --> (i*2 , j*2)
        self.start = (self.start[0]*2 , self.start[1]*2)
        self.goal = (self.goal[0]*2 , self.goal[1]*2)

        # break the wall and location
        for i in range(self.rows):
            for j in range(self.cols):

                # break location 
                if self.graph[i][j] == None: 
                    # that is start node 
                    continue 
                # (i,j) --> (i*2, j*2) :  represent for mapping node from graph in maze 

                # break wall 
                self.maze[i*2][j*2] = 0  

                # break wall 
                path_x , path_y = self.graph[i][j] 
                if  path_x*2 < (self.rows*2 -1) and path_y*2 < (self.cols*2 -1):
                    self.maze[path_x*2][path_y*2] = 0 
                # direction path 
                d_x , d_y = (path_x - i,  path_y - j)
                
                if (i*2 + d_x) < (self.rows*2 -1) and (j*2 + d_y) < (self.cols*2 -1):
                    self.maze[i*2 +d_x][j*2 + d_y] = 0 

        # break location start and goal
        self.maze[self.start[0]][self.start[1]] = 0 
        self.maze[self.goal[0]][self.goal[1]] = 1 

        return self.maze, self.start , self.goal 

if __name__ == '__main__':
    gen = Maze_DFS(rows= 5, cols= 4)

    maze , start, goal = gen.generator()

    print(start)
    print(maze)
    print(goal)



 




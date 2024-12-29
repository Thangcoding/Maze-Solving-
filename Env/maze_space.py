import numpy as np 


class Maze_Space:

    def __init__(self, raw_space, goal):
        # 'wall': -2, 'path': -1, 'goal': 1
        self.raw_space = raw_space
        self.goal = goal 

    def reward_function(self, done):
        if done == 'OUT':
            return -1000
        elif done == 'WALL':
            return -1000
        elif done == 'PATH':
            return -10
        else:
            return 10000
    def step(self,state = (int, int), action = (int, int)):
        ''' interating with environment '''
        next_state = (state[0] + action[0], state[1] + action[1])

        # Agent go to outside of maze
        if not (( 0 <= next_state[0] < len(self.raw_space)) and (0 <= next_state[1] < len(self.raw_space[0]))):
            return (None,self.reward_function('OUT'), 'OUT')
        
        # Agent go to wall 
        if self.raw_space[next_state[0]][next_state[1]] == -1:
            return (next_state,self.reward_function('WALL'), 'WALL')

        # Agent follow normal path which not reach on goal 
        if self.raw_space[next_state[0]][next_state[1]] == 0:
            return (next_state ,self.reward_function('PATH'),'PATH')

        # Agent reach to goal
        return (next_state, self.reward_function('GOAL'),'GOAL')

    def reset(self):
        ''' reset old environment  '''
        pass 
    def render(self):
        ''' showing the state of agent in raw space (simple visualize) '''
        pass

if __name__ == '__main__':
    pass 

import numpy as np 
import random 
from Env.maze_space import Maze_Space


EPSILON = 0.2
class Q_Learning:
    def __init__(self, gamma):

        # setup config 
        self.gamma = gamma
        self.lr = 0.1

        # decode action
        self.decode_action = {'LEFT': (0, -1), 'RIGHT': (0, 1), 'UP': (-1,0), 'DOWN': (1, 0)}

        # initial transition
        self.transition = {}

    def policy(self,state):
        # Epsilon-Greedy policy 
        if random.random() < 1-EPSILON:
            action = sorted(self.transition[state].keys(), key=lambda action: self.transition[state][action][0])[-1]
            return action
        else:
            # no exploration action valid 
            lst_action = sorted(self.transition[state].keys(), key=lambda action: self.transition[state][action][1])
            valid_action = [action for action in lst_action if self.transition[state][action][2] != 'WALL']
            return valid_action[0]
    def run(self,state):
        action = sorted(self.transition[state].keys(), key=lambda action: self.transition[state][action][0])[-1]
        return action
    def reset(self):
        self.transition = {}
    def set_config(self, gamma):
        self.gamma = gamma
                            
    def learn(self, state,env):
        ''' transition of Agent follow the format : 
                        state : {'action': (reward, numbers_visited , get)} 
        '''
        # update state 
        if state not in self.transition:
            self.transition.update({state: {'LEFT': [0, 0 , None] , 'RIGHT': [0, 0, None] , 'UP': [0,0, None] , 'DOWN': [0, 0 , None]}})
        
        # interacting with environment 
        action = self.policy(state)
        
        action_decode = self.decode_action[action]
        # repones from environment 
        next_state, reward , done  = env.step(state,action_decode)
        if done == 'OUT':
            # go over the maze 
            del self.transition[state][action]
            return (None,reward, done)

        # update Q-value 
        if next_state not in self.transition:
            # update state 
            self.transition.update({next_state: {'LEFT':[0, 0 , None]  , 'RIGHT':[0, 0 , None] , 'UP': [0,0,None] , 'DOWN': [0, 0 , None]}})
            # update getting 
            self.transition[state][action][2] = done 
            # update number visited 
            self.transition[state][action][1] += 1
            # update bellman equaltion
            self.transition[state][action][0] = reward
        
        else: 
            # update getting 
            self.transition[state][action][2] = done 
            # update numbers visited 
            self.transition[state][action][1] += 1
            # update bellman equaltion
            self.transition[state][action][0] = self.transition[state][action][0] + self.lr*(reward + self.gamma*max([value[0] for value in self.transition[next_state].values()]) - self.transition[state][action][0])
        
        if done == 'GOAL':
            # reset number transition 
            for state in self.transition:
                for action in ['LEFT','RIGHT','UP','DOWN']:
                    if action in self.transition[state]:
                        self.transition[state][action][1] = 0

        return next_state,reward,done 
         
    def solve(self, state):
        action = self.run(state)
        action_decode = self.decode_action[action]
        next_state = (state[0] + action_decode[0], state[1] + action_decode[1])

        return next_state 
if __name__ =='__main__':
    pass 

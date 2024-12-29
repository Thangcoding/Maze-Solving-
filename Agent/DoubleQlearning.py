import random

EPSILON = 0.2

class Double_Qlearning:
    '''  Double Q-learning using two table to learn and select action 
    helping for stable learning than normal Q-learning    '''
    def __init__(self, gamma):

        # setup config 
        self.gamma = gamma 
        self.lr = 0.15 

        # decode action
        self.decode_action = {'LEFT': (0, -1), 'RIGHT': (0, 1), 'UP': (-1,0), 'DOWN': (1, 0)}

        # two table Q value 
        self.transition = {}
        self.table_select = 0
    
    def policy(self, state):
        if random.random() < 1-EPSILON:
            if self.table_select == 0:
                action = sorted(self.transition[state].keys(), key = lambda action: (self.transition[state][action][0]))[-1]
            else:
                action = sorted(self.transition[state].keys(), key = lambda action: (self.transition[state][action][1]))[-1]
            return action
        else:
            lst_action = sorted(self.transition[state].keys(), key=lambda action: self.transition[state][action][2])
            valid_action = [action for action in lst_action if self.transition[state][action][3] != 'WALL']
            return valid_action[0]

    def set_config(self,gamma):
        self.gamma = gamma

    def run(self, state):
        action = sorted(self.transition[state].keys(), key = lambda action: (self.transition[state][action][0] + self.transition[state][action][1]))[-1]
        return action

    def reset(self):
        self.transition = {}

    def learn(self, state, env):
        ''' transition of Agent follow the format : 
                        state : {'action': (reward_1, reward_2, numbers_visited , get)} 
        '''
        # update state 
        if state not in self.transition:
            self.transition.update({state: {'LEFT': [0, 0 , 0, None] , 'RIGHT': [0, 0, 0, None] , 'UP': [0,0,0, None] , 'DOWN': [0, 0 ,0, None]}})
        
        # interacting with environment 
        action = self.policy(state) 
        
        action_decode = self.decode_action[action]
        # repones from environment 
        next_state, reward , done  = env.step(state,action_decode)
        if done == 'OUT':
            # go over the maze 
            del self.transition[state][action]
            return (None,reward, done) 
        
        # update two Q-values with equaly probability 
        if next_state not in self.transition:
            # update state 
            self.transition.update({next_state: {'LEFT':[0, 0 , 0, None]  , 'RIGHT':[0, 0, 0, None] , 'UP': [0, 0, 0, None] , 'DOWN': [0, 0, 0, None]}})
            # update getting 
            self.transition[state][action][3] = done 
            # update number visited 
            self.transition[state][action][2] += 1

            # update bellman equaltion 
            self.transition[state][action][0] = reward
            self.transition[state][action][1] = reward
        else: 
            # update getting                                           
            self.transition[state][action][3] = done                 
            # update numbers visited 
            self.transition[state][action][2] += 1
            # update bellman equaltion
            if self.table_select == 0:
                self.transition[state][action][0] = self.transition[state][action][0] + self.lr*(reward + self.gamma*max([value[1] for value in self.transition[next_state].values()]) - self.transition[state][action][0])
                self.table_select = 1
            else:
                self.transition[state][action][1] = self.transition[state][action][1] + self.lr*(reward + self.gamma*max([value[0] for value in self.transition[next_state].values()]) - self.transition[state][action][1])
                self.table_select = 0
        
        if done == 'GOAL':
            # reset number transition 
            for state in self.transition:
                for action in ['LEFT','RIGHT','UP','DOWN']:
                    if action in self.transition[state]:
                        self.transition[state][action][2] = 0
                    
        return next_state,reward,done
    def solve(self,state):
        action = self.run(state)
        action_decode = self.decode_action[action]
        next_state = (state[0] + action_decode[0], state[1] + action_decode[1])

        return next_state

if __name__ == '__main__':
    pass  

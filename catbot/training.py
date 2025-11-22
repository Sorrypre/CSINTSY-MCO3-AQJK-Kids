import random
import time
from typing import Dict
import numpy as np
import pygame
from utility import play_q_table
from cat_env import make_env
#############################################################################
# TODO: YOU MAY ADD ADDITIONAL IMPORTS OR FUNCTIONS HERE.                   #
#############################################################################


def get_next_state(state: int, action: int):

    #Move up if the action is 0
    #Check if the current state is within bounds of the map it must be greater than zero
    #moving up means the row value gets lesser (Ex. 1000 -> 0000)
    if action == 0 and state // 1000 > 0:
        state -= 1000
    #Move down if the action is 1
    #Check if the current state is within bounds of the map it must be less than 7 (max coordinate we can have)
    #moving up means the row value gets lesser (Ex. 1000 -> 2000)
    elif action == 1 and state // 1000 < 7:
        state += 1000
    #Move up if the action is 2
    #Check if the current state is within bounds of the map it must be greater than zero
    #moving up means the row value gets lesser (Ex. 7120 -> 7020)
    elif action == 2 and (state // 100) % 10 > 0:
        state -= 100
    #Move down if the action is 3
    #Check if the current state is within bounds of the map it must be less than 7 (max coordinate we can have)
    #moving up means the row value gets lesser (Ex. 7120 -> 7220)
    elif action == 3 and (state // 100) % 10 < 7:
        state += 100
    # does not move so everything stays the same
    elif action == 4:
        state = state
    else: print("State or action not within bounds")
    return state

#Note ni Jens: make sure to only put valid states kasi for now di pa nachecheck 8888 for example should not b
def is_goal_state(state):
    isGoalState = False
    if (state // 100) == (state % 100):
        isGoalState = True
    return isGoalState






#############################################################################
# END OF YOUR CODE. DO NOT MODIFY ANYTHING BEYOND THIS LINE.                #
#############################################################################

def train_bot(cat_name, render: int = -1):
    env = make_env(cat_type=cat_name)
    
    # Initialize Q-table with all possible states (0-9999)
    # Initially, all action values are zero.
    q_table: Dict[int, np.ndarray] = {
        state: np.zeros(env.action_space.n) for state in range(10000)
    }

    # Training hyperparameters
    episodes = 5000 # Training is capped at 5000 episodes for this project
    
    #############################################################################
    # TODO: YOU MAY DECLARE OTHER VARIABLES AND PERFORM INITIALIZATIONS HERE.   #
    #############################################################################
    # Hint: You may want to declare variables for the hyperparameters of the    #
    # training process such as learning rate, exploration rate, etc.            #
    #############################################################################
    
    # All the hyperparameters: alpha, gamma, epsilon, max_steps, minimum_epsilon

    #Learning rate
    alpha = 0.8
    #discount factor
    gamma = 0.95
    #exploration rate
    epsilon = 0.2
    #maximum steps the bot can take
    max_steps = 60









    
    #############################################################################
    # END OF YOUR CODE. DO NOT MODIFY ANYTHING BEYOND THIS LINE.                #
    #############################################################################
    
    for ep in range(1, episodes + 1):
        ##############################################################################
        # TODO: IMPLEMENT THE Q-LEARNING TRAINING LOOP HERE.                         #
        ##############################################################################
        # Hint: These are the general steps you must implement for each episode.     #
        # 1. Reset the environment to start a new episode.                           #
        # 2. Decide whether to explore or exploit.                                   #
        # 3. Take the action and observe the next state.                             #
        # 4. Since this environment doesn't give rewards, compute reward manually    #
        # 5. Update the Q-table accordingly based on agent's rewards.                #
        ############################################################################## 
        






























        
        
        #############################################################################
        # END OF YOUR CODE. DO NOT MODIFY ANYTHING BEYOND THIS LINE.                #
        #############################################################################

        # If rendering is enabled, play an episode every 'render' episodes
        if render != -1 and (ep == 1 or ep % render == 0):
            viz_env = make_env(cat_type=cat_name)
            play_q_table(viz_env, q_table, max_steps=100, move_delay=0.02, window_title=f"{cat_name}: Training Episode {ep}/{episodes}")
            print('episode', ep)

    return q_table
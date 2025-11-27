import math
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
from cat_env import CatChaseEnv

#ignore may ganito na pala si sir HAHAHAHA
# def get_next_state(state: int, action: int):

#     #Move up if the action is 0
#     #Check if the current state is within bounds of the map it must be greater than zero
#     #moving up means the row value gets lesser (Ex. 1000 -> 0000)
#     if action == 0 and state // 1000 > 0:
#         state -= 1000
#     #Move down if the action is 1
#     #Check if the current state is within bounds of the map it must be less than 7 (max coordinate we can have)
#     #moving up means the row value gets lesser (Ex. 1000 -> 2000)
#     elif action == 1 and state // 1000 < 7:
#         state += 1000
#     #Move up if the action is 2
#     #Check if the current state is within bounds of the map it must be greater than zero
#     #moving up means the row value gets lesser (Ex. 7120 -> 7020)
#     elif action == 2 and (state // 100) % 10 > 0:
#         state -= 100
#     #Move down if the action is 3
#     #Check if the current state is within bounds of the map it must be less than 7 (max coordinate we can have)
#     #moving up means the row value gets lesser (Ex. 7120 -> 7220)
#     elif action == 3 and (state // 100) % 10 < 7:
#         state += 100
#     # does not move so everything stays the same
#     elif action == 4:
#         state = state
#     else: print("State or action not within bounds")
#     return state

#Note ni Jens: make sure to only put valid states kasi for now di pa nachecheck 8888 for example should not b
def is_goal_state(state):
    return (state // 100) == (state % 100)
    """
    isGoalState = False
    if (state // 100) == (state % 100):
        isGoalState = True
    return isGoalState
    """

def get_action(env: CatChaseEnv, state: int, epsilon: float, q_table: Dict[int, np.ndarray]):
    if np.random.random() < epsilon:
        return env.action_space.sample()
    else:
        return int(np.argmax(q_table[state]))
    
def decay_alpha_epsilon(epsilon, alpha, min_epsilon, min_alpha, epsilon_decay, alpha_decay):
    return max(min_epsilon, epsilon * epsilon_decay), max(min_alpha, alpha * alpha_decay)

#simple reward structure muna na naisip ko lng based sa reference HAHAHA - jens
#pwede raw maglagay ng additional rito dagdagan na lng
def getReward(state: int, moves: int):
    return 60.0 / (max(1, moves) * 2) if is_goal_state(state) else 0.0

def update(q_table: Dict[int, np.ndarray], learning_rate: float, discount_factor: float, state: int, action: int, reward: float, terminated: bool, next_state: int):
    #best na pwede gawin mula sa susunod na state
    future_q_value = (not terminated) * np.max(q_table[next_state])
    
    #Q-value (Bellman equation)
    target = reward + discount_factor * future_q_value

    #Gaano kamali yung estimate
    temporal_diff = target - q_table[state][action]

    # return the updated estimate in the direction of the error
    # learning rate para macontrol yung gaano kalaki yung steps sa pagadjust
    # also multiple assignment para sa training_error
    q_table[state][action] += learning_rate * temporal_diff
    return q_table, temporal_diff

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
    alpha = 0.05
    end_alpha = 0.005
    alpha_decay_until_episode = 3000
    #discount factor
    gamma = 0.95
    #start exploration rate (100% random actions)
    epsilon = 1.0
    end_epsilon = 0.05
    epsilon_decay_until_episode = 3500
    #final exploreation rate (close to zero)    
    #Reducing the exploration over time
    
    # parehong dinerive galing sa ax^b=c -> x=e^(log(c/a)/b)
    # a = start alpha
    # x = decay rate to be identified
    # b = total episodes
    # c = final alpha
    
    # So meron syang 3500 episodes to test out random moves,
    # and then 1500 para magdry run ng kinalabasan ng training nya
    epsilon_decay = math.e ** (math.log(end_epsilon / epsilon) / epsilon_decay_until_episode)
    
    # Para fast learner muna sya sa una tapos saka na sya maging
    # diskumpyado sa pagbabago pag matalino na talaga sya
    alpha_decay = math.e ** (math.log(end_alpha / alpha, math.e) / alpha_decay_until_episode)
    #maximum steps the bot can take
    max_steps = 60
    
    #naka define na pala yung env sa function bruh
    #episodes already defined
    #training_error = []
    last_num_moves = 0
    start_time = time.perf_counter()
    
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
        #done step 1
        state, info = env.reset()
        done = False
        moves = 0
    
        while not done:
            #step 2 
            action = get_action(env, state, epsilon, q_table)
            #step 3
            next_state, reward, terminated, truncated, info = env.step(action)
            #step 4
            moves += 1
            truncated = (moves >= max_steps * 15)
            reward = getReward(next_state, moves)
            #step 5
            q_table, temporal_difference = update(q_table, alpha, gamma, state, action, reward, terminated, next_state)
            #training_error.append(temporal_difference)

            done = terminated or truncated
            state = next_state

        epsilon, alpha = decay_alpha_epsilon(epsilon, alpha, end_epsilon, end_alpha, epsilon_decay, alpha_decay)
        
        #############################################################################
        # END OF YOUR CODE. DO NOT MODIFY ANYTHING BEYOND THIS LINE.                #
        #############################################################################

        # If rendering is enabled, play an episode every 'render' episodes
        if render != -1 and (ep == 1 or ep % render == 0):
            viz_env = make_env(cat_type=cat_name)
            play_q_table(viz_env, q_table, max_steps=max_steps, move_delay=0.02, window_title=f"{cat_name}: Training Episode {ep}/{episodes}")
            print('episode', ep)
        last_num_moves = moves
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Last episode no. moves: {last_num_moves}")
    print(f"Total Training time: {elapsed_time:.3f}")
    return q_table
import pygame
import numpy as np
from environment import Snake_Game
from agent import DQN

pygame.init()
clock = pygame.time.Clock()

run = True
env = Snake_Game()
agent = DQN(env.SCR_WIDTH_PIXEL*env.SCR_HEIGHT_PIXEL, env)

def checkEvent():
    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            global run
            run = False
        else:
            env.checkEvent(e)
    return

def paint():
    env.draw()
    pygame.display.update()
    return

def update():
    checkEvent()
    env.update()
    return

def play():
    while(True):
        if(not run): break
        if(env.plr.alive == False): break
        if(env.plr.completeMovement()):
            if(agent.done == True): break
            action = agent.pick_action(np.array(env.getState()).reshape(env.SCR_WIDTH_PIXEL*env.SCR_HEIGHT_PIXEL,))
            env.postAction(action)
            agent.record(action, np.array(env.emulate(action)).reshape(env.SCR_WIDTH_PIXEL*env.SCR_HEIGHT_PIXEL,))
            agent.replay()
        update()
        paint()
    agent.replay()
    return

def train_agent():
    for i in range(agent.episode):
        #print(i+1)
        agent.setCurrentState(np.array(env.getState()).reshape(env.SCR_WIDTH_PIXEL*env.SCR_HEIGHT_PIXEL,))
        play()
        if(not run): break
        agent.reset()
        env.reset()
    return

while(True):
    agent.get_model()
    agent.setCurrentState(np.array(env.getState()).reshape(env.SCR_WIDTH_PIXEL*env.SCR_HEIGHT_PIXEL,))
    train_agent()
    agent.save_model()
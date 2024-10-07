from model import BasicModel
from player import PygamePlayer
from display import PygameDisplay

import pygame

model = BasicModel()

player = PygamePlayer(PygamePlayer.DEFAULT_BINDINGS)

display = PygameDisplay({})

model.reset()
while True:
    actions = player.get_actions()
    state = model.update(actions)
    display.update(state)

    pygame.event.pump()

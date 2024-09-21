# taken from # Taken from https://github.com/AlejoG10/python-chess-ai-yt/blob/master/src/sound.py


import pygame


class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)

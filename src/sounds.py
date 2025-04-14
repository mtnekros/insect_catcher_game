import pygame
from pygame.mixer import music

pygame.mixer.init()

def play_bg_music() -> None:
    """Play background music."""
    music.load("./assets/music/bg.mp3")
    music.play(-1)

def stop_bg_music() -> None:
    """Stop background music."""
    music.stop()
    music.unload()

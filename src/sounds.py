import pygame
from pygame.mixer import music

pygame.mixer.init()

def play_bg_music() -> None:
    """Play background music."""
    music.load("./assets/music/bg.mp3")
    music.play(-1)

def pause_bg_music() -> None:
    """Pause background music."""
    if music.get_busy():
        music.pause()

def stop_bg_music() -> None:
    """Stop background music."""
    music.stop()
    music.unload()

import random

import numpy as np
import pygame
from pygame.mixer import Sound, music
from scipy.signal import resample

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


def alter_pitch(sound: Sound, semitones: float) -> pygame.mixer.Sound:
    """Alter the pitch of given sound & return a new pitch."""
    array: np.ndarray = pygame.sndarray.array(sound)
    factor = 2 ** (semitones / 12)
    new_length = int(len(array) / factor)
    resampled = resample(array, new_length).astype(np.int16)
    return pygame.sndarray.make_sound(resampled)


def alter_pitch_rnd(sound: Sound) -> pygame.mixer.Sound:
    """Alter the pitch of given sound randomly & return a new pitch."""
    semitone_shift = random.uniform(5, 10)  # noqa: S311
    return alter_pitch(sound, semitone_shift)



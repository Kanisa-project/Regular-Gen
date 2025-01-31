# from wavio import write
import random

from settings import *
from scipy import signal
import numpy as np
from scipy.io.wavfile import write

samplerate = 44100
freq = 420


def get_mixed_tones(freaq):
    possible_tones = [get_sin_wave(freaq),
                      get_sweep_poly(freaq),
                      get_chirp(freaq)]
    return random.choice(possible_tones)


def generate_tone_notes(kre8dict: dict) -> dict:
    """
    Generate a dictionary of notes from a-z, 0-9
    :param kre8dict:
    :return:
    """
    base_freq = kre8dict["mujic"]["Base frequency"]
    i = 0
    tone_freq_dict = {}
    for c in ALPHANUMERIC:
        # set tone frequency for each character
        frequencee = base_freq * (i + 1)
        # tone_freq_dict[c] = get_wave(frequencee, kre8dict)
        tone_freq_dict[c] = {"Sine": get_sin_wave(frequencee),
                             "Sweep": get_sweep_poly(frequencee),
                             "Chirp": get_chirp(frequencee),
                             "Convolve": get_convolve_wave(kre8dict['number_list'])}
        # kre8dict["Mujic"]["Wave type"] = 1
        # kre8dict["Mujic"]["Wave type"] = random.randint(0, 3)
        i += 1
    # print(tone_freq_dict)
    return tone_freq_dict


def get_wave(freaq: int, wave_int=0):
    """

    """
    # t = np.linspace(2, 11, 2 * 2410)
    # wave_type = kre8dict["Mujic"]["Wave type"]
    wave = get_sin_wave(freaq)
    if wave_int == 1:
        poly_list = []
        for i in range(2):
            poly_list.append(random.random() + random.randint(-4, 4))
        wave = get_sweep_poly(freaq, poly1d_list=poly_list)
    if wave_int == 2:
        wave = get_chirp(freaq, f0=random.randint(2, 10), f1=random.randint(2, 10), t1=random.randint(2, 10))
    if wave_int == 3:
        wave = get_convolve_wave([0, 9, 3, 2, 4, 1, 4, 6, 7, 5])
    return wave


def get_convolve_wave(list_repeat=None):
    if list_repeat is None:
        list_repeat = [0, 2, 4, 6, 8, 0, 2, 4, 6, 8]
    sig = np.repeat(list_repeat, list_repeat[9] ** 3)
    print(sig)
    win = signal.windows.hann(50)
    # win = signal.windows.blackman(50)
    wave = signal.convolve(sig, win, mode='same') / sum(win)
    return wave


def get_chirp(freaq, duration=0.5, f0=4, f1=1, t1=10, method='linear'):
    """
    Function takes the "frequency" and "time_duration" for a wave
    as the input and returns a "numpy array" of values at all points
    in time.
    """
    t = np.linspace(0, 10, 2 * 3700)
    wave = signal.chirp(t, f0=f0, f1=f1, t1=t1, method=method)
    return wave


def get_sin_wave(freaq, duration=0.5, amplitude=4096):
    """
    Function takes the "frequency" and "time_duration" for a wave
    as the input and returns a "numpy array" of values at all points
    in time.
    """

    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freaq * t)
    return wave


def get_sweep_poly(freaq, duration=0.5, poly1d_list=None):
    """
    Function takes the "frequency" and "time_duration" for a wave
    as the input and returns a "numpy array" of values at all points
    in time.
    """
    if poly1d_list is None:
        poly1d_list = [-0.53, -0.96, 1.25, 8.0]
    p = np.poly1d(poly1d_list)
    t = np.linspace(0, 10, int(samplerate * duration))
    wave = signal.sweep_poly(t, p)
    return wave


def create_song_data(kre8dict: dict) -> np.ndarray:
    """
    Function to concatenate all the waves (notes)
    """
    print(kre8dict)
    music_notes = kre8dict['use_id']
    tone_freq_dict = generate_tone_notes(kre8dict)
    song = []
    new_notes = ""
    for c in music_notes:
        # new_notes += random.choice(ALPHANUMERIC_NOTE_PATTERNS[c])
        new_notes += random.choice(ALPHANUMERIC_NOTE_PATTERNS[c])
    new_notes = new_notes.replace("=", music_notes[0])
    new_notes = new_notes.replace(".", music_notes[1])
    new_notes = new_notes.replace("-", music_notes[2])
    new_notes = new_notes.replace("+", music_notes[3])
    new_notes = new_notes.replace("/", music_notes[4])
    new_notes = new_notes.replace("_", music_notes[5])
    for c in new_notes:
        song.append(tone_freq_dict[c][kre8dict["mujic"]["Wave type"]])
        # song.append(tone_freq_dict[c][random.randint(1, 3)])
    song = np.concatenate(song)
    return song

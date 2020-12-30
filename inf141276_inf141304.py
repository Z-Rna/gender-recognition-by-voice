from __future__ import division
import numpy as np
import sys
import scipy.io.wavfile
from scipy import *
import os
from scipy.signal import decimate
from scipy.signal.windows import kaiser

LIMIT_FREQ = 150
KAISER_BETA = 40
SAMPLES = range(2, 5)
START_FREQ = 60

def recognize_gender(freq):
    if freq < LIMIT_FREQ:
        return 'M'
    else:
        return 'K'

def hps(signal, w):
    # algorithm im using, Harmonic Product Spectrum: https://surveillance9.sciencesconf.org/data/151173.pdf
    n = len(signal)
    sample_rate = float(n) / w

    # kaiser window function gives the best results
    signal = signal * kaiser(n, KAISER_BETA)

    # abs of fft signal in logarithm scale
    spectrum = np.log(abs(fft.fft(signal)))

    hps_spectrum = np.copy(spectrum)

    # create couple versions of spectrum (different samples)
    for s in SAMPLES:
        # take every d_t'th item of spectrum
        decimated = decimate(spectrum, s)
        # multiply corresponding items of every decimated spectrum
        hps_spectrum[:len(decimated)] *= decimated

    start = START_FREQ * sample_rate
    peak = np.argmax(hps_spectrum[int(start):])
    freq = (start + peak) / sample_rate

    return freq

def read_signal(path):
    w, signal = scipy.io.wavfile.read(path)
    # extract one channel, if file has many
    if isinstance(signal[0], list):
        signal = [s[0] for s in signal]
    return w, signal

def main():
    path = sys.argv[1]
    w, signal = read_signal(path)
    freq = hps(signal, w)
    gender = recognize_gender(freq)
    print(gender)

if __name__ == "__main__":
   main()

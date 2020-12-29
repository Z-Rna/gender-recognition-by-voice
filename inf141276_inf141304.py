from __future__ import division
import numpy as np
import sys
import scipy.io.wavfile
from scipy import *
import os
from scipy.signal import decimate
from scipy.signal.windows import kaiser
from constants import *

def recognize_gender(freq):
    if freq < limit_frequency:
        return 'M'
    else:
        return 'K'

def hps(signal, w):
    # algorithm im using, Harmonic Product Spectrum: https://surveillance9.sciencesconf.org/data/151173.pdf
    n = len(signal)
    sample_rate = float(n) / w
    
    # kaiser window function gives best results
    signal = signal * kaiser(n, kaiser_beta)

    # abs of fft signal in logarithm scale
    spectrum = np.log(abs(fft.fft(signal)))

    hps_spectrum = np.copy(spectrum)

    # create couple versions of spectrum (different samples)
    for d_r in decimated_range:
        # take every d_t'th item of spectrum
        decimated = decimate(spectrum, d_r)
        # multiply corresponding items of every decimated spectrum
        hps_spectrum[:len(decimated)] *= decimated

    start = start_freq * sample_rate
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

import librosa
import math
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import firwin

import noisereduce as nr
# load data
data, rate = librosa.load("rain.wav")

# Step 1 Divide in windows of 1024 frames df 32
# Only first 5 seconds
seconds = 5
frame_len = 1024
delta_frame = 32

windows = []

print("Obtaining Frames")
i = 0
while i <= (rate*seconds - frame_len):
    windows.append(data[i:(i+frame_len)])
    i += delta_frame

print("Obtained Frames")

# Step 2 Hamming window to all frames
print("Applying Hamming Window")
def hamming_window(n, N):
    return 0.54 + 0.46*math.cos(2 * math.pi / N * n)

for window in windows:
    for i in range(len(window)):
        window[i] = hamming_window(window[i], frame_len)
print("Applied Hamming window")

# Step 3 FFT 4 all frames
fft_windows = list()

print("Computing FFT of each window")
for window in windows:
    fft_windows.append(fft(window))
print("Computed FFT of all windows")

# Step 4 Amplitude Spectrum of each window by frequency
# This is just obtaining the magnitude of each value in the fft array for each window
fft_A_windows = list()

print("Computing the Amplitude Spectrum")
for window in fft_windows:
    new_window = list()
    for val in window:
        new_window.append(np.absolute(val))
    fft_A_windows.append(new_window)
print("Computed the Amplitude Spectrum")

# Step 5 FIR Filter every amplitude spectrum
# Create the multipass factors for the fir filter
def H(x):
    b = 16
    c = 3
    return np.exp(- (x - b)*(x - b)/(2*c*c))


h = [H(i) for i in range(34)]
a = 0
for val in h:
    a += val

for i in range(len(h)):
    h[i] /= a

# h are the factors for the FIR filter
# TODO: No idea what N is, I need to figure this out help witu!

#fir_filter = firwin(N, h)


"""
# select section of data that is noise
noisy_part = data[10000:15000]
# perform noise reduction
reduced_noise = nr.reduce_noise(audio_clip=data[0:100000], noise_clip=noisy_part, verbose=True)
"""
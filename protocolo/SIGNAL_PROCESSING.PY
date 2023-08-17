import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft
from scipy.signal import argrelextrema
import serial
import random
from numba import jit , guvectorize

arduino_port = "COM4"
baud         = 115200

df = pd.read_csv('sujeto_3_hombre.csv', header=None)
n = 20
y = np.array(df[0][n * int(df[0].shape[0]/(12*5)):(n + 1) * int(df[0].shape[0]/(12*5))]) ## Extract two signals
print(y.shape)
x = np.linspace(0, 20, y.shape[0])
spacing = 1000




#ser = serial.Serial(arduino_port, baud)
ROLLING_WINDOW = 8200
SPACING = 1000
BATCHED_DATA = np.zeros(8200)
plt.ion()  # Turn on interactive mode
fig, ax2 = plt.subplots()
line_batched, = ax2.plot(range(ROLLING_WINDOW), BATCHED_DATA)

ax2.set_ylim(32000, 34000)


@guvectorize(['void(float64[:], intp[:], float64[:])'],
             '(n),()->(n)')
def move_mean(a, window_arr, out):
    window_width = window_arr[0]
    asum = 0.0
    count = 0
    for i in range(window_width):
        asum += a[i]
        count += 1
        out[i] = asum / count
    for i in range(window_width, len(a)):
        asum += a[i] - a[i - window_width]
        out[i] = asum / count




idx = 0
x = np.linspace(0, 8200, y.shape[0])
time = 25_000
while True:
    if idx == 8200:
        idx = 0
    
    read_value = df[0].values[time]
    BATCHED_DATA[idx] = read_value
    
    
    if idx % 100 == 80:
        line_batched.set_ydata(BATCHED_DATA)
        y_sma = np.empty_like(BATCHED_DATA)
        move_mean(BATCHED_DATA, np.array([ROLLING_WINDOW]), y_sma)
        valleys = argrelextrema(y_sma, comparator=np.less, order=50, mode='clip')[0]
        
        y_valleys = np.nan * np.ones_like(x)
        y_valleys[valleys] = y_sma[valleys]

        ax2.scatter(valleys, y_sma[valleys], color='red', marker='s')


    plt.draw()
    plt.pause(0.0001)
    idx += 1
    time = time + 1


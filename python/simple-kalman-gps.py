import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import csv
import pdb

filename_noise = 'data/unitySimulatorLog_190324123026_GPS_NOISE.txt'
filename_truth = 'data/unitySimulatorLog_190324123026_GPS_TRUTH.txt'

def read_gps_from_file(f):
    time = []
    x = []
    y = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            time.append(float(row[0]))
            x.append(float(row[2]))
            y.append(float(row[3]))
    
    return time, x, y

def plot_position(f_noise, f_truth, estimates=None):
    ax1 = plt.subplot(2, 1, 1)

    time, x_noise, y_noise = read_gps_from_file(f_noise)
    ax1.plot(time, x_noise, label='X Position (Sensor)')
    ax1.plot(time, y_noise, label='Y Position (Sensor)')

    time, x_truth, y_truth = read_gps_from_file(f_truth)
    ax1.plot(time, x_truth, label='X Position (Truth)', linestyle='--')
    ax1.plot(time, y_truth, label='Y Position (Truth)', linestyle='--')

    if estimates is not None:
        ax1.plot(time, list(map(lambda k: k[0], estimates)), label='X Position (Kalman)')
        ax1.plot(time, list(map(lambda k: k[1], estimates)), label='Y Position (Kalman)')

    ax1.set_xlabel('time (seconds)')
    ax1.set_ylabel('m')
    ax1.set_title('Position (measured by Simulation GPS)')
    ax1.legend()

    ax2 = plt.subplot(2, 1, 2)

    ax2.scatter(x_truth, y_truth, label='(X,Y) Position (Truth)', marker='.')
    ax2.scatter(x_noise, y_noise, label='(X,Y) Position (Sensor)', marker='.')
    ax2.set_xlabel('time (seconds)')
    ax2.set_ylabel('m')
    ax2.set_title('Position (measured by Simulation GPS)')
    ax2.legend()
    ax2.set_xlim(0, 17)
    ax2.set_ylim(0, 9)

    plt.subplots_adjust(hspace = 0.5)
    plt.show()

plot_position(filename_noise, filename_truth)    
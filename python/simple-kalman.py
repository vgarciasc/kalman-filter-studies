import matplotlib.pyplot as plt
import numpy as np
import csv
import pdb

filename = 'data/sensorLog_ACC_1.txt'

def read_accel_from_file(f):
    acc_x = []
    acc_y = []
    acc_z = []
    time = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            time.append(int(row[1]))
            acc_x.append(float(row[2]))
            acc_y.append(float(row[3]))
            acc_z.append(float(row[4]))
    
    return time, acc_x, acc_y, acc_z

def plot_acceleration(f):
    time, acc_x, acc_y, acc_z = read_accel_from_file(f)

    plt.plot(time, acc_x, label='X Acceleration')
    plt.plot(time, acc_y, label='Y Acceleration')
    plt.plot(time, acc_z, label='Z Acceleration')
    plt.xlabel('time')
    plt.ylabel('m/s²')
    plt.title('Acceleration measured by Sensor Fusion app')
    plt.legend()
    plt.show()

def plot_histogram(f):
    time, acc_x, acc_y, acc_z = read_accel_from_file(f)

    ax1 = plt.subplot(2, 2, 1)
    ax1.set_title('Histogram of Acceleration X measured by Sensor Fusion app')
    ax1.hist(acc_x, normed=True, bins=80, color='green', label='X Acceleration')
    ax1.set_ylabel('Probability')
    ax1.legend()
    
    ax2 = plt.subplot(2, 2, 2)
    ax2.set_title('Histogram of Acceleration Y measured by Sensor Fusion app')
    ax2.hist(acc_y, normed=True, bins=80, color='blue', label='Y Acceleration')
    ax2.set_ylabel('Probability')
    ax2.legend()

    ax3 = plt.subplot(2, 2, 3)
    ax3.set_title('Histogram of Acceleration Z measured by Sensor Fusion app')
    ax3.hist(acc_z, normed=True, bins=80, color='red', label='Z Acceleration')
    ax3.set_ylabel('Probability')
    ax3.legend()

    plt.show()

plot_acceleration(filename)
# plot_histogram(filename)
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import csv
import pdb

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

def read_imu_from_file(f):
    time = []
    v = []
    w = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            time.append(float(row[0]))
            v.append(float(row[2]))
            w.append(float(row[3]))
    
    return time, v, w

def get_pos_from_imu(time, initial_x, initial_y, initial_a, imu_v_noise, imu_w_noise):
    x = initial_x
    y = initial_y
    a = initial_a
    imu_x = [x]
    imu_y = [y]

    for i in range(1, len(time)):
        delta_t = time[i] - time[i-1]

        v = imu_v_noise[i]
        w = imu_w_noise[i]

        a = a + w * delta_t
        x = x + v * delta_t * np.cos(np.radians(-a))
        y = y + v * delta_t * np.sin(np.radians(-a))

        imu_x.append(x)
        imu_y.append(-y)
    
    return imu_x, imu_y
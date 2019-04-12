import csv
import pdb
import math
import calibration
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def read_gps_latlon_from_file(f):
    time = []
    lat = []
    lon = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[1] == 'GPS':
                time.append(float(row[0]))
                lat.append(float(row[2]))
                lon.append(float(row[3]))
    
    return time, lat, lon

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

def read_acc_from_file(f):
    time = []
    acc_x = []
    acc_y = []
    acc_z = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[1] == 'ACC':
                time.append(float(row[0]))
                acc_x.append(float(row[2]))
                acc_y.append(float(row[3]))
                acc_z.append(float(row[4]))
    
    return time, acc_x, acc_y, acc_z

def read_gyr_from_file(f):
    time = []
    gyr_x = []
    gyr_y = []
    gyr_z = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[1] == 'GYR':
                time.append(float(row[0]))
                gyr_x.append(float(row[2]))
                gyr_y.append(float(row[3]))
                gyr_z.append(float(row[4]))
    
    return time, gyr_x, gyr_y, gyr_z

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

def get_pos_from_acc_gyr(initial_x, initial_y, initial_a, time_acc, acc_x, acc_y, acc_z, time_gyr, gyr_z):
    lin_accs = []
    for i in range(0, len(time_acc)):
        vector = np.array([acc_x[i], acc_y[i], acc_z[i]])[np.newaxis].T
        bias, scale, misalignment = calibration.get_calibration_values('ACC')
        calibrated_vector = calibration.calibrate_reading(vector, bias, scale, misalignment)
        
        acc_x_temp = calibrated_vector[0][0]
        acc_y_temp = calibrated_vector[0][1]
        acc_z_temp = calibrated_vector[0][2] - 9.797899

        # temp_acc = math.sqrt(acc_x_temp**2 + acc_y_temp**2 + acc_z_temp**2)
        # lin_accs.append([time_acc[i], 'lin', temp_acc])

        lin_accs.append([time_acc[i], 'lin', [acc_x_temp, acc_y_temp, acc_z_temp]])
    
    x_pos = initial_x
    y_pos = initial_y
    imu_x = [x_pos]
    imu_y = [y_pos]
    lin_vel_x = [0]
    lin_vel_y = [0]

    linear_velocity_x = 0
    linear_velocity_y = 0

    for i in range(1, len(lin_accs)):
        delta_time = time_acc[i] - time_acc[i-1]
        acc_x = lin_accs[i][2][0]
        acc_y = lin_accs[i][2][1]

        linear_velocity_x = linear_velocity_x + acc_x * delta_time
        linear_velocity_y = linear_velocity_y + acc_y * delta_time
        
        x_pos = x_pos + linear_velocity_x * delta_time + acc_x * (delta_time ** 2) / 2
        y_pos = y_pos + linear_velocity_y * delta_time + acc_y * (delta_time ** 2) / 2

        lin_vel_x.append(linear_velocity_x)
        lin_vel_y.append(linear_velocity_y)
    
        imu_x.append(x_pos)
        imu_y.append(y_pos)

    return imu_x, imu_y, lin_vel_x, lin_vel_y
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import csv
import pdb

import reader

def plot_position(f_gps_noise, f_gps_truth, f_imu_noise, f_imu_truth, estimates=None):
    # -- Position as a Function
    ax1 = plt.subplot(2, 1, 1)

    # GPS (Noise)
    time, gps_x_noise, gps_y_noise = reader.read_gps_from_file(f_gps_noise)
    ax1.plot(time, gps_x_noise, label='X Position (GPS)', linestyle='--', color='lightblue')
    ax1.plot(time, gps_y_noise, label='Y Position (GPS)', linestyle='--', color='lightblue')

    # IMU (Noise)
    time, imu_v_noise, imu_w_noise = reader.read_imu_from_file(f_imu_noise)

    # Ground Truth
    time, gps_x_truth, gps_y_truth = reader.read_gps_from_file(f_gps_truth)
    ax1.plot(time, gps_x_truth, label='X Position (Truth)', color='green')
    ax1.plot(time, gps_y_truth, label='Y Position (Truth)', color='green')

    x = 0
    y = 0
    imu_x_noise = [x]
    imu_y_noise = [y]
    orientation = 90-57.85

    for i in range(1, len(time)):
        current_time = time[i]
        delta_t = time[i] - time[i-1]

        v = imu_v_noise[i]
        w = imu_w_noise[i]

        orientation = orientation + w * delta_t
        x = x + v * delta_t * np.cos(np.radians(-orientation))
        y = y + v * delta_t * np.sin(np.radians(-orientation))

        imu_x_noise.append(x)
        imu_y_noise.append(-y)

    ax1.plot(time, imu_x_noise, label='X Position (IMU)', linestyle='--', color='#f4b042')
    ax1.plot(time, imu_y_noise, label='Y Position (IMU)', linestyle='--', color='#f4b042')

    # IMU (Truth)
    # time, imu_v_truth, imu_w_truth = reader.read_imu_from_file(f_imu_truth)

    # Kalman Estimates
    if estimates is not None:
        ax1.plot(time, list(map(lambda k: k[0], estimates)), label='X Position (Kalman)')
        ax1.plot(time, list(map(lambda k: k[1], estimates)), label='Y Position (Kalman)')

    # Housework
    ax1.set_xlabel('time (seconds)')
    ax1.set_ylabel('m')
    ax1.set_title('Position x Time')
    ax1.legend()

    # -- Position as Scatterplot (Map)
    ax2 = plt.subplot(2, 1, 2)
    
    # GPS
    ax2.scatter(gps_x_noise, gps_y_noise, label='(X, Y) Position (GPS)', marker='.', color='lightblue')
    # IMU
    ax2.scatter(imu_x_noise, imu_y_noise, label='(X, Y) Position (IMU)', marker='.', color='#f4b042')
    # Ground Truth
    ax2.plot(gps_x_truth, gps_y_truth, label='(X, Y) Position (Truth)', color='green')
    # Housework
    ax2.set_xlabel('time (seconds)')
    ax2.set_ylabel('m')
    ax2.set_title('Trajectory')
    ax2.legend()
    # ax2.set_xlim(0, 17)
    # ax2.set_ylim(0, 9)

    # -- Finalization
    plt.subplots_adjust(hspace = 0.5)
    plt.show()

if __name__ == "__main__":
    filename_gps_noise = 'data/unitySimulatorLog_1903241400_GPS_NOISE.txt'
    filename_gps_truth = 'data/unitySimulatorLog_1903241400_GPS_TRUTH.txt'
    filename_imu_noise = 'data/unitySimulatorLog_1903241400_IMU_NOISE.txt'
    filename_imu_truth = 'data/unitySimulatorLog_1903241400_IMU_TRUTH.txt'
    
    plot_position(filename_gps_noise, filename_gps_truth, filename_imu_noise, filename_imu_truth)
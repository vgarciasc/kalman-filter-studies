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

def plot_acceleration(f, estimates=None):
    time, acc_x, acc_y, acc_z = read_accel_from_file(f)

    plt.plot(time, acc_x, label='X Acceleration')
    plt.plot(time, acc_y, label='Y Acceleration')
    plt.plot(time, acc_z, label='Z Acceleration')

    if estimates is not None:
        plt.plot(time, list(map(lambda k: k[0], estimates)), label='X Acceleration (Kalman)')
        plt.plot(time, list(map(lambda k: k[1], estimates)), label='Y Acceleration (Kalman)')
        plt.plot(time, list(map(lambda k: k[2], estimates)), label='Z Acceleration (Kalman)')

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

# plot_acceleration(filename)
# plot_histogram(filename)

should_print = False

time, acc_x, acc_y, acc_z = read_accel_from_file(filename)
current_estimate = [acc_x[0], acc_y[0], acc_z[0]] #initial values
error_in_estimate = 50000
error_in_sensor = 50000

estimates_history = [current_estimate]

for i in range(1, len(time)):
    # -- Iteration start
    previous_estimate = current_estimate
    current_estimate = None
    
    # -- Calculate Kalman Gain
    kalman_gain = (error_in_estimate) / (error_in_estimate + error_in_sensor)

    # -- Update Step
    # Update Estimate
    measurement = [acc_x[i], acc_y[i], acc_z[i]]
    current_estimate = [
        previous_estimate[0] * (1 - kalman_gain) + measurement[0] * (kalman_gain),
        previous_estimate[1] * (1 - kalman_gain) + measurement[1] * (kalman_gain),
        previous_estimate[2] * (1 - kalman_gain) + measurement[2] * (kalman_gain)
    ]

    # Update Error
    error_in_estimate = error_in_estimate * (1 - kalman_gain)

    # -- Debug
    # Print
    if should_print:
        print("time: " + str(time[i]))
        print("error_in_estimate: " + str(error_in_estimate) + ", error_in_sensor: " + str(error_in_sensor))
        print("measurement: " + str(measurement))
        print("current_estimate: " + str(current_estimate))
        print("--------------------")

    # Plot
    estimates_history.append(current_estimate)

print("final_estimate: [acc_x: " + str(current_estimate[0]) + ", acc_y: " + str(current_estimate[1]) + ", acc_z: " + str(current_estimate[2]) + "]")

plot_acceleration(filename, estimates_history)
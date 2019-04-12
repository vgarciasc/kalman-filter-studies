import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import csv
import pdb

filename = 'data/2019-04-03-imu-smartphone-rest-y-calibrated-easy.txt'

def read_accel_from_file(f):
    time = []
    acc_x = []
    acc_y = []
    acc_z = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            time.append(int(row[0]))
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
    plt.title('Acceleration (measured by Sensor Fusion app)')
    plt.legend()
    plt.show()

def plot_histogram(f):
    time, acc_x, acc_y, acc_z = read_accel_from_file(f)

    # Acceleration X
    ax1 = plt.subplot(2, 2, 1)
    ax1.hist(acc_x, density=True, bins=80, color='green', label='X Acceleration')
    
    variance_x = np.var(acc_x)
    mean_x = np.mean(acc_x)
    gaussian_x = np.linspace(mean_x - 3*np.sqrt(variance_x), mean_x + 3*np.sqrt(variance_x), 100)
    ax1.plot(gaussian_x, stats.norm.pdf(gaussian_x, mean_x, np.sqrt(variance_x)), color='magenta', linestyle='--', label='Approximated Gaussian')
    
    ax1.set_title('Histogram of Acceleration X. σ² = ' + str(variance_x))
    ax1.set_ylabel('Probability')
    ax1.legend()
    
    # Acceleration Y
    ax2 = plt.subplot(2, 2, 2)
    ax2.set_title('Histogram of Acceleration Y. σ² = ' + str(np.var(acc_y)))
    ax2.hist(acc_y, density=True, bins=80, color='blue', label='Y Acceleration')
    
    variance_y = np.var(acc_y)
    mean_y = np.mean(acc_y)
    gaussian_y = np.linspace(mean_y - 3*np.sqrt(variance_y), mean_y + 3*np.sqrt(variance_y), 100)
    ax2.plot(gaussian_y, stats.norm.pdf(gaussian_y, mean_y, np.sqrt(variance_y)), color='magenta', linestyle='--', label='Approximated Gaussian')
    
    ax2.set_ylabel('Probability')
    ax2.legend()

    # Acceleration Z
    ax3 = plt.subplot(2, 2, 3)
    ax3.set_title('Histogram of Acceleration Z. σ² = ' + str(np.var(acc_z)))
    ax3.hist(acc_z, density=True, bins=80, color='red', label='Z Acceleration')
    
    variance_z = np.var(acc_z)
    mean_z = np.mean(acc_z)
    gaussian_z = np.linspace(mean_z - 3*np.sqrt(variance_z), mean_z + 3*np.sqrt(variance_z), 100)
    ax3.plot(gaussian_z, stats.norm.pdf(gaussian_z, mean_z, np.sqrt(variance_z)), color='magenta', linestyle='--', label='Approximated Gaussian')
    
    ax3.set_ylabel('Probability')
    ax3.legend()

    print(np.sqrt(np.var(acc_y)**2 + np.var(acc_x)**2 + np.var(acc_z)**2))

    plt.show()

def kalman_filter(f):
    should_print = False
    time, acc_x, acc_y, acc_z = read_accel_from_file(f)
    current_estimate = [acc_x[0], acc_y[0], acc_z[0]] #initial values
    error_in_estimate = 5000000
    error_in_sensor = 100

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
    return estimates_history

# estimates = kalman_filter(filename)

# final_estimate = estimates[len(estimates) - 1]
# print("final_estimate: [acc_x: " + str(final_estimate[0]) + ", acc_y: " + str(final_estimate[1]) + ", acc_z: " + str(final_estimate[2]) + "]")

# plot_acceleration(filename, estimates)

# plot_acceleration(filename)
plot_histogram(filename)
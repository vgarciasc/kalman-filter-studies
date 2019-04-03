import pdb
import csv
import reader

import numpy as np

def get_error_gps(file_truth, file_gps):
    time, x_truth, y_truth = reader.read_gps_from_file(file_truth)
    time, x_noise, y_noise = reader.read_gps_from_file(file_gps)

    errors_x = []
    errors_y = []
    for i in range(0, len(time)):
        error_x = x_truth[i] - x_noise[i]
        errors_x.append(error_x)
        error_y = y_truth[i] - y_noise[i]
        errors_y.append(error_y)

    return errors_x, errors_y

def get_error_imu(file_truth, file_imu):
    time, v_truth, w_truth = reader.read_imu_from_file(file_truth)
    time, v_noise, w_noise = reader.read_imu_from_file(file_imu)

    errors_v = []
    errors_w = []
    for i in range(0, len(time)):
        error_v = v_truth[i] - v_noise[i]
        errors_v.append(error_v)
        error_w = w_truth[i] - w_noise[i]
        errors_w.append(error_w)

    return errors_v, errors_w

def get_calibration_values(sensor):
    if sensor == 'ACC':
        bias = np.array([-0.593196, 0.2645659, 0.014033])[np.newaxis].T
        scale = np.identity(3)
        misalignment = np.identity(3)
        # bias = np.array([-0.675486, 0.188289, 0.0112134])[np.newaxis].T
        # scale = np.array([
        #     [0.997423,         0,      0],
        #     [       0,  0.998976,      0],
        #     [       0,         0, 1.0002]
        # ])
        # misalignment = np.array([
        #     [1, 0.00709268,   0.013406],
        #     [0,          1, 0.00294083],
        #     [0,          0,          1]
        # ])
        # inverse_scale = np.array(1.00258, 1.00102, 0.999797)[np.newaxis].T 
    elif sensor == 'GYR':
        bias = np.array([0.020773, 0.0124993, -0.00443281])[np.newaxis].T
        scale = np.array([
            [0.97736,        0,        0],
            [      0, 0.988505,        0],
            [      0,        0, 0.997622]
        ])
        misalignment = np.array([
            [          1, -0.00741551,  0.00946448],
            [-0.00620259,           1, -0.00785747],
            [ -0.0036073,  0.00656645,           1]
        ])
        # inverse_scale = np.array(1.02316, 1.01163, 1.00238)[np.newaxis].T
    else:
        raise Exception("'" + sensor + "' is not a valid sensor name.")
    return bias, scale, misalignment

def calibrate_reading(reading, bias, scale, misalignment):
    return (np.dot(misalignment, np.dot(scale, np.subtract(reading, bias)))).T

def calibrate_file(input_file, output_file, sensor):
    bias, scale, misalignment = get_calibration_values(sensor)

    calibrated_vectors = []

    with open(input_file, 'r') as csvfile:
        readings = csv.reader(csvfile, delimiter=',')
        for reading in readings:
            vector = np.array([float(reading[2]), float(reading[3]), float(reading[4])])[np.newaxis].T
            calibrated_vector = calibrate_reading(vector, bias, scale, misalignment)
            string = ','.join([reading[0], reading[1], str(calibrated_vector[0][0]), str(calibrated_vector[0][1]), str(calibrated_vector[0][2])])
            calibrated_vectors.append(string)

    np.savetxt(output_file, calibrated_vectors, delimiter=",", fmt='%s')

filename = 'data/2019-04-03-imu-smartphone-rest-y-clean.txt'
filename_to_save = 'data/2019-04-03-imu-smartphone-rest-y-calibrated.txt'
calibrate_file(filename, filename_to_save, 'ACC')
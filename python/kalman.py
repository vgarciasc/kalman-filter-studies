import numpy as np
import pdb
import sys

import reader
import plotter
import calibration

class Measurement:
    def __init__(self, sensor, time, x, y, a, v, w):
        self.sensor = sensor
        self.time = time
        self.x = x
        self.y = y
        self.a = a
        self.v = v
        self.w = w

    def __str__(self):
        return "[" + str(self.sensor) + " (t: " + str(self.time) + ") => x: " + str(self.x) + "; y = " + str(self.y) + "; θ = " + str(self.a) + "; v = " + str(self.v) + "; ω = " + str(self.w) + "]"

def get_measurements(filename_gps, filename_imu):
    measurements_gps = reader.read_gps_from_file(filename_gps)
    measurements_imu = reader.read_imu_from_file(filename_imu)
    measurements = []

    for i in range(0, len(measurements_gps[0])):
        measurement = Measurement("GPS", measurements_gps[0][i], measurements_gps[1][i], measurements_gps[2][i], 0, 0, 0)
        measurements.append(measurement)

    for i in range(0, len(measurements_imu[0])):
        measurement = Measurement("IMU", measurements_imu[0][i], 0, 0, 0, measurements_imu[1][i], measurements_imu[2][i])
        measurements.append(measurement)

    measurements.sort(key=lambda x: x.time)
    return measurements

def kalman_filter(measurements, R_gps, R_imu, debug):
    # -- INITIALIZATION

    # Initial Parameters
    x0 = 0
    y0 = 0
    a0 = 90-57.85
    v0 = 0
    w0 = 0
    state = np.array([x0, y0, a0, v0, w0])[np.newaxis].T

    # Initial Process Matrixes
    process_covariance = np.identity(5) * 500
    Q = np.identity(5)

    # Constant Matrixes
    H_gps = np.array([
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0]
    ])
    H_imu = np.array([
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1]
    ])

    # Preparing Output
    estimation_history = [(Measurement("KALMAN", measurements[0].time, state[0], state[1], 0, 0, 0))]    

    for i in range(1, len(measurements)):
        measurement = measurements[i]
        if measurement.sensor == "IMU":
            H = H_imu
            R = R_imu
            reading = np.array([[measurement.v], [measurement.w]])
        elif measurement.sensor == "GPS":
            H = H_gps
            R = R_gps
            reading = np.array([[measurement.x], [measurement.y]])

        # -- PREDICTION
        delta_t = measurements[i].time - measurements[i-1].time
        #pdb.set_trace()

        # State Prediction
        x = state[0][0]
        y = state[1][0]
        a = state[2][0]
        v = state[3][0]
        w = state[4][0]
        #pdb.set_trace()

        state_predicted = np.array([
            x + v * delta_t * np.cos(np.radians(-a)),
            y + v * delta_t * np.sin(np.radians(-a)),
            a + w * delta_t,
            v,
            w
        ])[np.newaxis].T
        #pdb.set_trace()

        # Process Covariance Prediction
        jacobian_Fk = np.array([
            [1, 0, - (v * delta_t * np.sin(-a)), delta_t * np.cos(-a),       0],
            [0, 1,   (v * delta_t * np.sin(-a)), delta_t * np.sin(-a),       0],
            [0, 0,                            1,                    0, delta_t],
            [0, 0,                            0,                    1,       0],
            [0, 0,                            0,                    0,       1]
        ])
        #pdb.set_trace()

        process_covariance_predicted = np.add(np.dot(jacobian_Fk, np.dot(process_covariance, np.transpose(jacobian_Fk))), Q)
        #pdb.set_trace()

        # -- UPDATE

        # Calculate Kalman Gain
        numerator = np.dot(process_covariance_predicted, np.transpose(H))
        denominator = np.add(np.dot(H, np.dot(process_covariance_predicted, np.transpose(H))), R)
        kalman_gain = np.dot(numerator, np.linalg.inv(denominator))
        #pdb.set_trace()

        # Estimate New State
        innovation = np.subtract(reading, np.dot(H, state_predicted))
        state_estimated = np.add(state_predicted, np.dot(kalman_gain, innovation))
        #pdb.set_trace()

        # Update Process Covariance
        process_covariance_estimated = np.dot(np.subtract(np.identity(5), np.dot(kalman_gain, H)), process_covariance_predicted)
        #pdb.set_trace()

        # -- GETTING READY FOR NEXT ITERATION
        state = state_estimated
        process_covariance = process_covariance_estimated
        #pdb.set_trace()

        if debug:
            print("-----------------------")
            print("MEASUREMENT: " + str(measurement))
            print("PREDICTED STATE:")
            print(state_predicted)
            print("STATE:")
            print(state)
            print("PROCESS COVARIANCE:")
            print(process_covariance)
            print("KALMAN GAIN:")
            print(kalman_gain)
            input("Press Enter to continue...")

        estimation_history.append(Measurement("KALMAN", measurement.time, state[0], state[1], 0, 0, 0))
    return estimation_history

if __name__ == "__main__":
    filename_gps_noise = 'data/unitySimulatorLog_1903241400_GPS_NOISE.txt'
    filename_gps_truth = 'data/unitySimulatorLog_1903241400_GPS_TRUTH.txt'
    filename_imu_noise = 'data/unitySimulatorLog_1903241400_IMU_NOISE.txt'
    filename_imu_truth = 'data/unitySimulatorLog_1903241400_IMU_TRUTH.txt'
    measurements = get_measurements(filename_gps_noise, filename_imu_noise)

    error_gps_x, error_gps_y = calibration.get_error_gps(filename_gps_noise, filename_gps_truth)
    covar_gps_x_y = np.cov(error_gps_x, error_gps_y)

    error_imu_v, error_imu_w = calibration.get_error_imu(filename_imu_noise, filename_imu_truth)
    covar_imu_v_w = np.cov(error_imu_v, error_imu_w)

    estimates = kalman_filter(measurements, covar_gps_x_y, covar_imu_v_w, debug=("debug" in sys.argv))

    plotter.plot_position(filename_gps_truth, filename_gps_noise, filename_imu_noise, estimates)
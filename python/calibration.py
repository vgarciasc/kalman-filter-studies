import reader

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
import matplotlib.pyplot as plt
import numpy as np
import reader as reader

filename = 'data/sensorLog_20190410T145049_clean.txt'

def gps_to_xy_first(time, lats, lons):
    R = 6371000

    x = []
    y = []
    z = []

    for i in range(0, len(time) - 1):
        lat = np.radians(float(lats[i]))
        lon = np.radians(float(lons[i]))

        x.append(R * np.cos(lat) * np.cos(lon))
        y.append(R * np.cos(lat) * np.sin(lon))
        z.append(R * np.sin(lat))
    
    for i in range(1, len(time) - 1):
        x[i] = x[i] - x[0]
        y[i] = y[i] - y[0]
        z[i] = z[i] - z[0]
    
    x[0] = 0
    y[0] = 0
    z[0] = 0

    return x, y, z

def gps_to_xy_second(time, lats, lons):
    first_lat = np.float(lats[0])
    first_lon = np.float(lons[0])

    width = 100

    max_lat = first_lat + width/111111
    max_lon = first_lon + width/(111111 * np.cos(np.radians(first_lat)))

    print("first_lat: " + str(first_lat) + ", first_lon: " + str(first_lon))
    print("max_lat: " + str(max_lat) + ", max_lon: " + str(max_lon))

    x = []
    y = []

    for i in range(0, len(time) - 1):
        lat = np.float(lats[i])
        lon = np.float(lons[i])
        
        _x = ((lat - first_lat)/(max_lat - first_lat)) * width 
        _y = ((lon - first_lon)/(max_lon - first_lon)) * width
        
        # if i == 50:
            # pdb.set_trace()

        x.append(_x)
        y.append(_y)

    return x, y

# time_gps, lat, lon = reader.read_gps_latlon_from_file(filename)
# x_gps, y_gps = gps_to_xy_second(time_gps, lat, lon)

ax1 = plt.subplot(2, 2, 1)
time_acc, acc_x, acc_y, acc_z = reader.read_acc_from_file(filename)
time_gyr, gyr_x, gyr_y, gyr_z = reader.read_gyr_from_file(filename)
x_imu, y_imu, vel_x_imu, vel_y_imu = reader.get_pos_from_acc_gyr(0, 0, 0, time_acc, acc_x, acc_y, acc_z, time_gyr, gyr_z)

# plt.plot([0, 60], [0, -80])

ax1.plot(time_acc, vel_x_imu, label='Velocity X (IMU)')
ax1.plot(time_acc, vel_y_imu, label='Velocity Y (IMU)')
ax1.legend()

ax2 = plt.subplot(2, 2, 2)

ax2.set_xlim(-0.6, 0.6)
ax2.set_ylim(-0.6, 0.6)
ax2.scatter(x_imu, y_imu, label='(X, Y) Position (IMU)', marker='.', color='#f4b042')
# plt.scatter(x_gps, y_gps, label='(X, Y) Position (GPS)', marker='.', color='#b0f442')
ax2.legend()

ax3 = plt.subplot(2, 2, 3)

ax3.plot(time_acc, x_imu, label='Position X (IMU)')
ax3.plot(time_acc, y_imu, label='Position Y (IMU)')
ax3.legend()

ax4 = plt.subplot(2, 2, 4)

ax4.plot(time_acc, acc_x, label='Acceleration X (IMU)')
ax4.plot(time_acc, acc_y, label='Acceleration Y (IMU)')
ax4.plot(time_acc, acc_z, label='Acceleration Z (IMU)')
ax4.legend()

plt.show()
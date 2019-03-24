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
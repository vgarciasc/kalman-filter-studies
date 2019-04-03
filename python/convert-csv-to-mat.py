import numpy as np
import csv
import pdb

from decimal import Decimal

filename = 'data/sensorLog_20190403T173741_clean.txt'

def write_to_file(array, f):
    string = ''
    for i in array:
        if np.sqrt(float(i[2])**2 + float(i[3])**2 + float(i[4])**2) < 11:
            string += '   '
            string += str('%.7e' % Decimal(i[0]))
            string += '   '
            string += str('%.7e' % Decimal(float(i[2])))
            string += '   '
            string += str('%.7e' % Decimal(float(i[3])))
            string += '   '
            string += str('%.7e' % Decimal(float(i[4])))
            if array.index(i) < len(array) - 1:
                string += '\n'

    with open(f, 'w') as file:
        file.write(string)

def read_from_file(f):
    acc = []
    gyr = []

    with open(f, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[1] == 'ACC':
                acc.append(row)
            elif row[1] == 'GYR':
                gyr.append(row)

    return acc, gyr

acc, gyr = read_from_file(filename)
write_to_file(acc, 'acc.mat')
# write_to_file(gyr, 'gyr.mat')
import pathlib
import matplotlib.pyplot as plt
import numpy as np

others_data_dict = dict([(i, []) for i in [1, 2, 3, 4]])


def messages_of_node(file):
    f = open(file)
    return int(f.readlines()[-1].split()[-1])


def add_new_data(logs_directory):
    total_messages = 0
    for file in pathlib.Path(logs_directory).glob('*.stdout'):
        total_messages += messages_of_node(file)
    return total_messages


output_dir = "output/"
temp = []
for directory in pathlib.Path(output_dir).glob('*'):
    temp.append(add_new_data(str(directory) + '/logs'))
    # print(f"Directory {directory} has message complexity: {add_new_data(str(directory) + '/logs')}")
print(np.average(temp))

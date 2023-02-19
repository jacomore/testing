from multiprocessing import Process, Pipe
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt 
from sender import *


def init():
    sns.heatmap(np.zeros(DIMENSION), vmax=MAX_VAL, cbar=False)


def receiver(connection):
    """receive data from "sender.py" module. The program stops when data is received

    Args:
        connection (Connection object): is the edge of the Pipe established between plotter and sender

    Yields:
        y_data, x_data: generator that contains the appended values received from sender
    """
    print('Receiver: Running')
    while True:
        in_channel = connection.recv()
        if in_channel is None:
            ani.pause()
            print("Send is done: pausing animation.")
            break
        else:
            yval = in_channel[0]
            xval = in_channel[1]
            ydata.append(yval)       
            xdata.append(xval)
            yield ydata,xdata



if __name__ == '__main__':
    DIMENSION = (10,10)
    MAX_VAL = 1
    data = np.emtpy(DIMENSION)


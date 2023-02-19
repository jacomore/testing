from multiprocessing import Process, Pipe
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt 
from sender import *

def init():
    """ Initialise the Axes of animated image by setting the limits
    
    Returns:
        ln, : Line2D object that represents plotted data
    """
    ax.set_xlim(X_MIN,X_MAX)
    ax.set_ylim(Y_MIN,Y_MAX)
    return ln,


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

def update(data):
    """Update frame for plotting

    Args:
        ydata (generator): values to be plotted on the y axis
        xdata (generator): values to be plotted on the x axis

    Returns:
        ln : line2D object
    """
    ydata.append(data[0][0])
    xdata.append(data[1][0])
    ln.set_data(xdata,ydata)
    return ln,
    
if __name__ == '__main__':
    # Returns a pair of Connection objects, representing the ENDS of the pipe.
    # duplex : Boolean; if False the pipe is unidirectional (conn1 <--- conn2)
    conn1, conn2 = Pipe(duplex = False)
    # PROCESS 
    # target: is the callable object to be invoked by run() method
    # name: str that serves as an identifier
    # args: argument tuple to be passed to target process
    sender_process = Process(target=sender, name = "Sender", args=(conn2,))
    # Process.start starts the process activity
    sender_process.start()
    # start the receiver
    receiver_process = Process(target=receiver, name = "Receiver", args=(conn1,))
    receiver_process.start()
    # Process.join blocks the program until the process to which is called finishes. 
    # Timeout argument [s] can be passed; if the method times out a None is returned. 
    # Exitcode is always returned and must be checked.   
    sender_process.join(timeout=10)
    receiver_process.join(timeout=10)
    
    ## setup up th animation with matplotlib.animation class. 
    # returns Figure and Axes objects
    # Figure: top level container for all the plot elements.
    # Axes: contains most of the (sub-)plot elements: Axis, Tick, Line2D, Text, Polygon, etc., and sets the coordinate system.
    # Like all visible elements in a figure, Axes is an Artist subclass.
    fig, ax = plt.subplots()
    X_MIN = 0
    X_MAX = 2
    Y_MIN = 0
    Y_MAX = 1
    xdata, ydata = [],[]
    ln, = ax.plot([], [], 'ro')
    ani = FuncAnimation(fig, update, frames = receiver(conn1),init_func=init, interval = 10, blit=True,cache_frame_data = False)
    plt.show()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process, Pipe
from sender_2D import sender

def update_indeces(row, col):
    """Given the input index, returns the column index increase by an integer and, if the row if finished
       the row index is increased as well by 1.

    Arguments
    -------
        row, col (int): indeces obtained by counting the input data packets    
    
    Returns:
    -------
        row, col (int): indeces obtained by counting the input data packets  
    """
    # index --> col_index + 1
    col = col + 1
    if (col%DIMX == 0): # if row is finished, increase row index
        row += 1
    return row, col

def figure_index(row,col):
    """Given the updatead indeces, returns the actual column index for plotting the figure
    Arguments
    -------
        row, col (int): indeces to associate the input pixel with the position on the image    
    
    Returns:
    -------
        column index for plotting    
    """
    if (row%2 == 0): # even row
        return col%DIMY
    else:                  # odd row
        return DIMX-1-col%DIMX

def init():
    """Initialise the AxesImage object (image attached to an axis). 
    
    Returns:
        im, : AxesImage object that represents the image    
    """
    im.set(animated = True, clim = (0,AMPLITUDE),cmap = 'magma',interpolation = None,)
    return im,


def receiver(connection):
    """receive data from "sender.py" module. The program stops when data is received

    Args:
        connection (Connection object): is the edge of the Pipe established between plotter and sender

    Yields:
        y_data, x_data: generator that contains the appended values received from sender
    """
    print('Receiver: Running')
    row_index = 0
    col_index = 0
    while True:
        in_channel = connection.recv()
        if in_channel is None:
            ani.pause()
            print("Send is done: pausing animation.")
            break
        else:
            # evaluate the column index for the figure to be plotted
            fig_col_index = figure_index(row_index,col_index)
            # upload in_channel on data
            data[row_index,fig_col_index] = in_channel
            # evaluate new indeces
            row_index, col_index = update_indeces(row_index,col_index)
            yield data

def updatefig(data):
    im.set_data(data)
    return im,

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
    X_MIN , X_MAX = 0 , 9
    Y_MIN, Y_MAX = 0 , 9
    STEPX , STEPY = 1, 1
    DIMX, DIMY = 10 , 10 
    AMPLITUDE = 1
    data = np.empty((DIMX,DIMY))
    im = plt.imshow(data)
    
    ani = animation.FuncAnimation(fig, updatefig, frames = receiver(conn1),init_func=init, interval = 30, blit=True,cache_frame_data = False)
    plt.show()
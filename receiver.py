from multiprocessing import Process, Pipe
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt 
import numpy as np
from sender import sender

def init():
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    return ln,

def update(frame,item):
    xdata.append(frame)
    ydata.append(item)
    ln.set_ydata(xdata,ydata)
    return ln, 

# consume work
def receiver(connection):
    print('Receiver: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        item = connection.recv()
        # report
        print(f'>receiver got {item}', flush=True)
        # check for stop
        if item is None:
            break
        else:
            ani = FuncAnimation(fig, update, frames = np.linspace(0,1,100),
                    fargs = (item,), init_func=init, blit=True)
            plt.show()

    # all done
    print('Receiver: Done', flush=True)
    return 
 
# entry point
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
    
    ## setup up th animation with matplotlib.animation class. 
    # returns Figure and Axes objects
    # Figure: top level container for all the plot elements.
    # Axes: contains most of the (sub-)plot elements: Axis, Tick, Line2D, Text, Polygon, etc., and sets the coordinate system.
    # Like all visible elements in a figure, Axes is an Artist subclass.
    fig, ax = plt.subplots()
    xdata, ydata = [],[]
    # axes.plot returns a line2D object representing the plotted data. 
    # evidently, line2D object is a subclass of artist.
    ln, = ax.plot([], [], 'ro')

    
    
    # Process.join blocks the program until the process to which is called finishes. 
    # Timeout argument [s] can be passed; if the method times out a None is returned. 
    # Exitcode is always returned and must be checked.   
    sender_process.join()
    receiver_process.join()
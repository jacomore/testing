from numpy import random
import numpy as np
from time import sleep

# generate work
def sender(connection):
    print('Sender: Running', flush=True)
    # generate work
    for i in range(100):
        # generate a value
        value = random.rand(1)
        # block
        sleep(0.05)
        # send data
        pos = i*0.01
        connection.send([np.sin(pos),pos])
    # all done
    connection.send(None)
    print('Sender: Done', flush=True)
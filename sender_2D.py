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
        sleep(0.1)
        # send data
        connection.send(value)
    # all done
    connection.send(None)
    print('Sender: Done', flush=True)
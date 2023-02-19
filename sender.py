from numpy import random
from time import sleep

# generate work
def sender(connection):
    print('Sender: Running', flush=True)
    # generate work
    for i in range(100):
        # generate a value
        value = random()
        # block
        sleep(0.3)
        # send data
        connection.send(value)
    # all done
    connection.send(None)
    print('Sender: Done', flush=True)
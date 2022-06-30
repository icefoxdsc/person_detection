
from pynput import *
from person_detection import instanceListener

if __name__ == '__main__':
    instance_listener = instanceListener()
    instance_listener.run_pd()



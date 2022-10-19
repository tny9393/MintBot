# listen to contract creation -> get address
# listen to event log from this contract -> get time openning of wl

import config
from BClistener import *


def run():
    run_event_listener()

if __name__ == '__main__':
    run()
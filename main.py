#!/usr/bin/env python

"""
main.py
"""
from Queue import Queue
# import signal

from event_logger import EventLogger
from event_receiver_thread import EventReceiverThread
from command_thread import CommandThread
from command_tester import CommandTester


# def signal_handler(signal, frame):
#     print('You pressed Ctrl+Z!')


if __name__ == '__main__':
    # signal.signal(signal.SIGTSTP, signal_handler)

    outbound_queue = Queue()
    inbound_queue = Queue()
    command_thread = CommandThread(outbound_queue)
    command_thread.start()

    event_receiver_thread = EventReceiverThread(inbound_queue)
    event_receiver_thread.start()

    event_logger_thread = EventLogger(inbound_queue)
    event_logger_thread.start()

    command_tester = CommandTester(outbound_queue)
    command_tester.start()

    command_thread.join()
    event_receiver_thread.close()
    event_receiver_thread.join()
    event_logger_thread.join()
    command_tester.join()
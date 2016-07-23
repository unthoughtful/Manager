'''
Created on 23 Jul 2016

@author: professor
'''

from threading import Thread
import time


class Sched():
    """Schedule a given function to run with or without arguments at intervals.
    This basically emulates a timer task; run specific function at certain times.
    """
    def __init__(self, func, args=None):
        self.func = func
        self.args = args
        self.cancelled = False


    def schedule(self, sleep_time, delay):
        """Run the program in its own thread.

        Args:
            sleep_time: milliseconds to sleep after each function call.
            delay: milliseconds to wait before first execution.

        """
        self.sleep_time = sleep_time
        self.delay = delay
        self.thread = Thread(target=self.run)
        self.thread.start()


    def run(self):
        """Run the program.

        Args:
            sleep_time: milliseconds to sleep after each function call.
            delay: milliseconds to wait before first execution.

        """

        if self.cancelled:
            return
        time.sleep(self.delay / 1000.00)  # Wait for the delay
        if self.args is None:
            self.run_no_args()
        else:
            self.run_with_args()


    def run_no_args(self):
        """Execute the function with no arguments.
        """
        while True:
            if self.cancelled:
                return
            self.func()
            time.sleep(self.sleep_time / 1000.00)


    def run_with_args(self):
        """Execute the function with arguments supplied earlier.
        """
        while True:
            if self.cancelled:
                return
            self.func(self.args)
            time.sleep(self.sleep_time / 1000.00)


    def cancel(self):
        """Set the 'cancelled' flag so the thread exits.
        """
        self.cancelled = True


    def set_sleep_time(self, time):
        """Change the Node's sleep time between function calls.

        Args:
            time: amount of time in milliseconds to sleep

        """
        self.sleep_time = time


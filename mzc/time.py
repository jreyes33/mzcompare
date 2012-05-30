from datetime import datetime


class Timer(object):
    """Class used to time the execution of the app."""

    def __init__(self):
        self.t1 = datetime.today()

    def mark(self):
        self.t2 = datetime.today()

    def get_exec_time(self):
        return self.t2 - self.t1

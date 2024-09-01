import datetime


class TimeSpanTracker:

  def __init__(self):
    self.Expires = datetime.datetime.now()

  def StartTimer(self, secs:int):
    self.Expires = datetime.datetime.now() + datetime.timedelta(seconds=secs)

  def IsActive(self):
    return datetime.datetime.now() < self.Expires
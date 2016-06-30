import csv
import copy
import thread

def writedata(filename, buf, lock):
  lock.acquire()
  with open(filename, "a") as csvfile:
    for line in buf:
      csvfile.write(line+"\n")
  lock.release()
  return

def writedatal(filename, buf):
  """Writes the data in a locking way."""
  with open(filename, "a") as csvfile:
    for line in buf:
      csvfile.write(line+"\n")
    csvfile.close()
  return

class DataWriter(object):
  """docstring for DataWriter"""
  def __init__(self, *args, **kwargs):
    super(DataWriter, self).__init__()
    self.filename = kwargs.pop("filename","data.csv")
    self.datathreshold = kwargs.pop("datathreshold", 10)
    self.data = []
    self.lock = thread.allocate_lock()

  def append(self, data):
    """Get the data from the main program. Data should be provide in the form of
    a string, it will be added as is to the csv file."""
    if data is not None:
      self.data.append(data)
      self.checkdata()

  def checkdata(self):
    """Check the size of data array. If it is bigger than a certain threshold
    save the data to file (possibly asynchronously) and empty the array."""
    if len(self.data) >= self.datathreshold and not self.lock.locked():
      buf = copy.deepcopy(self.data)
      self.data = []
      thread.start_new_thread(writedata,(self.filename,buf,self.lock))

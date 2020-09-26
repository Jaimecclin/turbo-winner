# from multiprocessing import Manager, Lock
import threading
import queue
import time

class TaskManager:
  ''' This class is to manager all tasks in system. '''
  def __init__(self):
    self.shutdown = threading.Event()
    self.queue = queue.Queue()
    self.tasks = []

  def start(self):
    t = threading.Thread(target = self.mainThread, name='MAIN')
    t.start()
    return True
  
  def addTask(self, task):
    self.queue.put(task)

  @property
  def runningTaskCount(self):
    return len([t for t in self.tasks if t.isRunning])

  def mainThread(self):
    try:
      while not self.shutdown.is_set():
        task = self.queue.get()
        task.execute()
        self.tasks.append(task)
        time.sleep(1)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
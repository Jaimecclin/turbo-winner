import threading
import numpy as np
from multiprocessing import Process
from tpot import TPOTRegressor

class Task:
  def __init__(self, type):
    self.type = type
    self.p = None

  @property
  def taskType(self):
    return self.type
  
  @property
  def isRunning(self):
    ''' Return whether task is running or not. '''
    return self.p.is_alive()
  
  def execute(self):
    ''' 
    Create a thread to monitor task. 
    You can do more here, such as terminating task or tracing task status.
    '''
    monitorThreading = threading.Thread(target = self.exe)
    monitorThreading.start()  
  
  def exe(self):
    # Initialize a subprocess
    self.p = Process(target=self.__trainTask)
    # Start it.
    self.p.start()

  def __trainTask(self):
    ''' You can define your task here. '''
    x = np.random.rand(50,2)
    y = np.random.randint(2, size=50)
    regressor = TPOTRegressor(generations=10, population_size=20, verbosity=2, scoring="neg_mean_squared_error", random_state = 42)
    regressor.fit(x, y)
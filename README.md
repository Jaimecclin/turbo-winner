# Use flask to build a website platform to run Machine Learning tasks parallelly

## Introduction 

This is an example presenting how to build a multiprocessing program in Python flask server. It would have a http interface to accept tasks and a routine to handle machine learning tasks.

To understand more, please see [github repostitory](https://github.com/Jaimecclin/turbo-winner).

I'd explain a bit how to build this simple platform and where you can extend in the following part. Only backend code here. 

## Prerequisite

Python version: 3.6.8
Machine learning related package:
1. [scikit-learn](https://scikit-learn.org/stable/install.html)
2. [TPOT](http://epistasislab.github.io/tpot/installing/)

You'd better know what [Python flask](https://flask.palletsprojects.com/en/1.1.x/) is and how to use it. I will regard every tas)k as a training task so I pick up these two packages in this platform.

## Implementation

### flask server

Use threading module to create to routine.

1. Task manager: to handle all tasks in system
2. Flask server: a http service to accept tasks.

```python
app = Flask(__name__)
tm = TaskManager()

if __name__ == "__main__":
  # Main threading to handle tasks.
  tm.start()
  # Create a threading to run flask servers.
  serverTheading = threading.Thread(target = app.run,
                                    daemon=True,
                                    name='FLASK_SERVER',
                                    kwargs=({'host':'0.0.0.0', 
                                              'port':5000,
                                              'debug':False}))
  serverTheading.start()
```


Flask interface: users can call these APIs to execute tasks or check task state.

```python
@app.route("/AddTask")
def addTask():
  # Create a task
  task = Task("Train")
  # Insert it into task manager
  tm.addTask(task)
  return "Success"

@app.route("/RunningTaskCount")
def RunningTaskCount():
  return "We have {} running tasks.".format(tm.runningTaskCount)
```

### Task Manager

I use python __queue__ as a container to store tasks because it's a thread-safe object. In this way, a threading lock is not needed. The mainThead function is responsible for executing each task. If there is no task in the queue, it would stop as the queue is __blocking__.

```python
class TaskManager:
  ''' This class is to manager all tasks in system. '''
  def __init__(self):
    self.shutdown = threading.Event()
    self.queue = queue.Queue()
    self.tasks = []

  def start(self):
    ''' Start main thread '''
    t = threading.Thread(target = self.mainThread, name='MAIN')
    t.start()
    return True
  
  def addTask(self, task):
    self.queue.put(task)

  @property
  def runningTaskCount(self):
    ''' Return the count of running tasks '''
    return len([t for t in self.tasks if t.isRunning])

  def mainThread(self):
    ''' Run each task in system. '''
    try:
      while not self.shutdown.is_set():
        task = self.queue.get()
        task.execute()
        self.tasks.append(task)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
```
### Task

We all know that __multithreading__ cannot bring us real speed-up effect on our program as [__Global Interpreter Lock__](https://en.wikipedia.org/wiki/Global_interpreter_lock). In order to execute many tasks parallelly, I adopt Python multiprocessing module to run tasks. And I also create another thread here to monitor the process state. If you have special requirements, f.g. scanning the output of the running task, you could extend this thread to get what you need.

Regarding the __trainTask function is exactly our real task. Of course, you could define it by yourself, such as scikit-learn SVN. TPOT package is a great tool to help you find the best Machine Learning model without too much effort. I take TPOT regressor as an example here because I'd like a task taking a long time to show the result.

```python
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
    while self.p.is_alive():
      '''
      Do something, like monitor the process output. 
      '''
      time.sleep(0.1)

  def __trainTask(self):
    ''' You can define your task here. '''
    x = np.random.rand(50,2)
    y = np.random.randint(2, size=50)
    regressor = TPOTRegressor(generations=10, population_size=20, verbosity=2, scoring="neg_mean_squared_error", random_state = 42)
    regressor.fit(x, y)
```

## Test it!

1. Please run this program.
```
$ python main.py
```
- See this picture means the service is on.

![](https://i.imgur.com/dFqVK65.png)


2. Use your browser to check tasks status. 

- URL:

```
http://localhost:5000/RunningTaskCount
```

Result:
- Now no running task.

![](https://i.imgur.com/Op3xqza.png)

2. Use your browser to add a task. 

- URL:

```
http://localhost:5000/AddTask
```

Result:

- Success to add a task.

![](https://i.imgur.com/pgGnoLS.png)

- The system starts to execute this training task and best model is from AdaBoost.

![](https://i.imgur.com/6PerH3h.png)

- Check the task state again via url.

Result:

![](https://i.imgur.com/SO12Op2.png)

## Summary

This article shows we can utilize some modules to build a Machine Learning platform. Indeed, this is a quite simple program but you could modify it to fit your requirements, such as replacing Django to flask, adding Tensor flow package into the system to do Deep Learning, or changing threading to coroutine. You could try everything you want! Happy hacking!

## Reference
1. https://docs.python.org/3/library/multiprocessing.html
2. https://flask.palletsprojects.com/en/1.1.x/

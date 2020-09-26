from flask import Flask
from task_manager import TaskManager
from task import Task
import threading

app = Flask(__name__)
tm = TaskManager()

''' flask interface '''
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
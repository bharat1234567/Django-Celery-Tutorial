from celery import Celery
import time

app = Celery('tasks',broker='amqp://localhost/')

@app.task
def runme(i):
    time.sleep(1)
    print(i)

# as we can see we can create any python file,  import celery and create its instance using above command

# app = Celery('tasks',broker='amqp://localhost/')

#once done we can use that instance name to create tasks  @app.task

# what is a task?
# its nothing but a function that will be taken by celery workers to execute asnychronously!

# When you send a task message in Celery, that message won’t contain any source code, but only the name of the task you want to execute. This works similarly to how host names work
# on the internet: every worker maintains a mapping of task names to their actual functions, called the task registry.
# Whenever you define a task, that task will also be added to the local registry


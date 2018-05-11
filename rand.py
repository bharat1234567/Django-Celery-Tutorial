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
# will go into details latr!

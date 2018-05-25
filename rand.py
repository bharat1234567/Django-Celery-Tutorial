from celery import Celery
import time

app = Celery('tasks',broker='amqp://localhost/', backend='redis://localhost') #'redis://localhost:6379/0'
app.conf.task_routes = {'task_1': {'queue': 'first_task_queue'}, 'task_2': {'queue': 'second_task_queue'}}
# app.conf.task_routes = {'task_2': {'queue': 'second_task_queue'}}

@app.task
def runme(i):
    time.sleep(1)
    print(i)

# as we can see we can create any python file,  import celery and create its instance using above command

# app = Celery('tasks',broker='amqp://localhost/')

# once done we can use that instance name to create tasks  @app.task

# what is a task?
# its nothing but a function that will be taken by celery workers to execute asnychronously!

# When you send a task message in Celery, that message won’t contain any source code, but only the name of the task
# you want to execute. This works similarly to how host names work
# on the internet: every worker maintains a mapping of task names to their actual functions, called the task registry.
# Whenever you define a task, that task will also be added to the local registry


@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
    print(self.request)


@app.task(name='task_1')
def task_1(i):
    print(str(i) + " task 1 is getting executed")


@app.task(name='task_2')
def task_2(i):
    print(str(i) + " task 2 is getting executed")
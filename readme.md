# Django Celery Tutorial

<h4>Commands to Install broker:</h4>

```
$ sudo apt-get install rabbitmq-server
$ sudo service rabbitmq-server restart
$ sudo rabbitmqctl status
```

Now create a python file with any name say xyz.py ( filename to be used for celery
and keep this code in there.

```
from celery import Celery
import time

app = Celery('tasks',broker='amqp://localhost/')

@app.task
def mytask(params):
    your code goes here...
```

Command to start celery workers:

```
celery -A  xyz worker --loglevel=INFO  #...can add other parameters like concurrency and all! will see later on
```

- As clear from code we are referencing xyz.py file while creating worker. In xyz.py is where celery app is created.

- This command by default create as many celery parallel processes as there are number of cores in the cpu. 

 Exmaple: If quadcore then if you check with ps after above command
 
 ```
 $ ps celery
 ```
then you can see that 4 processes are created.

**Celery is thread safe**. In one project, we can create different celery instances that maps to different set of configurations and tasks.

```
from celery import Celery
app = Celery()
app
```
Output:
```
<Celery __main__ at 0x7f8c0999d128>  # this is textual representation of app classname = Celery current main module __main__ + memory address of object
```

After this, if i go ahead and create another instance 

```
app2 = Celery()
app2
```
Output:
```
<Celery __main__ at 0x7f8c03097e10>
```

- **<Classname__modulename___at memory address of obj>** this is the structure of any celery app.

- app and app2 are 2 seperate instances of celery that are defined one after another. they can be mapped to different set of tasks to keep work seperate.

Till now we have created instance of celery object. Next is setting its configuration which can be found [here](http://docs.celeryproject.org/en/latest/userguide/configuration.html).

Generally for any configuration we set it by setting 
```
app.some_property_name = value
```
other options are like loading these from a class or environment variables.

#How to create a task?

On top of any function add the decorator **@app.task**

```
from celery import Celery
app = Celery()

@app.task
def add(a,b):
    return a + b
    
@app.task
def sub(a,b):
    return a + b
```
- One thing to notice here, if we try printing the object app, add and sub, all of these will
point to same memory value.

```
app
```
Output:
```
<Celery __main__ at 0x7f0df3396668> 
```

```
add
```
Output:
```
<@task: __main__.add of __main__ at 0x7f0df3396668>
```

```
sub
```
Output:
```
<@task: __main__.sub of __main__ at 0x7f0df3396668>
```

<h2>Name of a task: </h2>

```
add.name
```
Output:
```
__main__.add
```

- when we create a task what happens is it creates a mapping of task name to function name , this is maintained in task registery.
- Whenever you define a task, that task will also be added to the local registry
- whenever Celery isn’t able to detect what module the function belongs to, it uses the main module name to generate the beginning of the task name.

- whenever we import any task from anyother file then the module name will no longer remain main

```
from rand import runme
runme.name
```
Output:
```
rand.runme
```

If we want that instead of main anyother module should be used then 

```
crap = Celery('dome')  # here dome is the module name that we have given in input and is being used by celery
@crap.task
def sade():
    return 2
sade.name
```
Output:
```
dome.sade
```

<h5>Basically tasks generate their names automatically with module_name.task_name, however we can give our specific names to tasks as well. 

```
 @app.task(name='sum-of-two-numbers')
 def add(x, y):
    return x + y
 add.name
```
Output:
```
sum-of-two-numbers
```

<h6> sum of 2 numbers can also be present in other module which can lead to collision. 
as a best practice always append modulename-taskname even while giving your own custom names to avoid collision.

#Configuring celery app

- we can directly configure like this 
```
app.conf.enable_utc = True # configuration to use UTC Time
```

Or 

- use update method to set multiple keys at once

```
app.conf.update(
        enable_utc=True,
        timezone='Europe/London')
```

Or 

- create a python file that has all properties in variables. pass that object to 
**app.config_from_object()** method to load configurations.

```
#celeryConfig.py

enable_utc = True
timezone = 'Europe/London'
.
.
. # keep all setting in this python file
```

```
from celery import Celery

app = Celery()
app.config_from_object('celeryconfig') #why we have used celeryconfig as a string here?
```

- celeryconfig can be imported seperately and that will also work but its not RECOMMENDED.
- Using the name of a module is recommended as this means the module does not need to be serialized when the prefork pool is used.
If you’re experiencing configuration problems or pickle errors then please try using the name of a module instead.

Or

We can also create a class and use it as object

```
from celery import Celery

app = Celery()

class Config:
    enable_utc = True
    timezone = 'Europe/London'

app.config_from_object(Config)
```

Or 

We can set configuration from environment variables

```
import os
from celery import Celery

os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')
```
- In this case we can maintain different configurations like celeryconfig.prod, celeryconfig.staging etc and set them as environment variable. Out code will start
picking that configuration without even doing any restart.


#Hiding sensitive celery configurations

Celery can't hide all sensitive info. it will only hide if  if the name contains any of these sub-strings:

API, TOKEN, KEY, SECRET, PASS, SIGNATURE, DATABASE


Say I am in a situation where i want to print all the configuration information for some debugging purpose

````
app.conf.humanize(with_defaults=True, censored=False)  --> here true means we want to see them , false means we want to hide them

app.conf.table(with_defaults=False, censored=True) # returns dictionary , above one returns string!
````


#What happens when celery instance is created?
- a logical clock instance is created, used for events.
- Create the task registry.  (creates a place to store mapping of task name and function corresponding to them)
- Set itself as the current app (**but not if the set_as_current argument was disabled**)

````
app.set_as_current
True    ---> this is true by default
````

- Call the app.on_init() callback (does nothing by default).

# What happens when we write @app.task ?

- app.task() decorators don’t create the tasks at the point when the task is defined, instead it’ll defer the creation of the task to happen either when the task is used, or after
the application has been finalized.
- Finalization of the app happens either explicitly by calling app.finalize() – or implicitly by accessing the app.tasks attribute.

#Difference between task and shared task?

- @task(shared=True)  If we turn this shared to false then task will be private to the app
- The task decorator **@task** will share tasks between apps by default 

````
app1 = Celery()

@app1.task
def test():
    pass

app2 = Celery() # Another celery instance

#the test task will be registered in both apps:

assert app1.tasks[test.name]
assert app2.tasks[test.name]

````

- Note: test will be configured using app1's configuration not app2 and it will always use app1's configuration.

However if we are using @shared_task decorator, the **@shared_task** decorator returns a proxy that always uses the task instance
in the current_app.

````
app1 = Celery()

    @shared_task
    def test():
        pass
    assert test.app is app1


    app2 = Celery()
    assert test.app is app2
````

- This makes the @shared_task decorator useful for libraries and reusable apps,
since they will not have access to the app of the user.

# What does finalizing the app will do?

- Copy tasks that must be shared between apps
- Tasks are shared by default, but if the shared argument to the task decorator is disabled, then the task will be private to the app it’s bound to.

````
@app.task(shared=false)
def add(a,b):
    return a + b
````

- Evaluate all pending task decorators.
- Make sure all tasks are bound to the current app.

#Tasks 

- @app.task(serializer='json') to make tasks input serializable
- Task.max_retries: 
Only applies if the task calls self.retry or if the task is decorated with the autoretry_for argument.

- If the number of retries exceeds this value a

- MaxRetriesExceededError exception will be raised.
You have to call retry() manually, as it won’t automatically retry on exception.

- Throwing Error:

````
@task(throws=(KeyError, HttpNotFound)):
def get_foo():
    something()
````
- now here HttpNotFound is an expected error: so it will be logged with severity = INFO, traceback included.
It won't be logged as error

- **[Task.default_retry_delay]** Default time in seconds before a retry of the task should be executed. Can be either int or float. **Default is a three minute delay**.

- **[Task.rate_limit]** the rate limit for this task type (limits the number of tasks that can be run in a given time frame). Tasks will still
complete when a rate limit is in effect, but it may take some time before it’s allowed to start.
- If this is None no rate limit is in effect. If it is an integer or float, it is interpreted as “tasks per second”.

- rate limits can be specified in seconds, minutes or hours by appending “/s”, “/m” or “/h” to the value. Tasks will be evenly distributed over the specified time frame.
 
 - Example: “100/m” (hundred tasks a minute) i.e. 100 tasks in 60 seconds by a single worker. This will enforce a minimum delay of 600ms between starting two tasks on the same worker instance.
 
- enforce a global rate limit

- suppose celery workers are calling an api for which we have like 5 requests per second max limit
and we have created a worker --> 4 processes for each core
now they should know that 5 req are sent already and till 1 sec completes we can't request more!
so we need to set this at queue level.
 
- Task.time_limit
The hard time limit, in seconds, for this task. When not set the workers default is used.

- Task.soft_time_limit
The soft time limit for this task. When not set the workers default is used.

- Task.ignore_result
Don’t store task state. Note that this means you can’t use AsyncResult to check if the task is ready, or get its return value.

- Task.store_errors_even_if_ignored
If True, errors will be stored even if the task is configured to ignore results.

- Task.serializer
A string identifying the default serialization method to use. Defaults to the task_serializer setting. Can be pickle, json,
 yaml, or any custom serialization methods that have been registered with kombu.serialization.registry.
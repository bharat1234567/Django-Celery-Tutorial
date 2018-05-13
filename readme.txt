This is django + celery tutorials. 

Commands to Install broker:

------------------------------------------------------------------------------------


sudo apt-get install rabbitmq-server
sudo service rabbitmq-server restart -- we need to restart it!
sudo rabbitmqctl status  -- to check if server is started or not

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Now create a python file with any name say xyz.py ( filename to be used for celery

and keep this code in there:

---------------
from celery import Celery
import time

app = Celery('tasks',broker='amqp://localhost/')

@app.task
def mytask(params):
    <mycode>
----------------------

now start celery worker using this command...

celery -A  xyz worker --loglevel=INFO  #...can add other parameters like concurrency and all! will see latr

This command by default create as many celery parallel processes as there are number of cores in the cpu. say if quadcore then if you check with ps after above command

ps celery

then you can see that 4 processes are created using above command.

----------------------------------------------------------------------------------------------------------------------------------------------

for using celery we need to instantiate its library and we generally give it name app.

In one project, we can create different celery instances that maps to different set of configurations and tasks as celery is thread safe.

from celery import Celery
app = Celery()
app
<Celery __main__ at 0x7f8c0999d128>  # this is textual representation of app classname = Celery current main module __main__ + memory address of object
crap = Celery()
crap
<Celery __main__ at 0x7f8c03097e10>
<Classname__modulename___at memory address of obj>  # this is the structure of any celery app.

as we can see app and crap are 2 seperate instances of celery that are defined one after another. they can be mapped to different set of tasks to keep work seperate.


Now once we have created an istance first thing we want to do is to configure it. configure it
one basic way is

app.property_name = setting ( i.e. through coding )

other options are like loading it from a class ,or environment varable

-----------------------------------------------------------------------------------------------------------------------------------------------

How to create task? how celery worker understands task?

 @app.task -- this decorator undertands that function is a task

from celery import Celery
app = Celery()
crap = Celery)

@app.task  ------> by this def "add" will be used by celery instance app , If i make it crap then this def will be mapped to instance crap
def add(a,b):
    return a + b


app # it is a celery instance
<Celery __main__ at 0x7f0df3396668> --> here module name is main!!

add # its a function
<@task: __main__.add of __main__ at 0x7f0df3396668> as we can see the memory address of task is same as that of celery instance..


@app.task
def sub(a,b):
    return a - b
sub
<@task: __main__.sub of __main__ at 0x7f0df3396668>  similary for sub also memory address is same.

what is the name of the task?

add.name
'__main__.add'  # as we can see name is created as < __main__. + name of function >
sub.name
'__main__.sub'



when we create a task what happens is it creates a mapping of task name to function name , this is maintained in task registery.

Whenever you define a task, that task will also be added to the local registry

whenever Celery isn’t able to detect what module the function belongs to, it uses the main module name to generate the beginning of the task name.


whenever we import any task from anyother file then the module name will no longer remain __main__


from rand import runme
runme.name
'rand.runme' --> here rand  is the module name!!

basically if you are not importing your task from anywhere i.e. it is at its beginning then the name will be  __main__.function_name
but if you are importing it then it is file_name.function_name


If we want instead of __main__ anyother name should be used at first then

crap = Celery('dome')  # here dome is the module name that we have given in input and is being used by celery
@crap.task
def sade():
    return 2
sade.name
'dome.sade'  -- basically this is the name that task decorator creates automatically! we can also give our custom names to the tasks!!


----------------------------------------------------------------------------------------------------------------------------------------------------------------------

It is always more convinient to give every task a name! even if we are not giving names to the task as above task decorator generates one automatically

name will be based on 1) the module the task is defined in, and 2) the name of the task function.


>>> @app.task(name='sum-of-two-numbers')
>>> def add(x, y):
...     return x + y

>>> add.name
'sum-of-two-numbers'

********************************* Best practice: USE MODULE NAME AS NAMESPACE To avoid collisions ***********************************************



Configuring celery application Instance

----------------------------------------------------
we can directly configure like this :

 app.conf.enable_utc = True

-----------------------------------------------------
or use "update" method to set multiple keys at once

>>> app.conf.update(
...     enable_utc=True,
...     timezone='Europe/London',
...)
-------------------------------------------------------
The app.config_from_object() method loads configuration
from a configuration object.
This can be a configuration module, or any object with
configuration attributes.

the way is create a python file say xyz.py or
celeryconfig.py ( used generally)



celeryconfig.py:

enable_utc = True
timezone = 'Europe/London'
.
.
. # keep all setting in this python file

in another file where celery instace is created , import
this configuration


-------------------------------------------------
from celery import Celery

app = Celery()
app.config_from_object('celeryconfig') # ******** why we have used celeryconfig as a string here? why haven't we imported it as module?

# celeryconfig can be imported seperately and that will also work but its not RECOMMENDED.

Using the name of a module is recommended as this means the module does not need to be serialized when the prefork pool is used.
If you’re experiencing configuration problems or pickle errors then please try using the name of a module instead.
-------------------------------------------------
and the app will be able to use it as long as import
celeryconfig is possible.
-----------------------------------------------------------
We can also create a class and use it as object

from celery import Celery

app = Celery()

class Config:
    enable_utc = True
    timezone = 'Europe/London'

app.config_from_object(Config)
# or using the fully qualified
----------------------------------------------------------------
We can configure from envvar:

import os
from celery import Celery

#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')

You can then specify the configuration module to use via the environment:

$ CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l info
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Hiding and Showing sensitive configuration information:


Say I am in a situation where i want to print all the configuration information for some debugging purpose

app.conf.humanize(with_defaults=True, censored=False)  --> here true means we want to see them , false means we want to hide them

app.conf.table(with_defaults=False, censored=True) # returns dictionary , above one returns string!

Celery can't hide all sensitive info. it will only hide if  if the name contains any of these sub-strings:

API, TOKEN, KEY, SECRET, PASS, SIGNATURE, DATABASE

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

What happens when a celery instance is created?
-----------------------------------------------

Creating a Celery instance will only do the following:

Create a logical clock instance, used for events.
Create the task registry. (creates a place to store mapping of task name and function corresponding to them)
Set itself as the current app (but not if the set_as_current argument was disabled)

app.set_as_current
True    ---> this is true by default

Call the app.on_init() callback (does nothing by default).


What happens when we write @app.task ?
----------------------------------------
e app.task() decorators don’t create the tasks at the point when the task is defined, instead it’ll defer the creation of the task to happen either when the task is used, or after
the application has been finalized,


Finalization of the app happens either explicitly by calling app.finalize() – or implicitly by accessing the app.tasks attribute.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

What is difference between task and shared task?

There is a difference between @task(shared=True) and @shared_task


The task decorator will share tasks between apps by default so that if you do:


    app1 = Celery()
    @app1.task
    def test():
        pass

    app2 = Celery()

the test task will be registered in both apps:

     assert app1.tasks[test.name]
     assert app2.tasks[test.name]

but test will be configured using app1's configuration not app2 and it will always use app1's configuration.

However if we are using @shared_task decorator

The @shared_task decorator returns a proxy that always uses the task instance
in the current_app:


    app1 = Celery()

    @shared_task
    def test():
        pass
    assert test.app is app1


    app2 = Celery()
    assert test.app is app2

This makes the @shared_task decorator useful for libraries and reusable apps,
since they will not have access to the app of the user.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


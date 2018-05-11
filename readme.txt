This is django + celery tutorials. 

Commands to Install broker:

------------------------------------------------------------------------------------


sudo apt-get install rabbitmq-server
sudo service rabbitmq-server restart -- we need to restart it!
sudo rabbitmqctl status  -- to check if server is started or not

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Now create a python file with any name say xyz.py

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

celery -A <file name where above code is kept> worker --loglevel=INFO  #...can add other parameters like concurrency and all! will see latr

This command by default create as many celery parallel processes as there are number of cores in the cpu. say if quaqcore then if you check with ps after above command

ps celery

then you can see that 4 processes are created using above command.

----------------------------------------------------------------------------------------------------------------------------------------------
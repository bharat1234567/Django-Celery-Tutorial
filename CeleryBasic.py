from rand import *
import time

# before runnint this start celery worker using : celery -A rand  worker --loglevel=INFO
start = time.time()
for i in range(0,100):
    runme.delay(i)
end = time.time()
print(end-start)


# as we can see process to delegate task to worker took only 0.08506536483764648 secs.
# ie. for loop completed and ended..now tasks were taken by workers seperately..

# on the contrary it would have taken 100 secs to execute linearly!!


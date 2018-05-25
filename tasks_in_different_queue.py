from rand import *
import time

# before runnint this start celery worker using : celery -A rand  worker --loglevel=INFO
start = time.time()
for i in range(0,100):
    task_1.delay(i)
end = time.time()
print(end-start)

start = time.time()
for i in range(0,100):
    task_2.delay(i)
end = time.time()
print(end-start)
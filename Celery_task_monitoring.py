from rand import dump_context
from celery.result import AsyncResult
import time


list_tasks = []

def runme():
    for i in range(1,100):
        s = dump_context.delay(1, 2)
        list_tasks.append(s.task_id)


def getStatus():
    i = 1
    for task_id in list_tasks:
        res = AsyncResult(task_id)
        print(str(i) + " , " + str(task_id) + "  , " + str(res.status))
        i = i + 1


# by this way we can get number of tasks completed , pending or failed. but we need to make sure that celery gets proper time
# to execute the tasks!!
# log it if tasks status is failed due to some reason!!
# one way to track it for latr is to write all tasks id on a file and get it read latr and check its status on scheduled basis.
# once done
def function_to_get_number_of_tasks_completed_pending_or_failed():
    result = []
    completed_tasks = 0
    pending_tasks = 0
    failed_tasks = 0
    for task_id in list_tasks:
        res = AsyncResult(task_id)
        if res.status == 'SUCCESS':
            completed_tasks += 1
        elif res.status == 'PENDING':
            pending_tasks += 1
        else:
            failed_tasks += 1
    result.append(completed_tasks)
    result.append(pending_tasks)
    result.append(failed_tasks)
    return result




runme()
#time.sleep(3)
#getStatus()
res = []
res = function_to_get_number_of_tasks_completed_pending_or_failed()
print(res[0])
print(res[1])
print(res[2])
# res = AsyncResult(s.task_id)
# res.status
# 'SUCCESS' -- if its success --> task is completed successfully
# res.ready() -- if we want to do something
# True

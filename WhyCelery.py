# Lets understand why celery is needed at first place..
# say i want to run a function like this one

import time


def runme(i):
    print(i)

start = time.time()
for i in range(0,100000):
    runme(i)
end = time.time()
print(end-start)

# so as we can see it took around 0.231 sec time to run this code.. as its just a print function..
#CPU never has to wait for anything, all imputs etc everything are coming from code only..

# In real life scenarion where things go complex there comes waiting time for I/O, some complex processing time say Image manipulation etc
# Anything basically which is cpu extensive and is going to take some good time..

# runme function in that case will have some delay , lets create some other function runmewithwait



def runmewithwait(i):
    time.sleep(1)
    print(i)


start = time.time()
for i in range(0,20):
    runmewithwait(i)
end = time.time()
print(end - start)

# It almost took 20 secs just to print from 1 to 20 as the process is linear...
# here until n unless cpu prints 1 , it won't go ahead and print 2 ,, it will wait for definite time

# say I don't bother how and in which order they are getting printed , I just want that they should get printed.. thats it!!
# i.e. we are making this task asynchronous!

# so basically by using celery this waiting time of 1 sec we have given can be utilized by celery!! Lets see how we can actually do that!!

# if we make it 100 it will take 100+ secs to run , lets see how much time it will be taken by celery!!

# go to readme.txt file and see how to install broker, start it and check its working fine. broker is nothing but a queue where async tasks will be kept by workers to pick then and
#execute them

#once done go to CeleryBasic and see how it can be executed..
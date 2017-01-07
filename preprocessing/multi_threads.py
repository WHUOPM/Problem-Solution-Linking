
from multiprocessing.dummy import Pool as ThreadPool 
import datetime

ints=range(10000000)




def addone(num):
	return num+1



# Make the Pool of workers
pool = ThreadPool(10) 
# Open the urls in their own threads
# and return the results
start = datetime.datetime.now()
results = pool.map(addone, ints)

end = datetime.datetime.now()
print (end - start).seconds

#close the pool and wait for the work to finish 
pool.close() 
pool.join() 
start = datetime.datetime.now()
for i in range(10000000):
	addone(i)
end = datetime.datetime.now()
print (end - start).seconds



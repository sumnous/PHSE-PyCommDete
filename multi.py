
from multiprocessing import Process,Array,Pool

def sleep_and_print(a):
    import time
    time.sleep(3)
    return a+a

if __name__ == "__main__":
    result=[]
    pool = Pool(5)
    for x in range(5):
        result.append(pool.apply_async(sleep_and_print, (x,)))
        
    pool.close()
    pool.join()
    print [x.get() for x in result]
    
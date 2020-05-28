import time
from datetime import datetime


def logged(format):
    def new(func):
        def count(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            print(f"Finished '{func.__name__}', execution time =  {(datetime.now()-start).total_seconds()}s")
            print(f"Running '{func.__name__}', on {datetime.now().strftime(format)}")
            return result
        return count
    return new


@logged("%b %d %Y - %H:%M:%S")
def add1(x, y):
    time.sleep(1)
    return x + y

@logged("%b %d %Y - %H:%M:%S")
def add2(x, y):
    time.sleep(2)
    return x + y

print(add1(1, 2))
print(add2(1, 2))


# Output:
#- Running 'add1' on Jul 24 2013 - 13:40:47
#- Finished 'add1', execution time = 1.001s

# Running 'add2' on Jul 24 2013 - 13:40:48
#- Finished 'add2', execution time = 2.001s

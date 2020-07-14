import time
from threading import Thread
from queue import Queue

__all__ = ['ThreadPool']


class Worker(Thread):

    def __init__(self, name, tasklist):
        Thread.__init__(self)
        self.name = name
        self.tasklist = tasklist

    def run(self):
        while True:
            task, job = self.tasklist.get()
            job(task)
            if self.tasklist.empty():
                time.sleep(2)


class ThreadPool:
    def __init__(self):
        self.__task_list = Queue()
        self.worker_list = [Worker(i, self.__task_list) for i in range(0, 1)]
        for worker in self.worker_list:
            worker.start()

    def add_task(self, task):
        self.__task_list.put(task)

from threading import Thread
from queue import Queue


class ThreadPool:
    """Create a new ThreadPool.

    The size is the number of threads in the pool.

    The constructor will fail if the size is zero.
    """

    def __init__(self, size):
        assert size > 0

        self.channel = Queue()
        self.workers = list()

        for idx in range(0, size):
            self.workers.append(Worker(idx, self.channel))

    def execute(self, target, args):
        self.channel.put((target, args))

    # Closure alternative
    # def execute(self, job):
    #     self.channel.put(job)


class Worker:
    def __init__(self, idx, channel):
        self.id = idx
        self.thread = Thread(target=self._work, args=[channel]).start()

    def _work(self, channel):
        while True:
            target, args = channel.get()
            # job = channel.get()  # Closure alternative
            print(f"Worker {self.id} got a job; executing.")
            target(*args)
            # job()  # Closure alternative

            channel.task_done()

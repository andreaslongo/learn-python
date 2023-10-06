from threading import Thread
from queue import Queue


class ThreadPool:
    """Create a new ThreadPool.

    The size is the number of threads in the pool.

    The constructor will fail if the size is zero.
    """

    def __init__(self, size):
        assert size > 0

        self.workers: list[Worker] = list()
        self.sender: Queue = Queue()

        for idx in range(0, size):
            worker = Worker(idx, self.sender)
            print(f"Starting worker {worker.id}")
            self.workers.append(worker)

    def __del__(self):
        for worker in self.workers:
            print(f"Shutting down worker {worker.id}")
            self.sender.put(("shutdown", "now"))

    def execute(self, target, args):
        self.sender.put((target, args))

    # Closure alternative
    # def execute(self, job):
    #     self.sender.put(job)


class Worker:
    def __init__(self, idx, receiver):
        self.id = idx
        self.receiver = receiver
        #        self.thread = Thread(target=self.run, args=[self.id, self.receiver])
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            target, args = self.receiver.get()
            # job = receiver.get()  # Closure alternative
            if (target, args) == ("shutdown", "now"):
                print(f"Worker {self.id} disconnected; shutting down.")
                self.receiver.task_done()
                break

            print(f"Worker {self.id} got a job; executing.")
            target(*args)
            # job()  # Closure alternative
            self.receiver.task_done()

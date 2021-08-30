import queue
import threading
from time import sleep, time


class QueueWorker(threading.Thread):
    SENTINEL = object()
    def __init__(self, queue: queue.Queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            if item is self.SENTINEL:
                return
            #sleep(4)
            print(item)
            self.queue.task_done()

    def close(self):
        self.queue.put(self.SENTINEL)


def stack(no: str, q: queue.Queue):
    for item in range(30):
        t = time()
        q.put(f'{no}:{item}:{t}')


q = queue.Queue(1)

queue_thread = QueueWorker(q)
queue_thread.start()

find_thread1 = threading.Thread(target=stack, args=(1, q))
find_thread2 = threading.Thread(target=stack, args=(2, q))

find_thread1.start()
find_thread2.start()
find_thread1.join()
find_thread2.join()

queue_thread.close()

#q.join()
queue_thread.join()

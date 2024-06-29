import time
import shared_event_manager
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

QueueManager.register('get_queue')

def reader(event):
    manager = QueueManager(address=('localhost', 50000), authkey=b'queue')
    manager.connect()
    queue = manager.get_queue()

    while True:
        if not queue.empty():
            message = queue.get()
            print(f"Consumed: {message}")
        else:
            print("No message in the queue")
        event.clear()
        time.sleep(1)

if __name__ == '__main__':
    event = shared_event_manager.create_event()
    reader(event)

import time
import random
import string
import shared_event_manager
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

QueueManager.register('get_queue')

def generate_random_message(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def writer(event):
    manager = QueueManager(address=('localhost', 50000), authkey=b'queue')
    manager.connect()
    queue = manager.get_queue()

    while True:
        message = generate_random_message()
        queue.put(message)
        print(f"Produced: {message}")
        event.set()
        time.sleep(1)

if __name__ == '__main__':
    event = shared_event_manager.create_event()
    writer(event)

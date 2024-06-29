import multiprocessing
from multiprocessing.managers import BaseManager

queue = multiprocessing.Queue()

class QueueManager(BaseManager):
    pass

def get_queue():
    global queue
    return queue

QueueManager.register('get_queue', callable=get_queue)

def start_server():
    manager = QueueManager(address=('', 50000), authkey=b'queue')
    server = manager.get_server()
    print("Server started at port 50000")
    server.serve_forever()

if __name__ == '__main__':
    start_server()

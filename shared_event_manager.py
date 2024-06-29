import multiprocessing
from multiprocessing.managers import BaseManager

event = multiprocessing.Event()

class EventManager(BaseManager):
    pass

def get_event():
    global event
    return event

EventManager.register('get_event', callable=get_event)

def start_event_server():
    manager = EventManager(address=('', 50001), authkey=b'event')
    server = manager.get_server()
    print("Event server started at port 50001")
    server.serve_forever()

def create_event():
    manager = EventManager(address=('localhost', 50001), authkey=b'event')
    manager.connect()
    return manager.get_event()

if __name__ == '__main__':
    start_event_server()

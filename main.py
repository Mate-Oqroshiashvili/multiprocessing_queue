import multiprocessing
import shared_queue_manager
import shared_event_manager
import writer
import reader
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_manager():
    manager_port = 50000

    if not is_port_in_use(manager_port):
        manager_process = multiprocessing.Process(target=shared_queue_manager.start_server)
        manager_process.start()
        print("Queue manager started.")
        return manager_process
    else:
        print(f"Port {manager_port} is already in use. Assuming the manager is already running.")
        return None

def start_event_manager():
    event_port = 50001

    if not is_port_in_use(event_port):
        event_manager_process = multiprocessing.Process(target=shared_event_manager.start_event_server)
        event_manager_process.start()
        print("Event manager started.")
        return event_manager_process
    else:
        print(f"Port {event_port} is already in use. Assuming the event manager is already running.")
        return None

if __name__ == '__main__':
    manager_process = start_manager()
    event_manager_process = start_event_manager()

    event = shared_event_manager.create_event()

    writer_process = multiprocessing.Process(target=writer.writer, args=(event,))
    reader_process = multiprocessing.Process(target=reader.reader, args=(event,))

    writer_process.start()
    reader_process.start()

    writer_process.join()
    reader_process.join()

    if manager_process and manager_process.is_alive():
        manager_process.terminate()
        print("Queue manager terminated.")

    if event_manager_process and event_manager_process.is_alive():
        event_manager_process.terminate()
        print("Event manager terminated.")

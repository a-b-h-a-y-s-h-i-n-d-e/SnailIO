from queue import Queue
import time

event_loop = Queue()

def run(main_task):
    from .task import Task
    event_loop.put(Task(main_task))

    while not event_loop.empty():
        task = event_loop.get()

        # skip cancelled task
        if task.cancelled:
            task.finished = True
            continue

        # setting current time for timeout
        if task.timeout is not None and task.start_time is None:
            task.start_time = time.monotonic()

        # now checking for timeout
        if task.timeout is not None and task.start_time is not None:
            elapsed = time.monotonic() - task.start_time
            if elapsed >= task.timeout:
                task.cancel()
                task.finished = True
                print(f"Task : {task.name} got cancelled due to timeout after {task.timeout}")
                continue


        try:
            task.iter.send(None)
        except StopIteration:
            task.finished = True
        else:
            event_loop.put(task)
    

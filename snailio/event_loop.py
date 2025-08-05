from queue import Queue

event_loop = Queue()

def run(main_task):
    from snailio.task import Task
    event_loop.put(Task(main_task))

    while not event_loop.empty():
        task = event_loop.get()
        try:
            task.iter.send(None)
        except StopIteration:
            task.finished = True
        else:
            event_loop.put(task)


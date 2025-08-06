from .event_loop import event_loop
import time

class Task:
    def __init__(self, generator, name=None, timeout=None):
        self.iter = generator
        self.name = name or f"{id(generator)}"
        self.finished = False
        self.cancelled = False
        self.timeout = timeout

        self.start_time = None


    def __await__(self):
        while not self.finished:
            yield self
    
    def __repr__(self):
        return f"Task name={self.name} , done={self.finished}"

    def done(self):
        return self.finished
    
    def cancel(self):
        self.cancelled = True

        
    

def create_task(generator, name=None, timeout=None):
    task = Task(generator, name=name, timeout=timeout)
    event_loop.put(task)
    return task

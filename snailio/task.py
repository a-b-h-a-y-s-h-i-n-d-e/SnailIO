from snailio.event_loop import event_loop

class Task:
    def __init__(self, generator, name=None):
        self.iter = generator
        self.finished = False
        self.name = name or f"{id(generator)}"

    def done(self):
        return self.finished

    def __await__(self):
        while not self.finished:
            yield self
    
    def __repr__(self):
        return f"Task name={self.name} , done={self.finished}"

def create_task(generator, name=None):
    task = Task(generator, name=name)
    event_loop.put(task)
    return task


import time
from snailio.task import create_task

def _sleep(seconds):
    start = time.time()
    while time.time() - start < seconds:
        yield

async def sleep(seconds):
    task = create_task(_sleep(seconds))
    return await task


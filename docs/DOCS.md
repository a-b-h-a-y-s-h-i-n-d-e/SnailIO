# SnailIO Documentation


## API Reference

### Event Loop Module (`event_loop.py`)

#### `run(main_task)`

Starts the event loop with the specified main task and continues until all tasks are complete.

**Parameters:**
- `main_task` *(generator/coroutine)*: The main coroutine to start the event loop with

**Behavior:**
- Creates a Task wrapper around the main coroutine
- Continuously processes tasks from the event loop queue
- Skips cancelled tasks
- Handles task timeouts by tracking start time and elapsed duration
- Executes tasks by calling `task.iter.send(None)`
- Re-queues unfinished tasks for continued execution
- Stops when the queue is empty

**Example:**
```python
import snailio

async def main():
    print("Starting application")
    await snailio.sleep(1)
    print("Application finished")

snailio.run(main())
```

---

### Task Module (`task.py`)

#### `create_task(generator, name=None, timeout=None)`

Creates a new Task object and immediately schedules it in the event loop.

**Parameters:**
- `generator` *(generator/coroutine)*: The coroutine to wrap in a task
- `name` *(str, optional)*: Human-readable name for the task. Defaults to `str(id(generator))`
- `timeout` *(float, optional)*: Maximum execution time in seconds. Task will be cancelled if exceeded

**Returns:**
- `Task`: A Task object that can be awaited

**Example:**
```python
import snailio

async def my_coroutine():
    print("simple coroutine")
    await snailio.sleep(1)


async def main():
    # With name and timeout
    task = snailio.create_task(
        my_coroutine(), 
        name="my-task", 
        timeout=5.0
    )

    await task

snailio.run(main())
```

#### `Task` Class

A wrapper around generators/coroutines that provides scheduling and management functionality.

##### Constructor: `Task(generator, name=None, timeout=None)`

**Parameters:**
- `generator` *(generator/coroutine)*: The generator/coroutine to execute
- `name` *(str, optional)*: Task identifier for debugging
- `timeout` *(float, optional)*: Maximum execution time in seconds

**Attributes:**
- `iter` *(generator)*: The wrapped generator/coroutine
- `name` *(str)*: Human-readable task name
- `finished` *(bool)*: Whether task has completed (successfully or via cancellation)
- `cancelled` *(bool)*: Whether task has been cancelled
- `timeout` *(float)*: Maximum execution time in seconds
- `start_time` *(float)*: Timestamp when task started executing (set by event loop)

##### `__await__()`

Makes the Task awaitable by implementing the await protocol.

**Yields:**
- `Task`: Self reference while task is running

**Behavior:**
- Continuously yields `self` until `self.finished` is `True`
- Allows the task to be used with `await` keyword
- Integrates with the event loop's task scheduling

**Example:**
```python
# wrap this task in async method and then use snailio.run()
task = snailio.create_task(some_coroutine())
result = await task  # Uses __await__ internally
```

##### `__repr__()`

Returns a string representation of the task.

**Returns:**
- `str`: Formatted string showing task name and completion status

**Format:** `"Task name={name} , done={finished}"`

##### `done()`

Checks if the task has finished execution.

**Returns:**
- `bool`: `True` if task is finished (completed or cancelled), `False` otherwise

**Example:**
```python
# wrap this task in async method and then use snailio.run()
task = snailio.create_task(some_coroutine())
if task.done():
    print("Task is complete")
```

##### `cancel()`

Marks the task for cancellation.

**Behavior:**
- Sets `self.cancelled = True`
- Task will be skipped on next event loop iteration
- Does not immediately stop currently executing task
- Cancellation is cooperative and takes effect on next yield

**Example:**
```python
# wrap this task in async method and then use snailio.run()
task = snailio.create_task(long_running_task())
task.cancel()  # Will be cancelled on next loop iteration
```

---

### Sleep Module (`sleep.py`)

#### `sleep(seconds)`

Provides non-blocking sleep functionality that yields control to other tasks.

**Parameters:**
- `seconds` *(float)*: Duration to sleep in seconds. Can be fractional for sub-second precision

**Returns:**
- `None`: Function doesn't return a value, just suspends execution

**Behavior:**
- Creates an internal `_sleep()` generator task
- Yields control back to event loop during sleep period
- Allows other tasks to run concurrently during sleep
- More cooperative than `time.sleep()` which blocks the entire thread


#### `_sleep(seconds)` *(Internal Function)*

Internal generator that implements the actual sleep mechanism.

**Parameters:**
- `seconds` *(float)*: Duration to sleep in seconds

**Yields:**
- `None`: Yields control back to event loop on each iteration

**Behavior:**
- Records start time using `time.time()`
- Continuously yields until elapsed time exceeds specified duration
- Uses busy-waiting approach with cooperative yielding
- Not intended for direct use (use `sleep()` instead)

**Implementation Details:**
```python
def _sleep(seconds):
    start = time.time()
    while time.time() - start < seconds:
        yield  # Yield control back to event loop
```

---

## Module Integration

### How Components Work Together

1. **Event Loop** (`event_loop.py`):
   - Central scheduler that manages task execution
   - Processes tasks from a FIFO queue
   - Handles timeouts and cancellation

2. **Task Management** (`task.py`):
   - Wraps coroutines in manageable Task objects
   - Provides await semantics and status tracking
   - Integrates with event loop for scheduling

3. **Cooperative Sleep** (`sleep.py`):
   - Demonstrates how to create awaitable functions
   - Uses internal task creation for non-blocking delays
   - Shows proper yielding patterns for cooperative multitasking

### Execution Flow

```python
# 1. Main task is created and added to event loop queue
snailio.run(main())

# 2. Event loop processes tasks one by one
while not event_loop.empty():
    task = event_loop.get()
    
    # 3. Task executes until it yields (await)
    task.iter.send(None)
    
    # 4. If not finished, task goes back in queue
    if not task.finished:
        event_loop.put(task)

# 5. Loop continues until all tasks complete
```

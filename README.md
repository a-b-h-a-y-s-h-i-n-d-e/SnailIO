<p align="center">
  <h1 align="center">🐌 snailio</h1>
  <h3 align="center"><code>Minimal asyncio-inspired event loop written from scratch</code></h3>
   
---
</p>
<p align="center">
 <img src="assets/logo.png" alt="snail logo" width="1000"/>
</p>

---



### 🐌 What is snailio?

**snailio** is a tiny educational Python library that mimics the core ideas behind `asyncio` — but built from scratch using generators and queues.

It supports:
- Asynchronous `sleep`
- Creating and awaiting tasks
- Naming tasks for better tracking
- A custom event loop

### 📦 Installation (local)

```bash
git clone https://github.com/a-b-h-a-y-s-h-i-n-d-e/snailio.git
cd snailio
pip install -e .
```

### 🚀 Usage Example

```python
import snailio

async def task1():
    for _ in range(2):
        print('Task 1')
        await snailio.sleep(1)

async def task2():
    for _ in range(3):
        print('Task 2')
        await snailio.sleep(0)

async def main():
    one = snailio.create_task(task1(), name="first task")
    two = snailio.create_task(task2(), name="second task")

    await one
    await two

    print('done')

if __name__ == '__main__':
    snailio.run(main())
```

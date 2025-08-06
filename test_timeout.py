import snailio
import time

async def task1():
    for _ in range(2):
        print('Task 1')
        time.sleep(2)
        await snailio.sleep(1)

async def task2():
    for _ in range(3):
        print('Task 2')
        await snailio.sleep(0)

async def main():
    one = snailio.create_task(task1(), name = "timepass", timeout=2)
    two = snailio.create_task(task2())

    print(one)


    await one
    await two
    
    print(one)
    print('done')


if __name__ == '__main__':
    snailio.run(main())

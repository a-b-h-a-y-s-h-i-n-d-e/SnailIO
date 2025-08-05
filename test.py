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
    one = snailio.create_task(task1(), "timepass")
    two = snailio.create_task(task2())
    print(one)
    print(two)
    await one
    await two
    print(one) 
    print('done')


if __name__ == '__main__':
    snailio.run(main())

from celery import shared_task

@shared_task
def test_asyncio():
    for i in range(1000000):
        print(i)
    return None
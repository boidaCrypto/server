from celery import shared_task

@shared_task
def test():
    for i in range(100000):
        print(i)

    return None
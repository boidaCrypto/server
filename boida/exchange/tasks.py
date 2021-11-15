from celery import shared_task

@shared_task
def exchange_synchronization(ACCESS_KEY, SECRET_KEY):
    print(ACCESS_KEY, SECRET_KEY)

    return None
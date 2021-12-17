from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
import asyncio
import multiprocessing as mp
import time


async def async_func1():
    print("hello")


async def make_americano():
    print("Americano Start")
    await asyncio.sleep(3)
    print("Americano End")
    return "Americano"

async def make_latte():
    print("Latte Start")
    await asyncio.sleep(5)
    print("Latte End")
    return "Latte"

async def main():
    coro1 = make_americano()
    coro2 = make_latte()
    result = await asyncio.gather(
        coro1,
        coro2
    )
    print(result)

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def Test(request, format=None):
    # print("Main Start")
    # asyncio.run(main())
    # print("Main End")
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(async_func1())
    # loop.close()
    def worker():
        proc = mp.current_process()
        print(proc.name)
        print(proc.pid)
        time.sleep(5)
        print("SubProcess End")

    if __name__ == "__main__":
        proc = mp.current_process()
        print(proc.name)
        print(proc.pid)
        p = mp.Process(name="SubProcess", target=worker())
        p.start()
        print("MainProcess End")
    return Response(status=status.HTTP_200_OK)

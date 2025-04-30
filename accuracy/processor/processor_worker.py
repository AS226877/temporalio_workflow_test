import asyncio
import math
import random

from temporalio import activity
from temporalio.client import Client
from temporalio.worker import Worker

PROCESSOR_TASK_QUEUE = "processor-task-queue"


@activity.defn
async def sqrt_activity(number: float) -> float:
    total_duration = 60
    step = 10

    print("Got new request! Performing sqrt action!")

    for elapsed in range(0, total_duration, step):
        activity.heartbeat(f"Progress: {elapsed + step} / {total_duration} seconds")
        await asyncio.sleep(step)

    print("Finished sqrt action!")
    return math.sqrt(number)


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=PROCESSOR_TASK_QUEUE,
        activities=[sqrt_activity],
    )
    print("Processor worker started. Waiting for tasks...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

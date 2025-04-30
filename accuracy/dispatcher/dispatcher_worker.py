import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.client import Client
from temporalio.common import RetryPolicy
from temporalio.worker import Worker

ACCURACY_TASK_QUEUE = "accuracy-task-queue"
PROCESSOR_TASK_QUEUE = "processor-task-queue"


@dataclass
class AutomationPipelineInput:
    image_path: str
    image_type: str


# --- Accuracy Workflow ---
@workflow.defn
class AccuracyWorkflow:
    @workflow.run
    async def run(self, data) -> float:
        print(f"Received new request! {data}")
        print("Ignoring data! This is test anyway lol")
        numbers = [42.0] * 20  # Deterministic!
        # Send each number to the processor task queue as a separate activity
        futures = [
            workflow.execute_activity(
                activity="sqrt_activity",
                arg=n,
                task_queue=PROCESSOR_TASK_QUEUE,
                start_to_close_timeout=timedelta(seconds=70),
                retry_policy=RetryPolicy(
                    maximum_attempts=3,  # 1 original attempt + 2 retries = 3 total
                ),
            )
            for n in numbers
        ]
        # Wait for all results
        print(f"Running {len(futures)} requests to processor")
        results = await asyncio.gather(*futures)
        result = sum(results)
        print(f"Result is {result}")
        return result


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client=client,
        task_queue=ACCURACY_TASK_QUEUE,
        workflows=[AccuracyWorkflow],
        activities=[],  # No activities registered here
    )
    print("Dispatcher worker started. Waiting for workflows...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

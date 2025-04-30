import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

INGESTION_TASK_QUEUE = "ingestion-task-queue"


@dataclass
class AutomationPipelineInput:
    image_path: str
    image_type: str


@activity.defn
async def process_ingestion(request: AutomationPipelineInput) -> bool:
    print("Performing ingestion process!")
    if type(request.image_path) != str:
        print("Ingestion failed! Image path invalid")
        return False
    else:
        print("Ingestion success!")
        return True


# --- Ingestion Workflow ---
@workflow.defn
class IngestionWorkflow:
    @workflow.run
    async def run(self, data) -> float:
        print(f"Received new request! {data}")
        result = await workflow.execute_activity(
            activity=process_ingestion,
            arg=data,
            start_to_close_timeout=timedelta(seconds=3),
        )
        print(f"Ingestion workflow finished with result {result}")
        return result


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client=client,
        task_queue=INGESTION_TASK_QUEUE,
        workflows=[IngestionWorkflow],
        activities=[process_ingestion],
    )
    print("Ingestion worker started. Waiting for workflows...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

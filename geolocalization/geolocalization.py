import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

GEOLOCALIZATION_TASK_QUEUE = "geolocalization-task-queue"


@dataclass
class AutomationPipelineInput:
    image_path: str
    image_type: str


@activity.defn
async def process_geolocalization(request: AutomationPipelineInput) -> bool:
    print("Performing geolocalization process!")
    if type(request.image_type) != str:
        print("Geolocalization failed! Image path invalid")
        return False
    else:
        print("Geolocalization success!")
        return True


# --- Ingestion Workflow ---
@workflow.defn
class GeolocalizationWorkflow:
    @workflow.run
    async def run(self, data) -> float:
        print(f"Received new request! {data}")
        result = await workflow.execute_activity(
            activity=process_geolocalization,
            arg=data,
            start_to_close_timeout=timedelta(seconds=3),
        )
        print(f"Ingestion workflow finished with result {result}")
        return result


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client=client,
        task_queue=GEOLOCALIZATION_TASK_QUEUE,
        workflows=[GeolocalizationWorkflow],
        activities=[process_geolocalization],
    )
    print("Geolocalization worker started. Waiting for workflows...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import uuid
from dataclasses import dataclass

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker

AUTOMATION_TASK_QUEUE = "automation-pipeline-queue"
INGESTION_TASK_QUEUE = "ingestion-task-queue"
ACCURACY_TASK_QUEUE = "accuracy-task-queue"
GEOLOCALIZATION_TASK_QUEUE = "geolocalization-task-queue"


@dataclass
class AutomationPipelineInput:
    image_path: str
    image_type: str


# --- Automation Workflow ---
@workflow.defn
class AutomationWorkflow:
    @workflow.run
    async def run(self, data: AutomationPipelineInput) -> str:
        print(f"Received new request! {data}")
        orchestrator_id = workflow.info().workflow_id

        if data.image_type == "Navad":
            print("Executing Ingestion workflow for Navad flight!")
            result = await workflow.execute_child_workflow(
                workflow="IngestionWorkflow",
                task_queue=INGESTION_TASK_QUEUE,
                id=f"{orchestrator_id}-ingestion",
                arg=data,
            )
            if result is False:
                return "Automation pipeline failed at ingestion!"
            print("Ingestion workflow succeeded! Running accuracy workflow")
            result = await workflow.execute_child_workflow(
                workflow="AccuracyWorkflow",
                task_queue=ACCURACY_TASK_QUEUE,
                id=f"{orchestrator_id}-accuracy",
                arg=data,
            )
            print("Finished accuracy! Automation pipeline completed.")
            if result is False:
                return "Automation pipeline failed at accuracy!"
            return "Success automation for Navad."

        elif data.image_type == "Satellite":
            print("Executing geolocalization workflow for Satellite!")
            result = await workflow.execute_child_workflow(
                workflow="GeolocalizationWorkflow",
                task_queue=GEOLOCALIZATION_TASK_QUEUE,
                id=f"{orchestrator_id}-geolocalization",
                arg=data,
            )
            if result is False:
                return "Automation pipeline at geolocalization"
            return "Success automation for Satellite."
        else:
            raise ValueError(f"Image type {data.image_type} is not a supported type.")


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client=client,
        task_queue=AUTOMATION_TASK_QUEUE,
        workflows=[AutomationWorkflow],
        activities=[],  # No activities registered here
    )
    print("Automation worker started. Waiting for workflows...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

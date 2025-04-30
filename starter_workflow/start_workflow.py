import asyncio
import uuid

from temporalio.client import Client

from dataclasses import dataclass

from temporalio.common import SearchAttributes, TypedSearchAttributes, SearchAttributePair, SearchAttributeKey, \
    SearchAttributeValue

AUTOMATION_TASK_QUEUE = "automation-pipeline-queue"


@dataclass
class AutomationPipelineInput:
    image_path: str
    image_type: str


async def main():
    client = await Client.connect("localhost:7233")
    navad_request = AutomationPipelineInput(
        image_path="My_path", image_type="Navad"
    )
    # Start the workflow
    workflow_id = f"automation-workflow-{str(uuid.uuid4())}"

    search_attrs = TypedSearchAttributes([
        SearchAttributePair(
            key=SearchAttributeKey.for_text("CustomStringField"),
            value="my-workflow-id"  # ✅ Pass list directly
        ),
        SearchAttributePair(
            key=SearchAttributeKey.for_keyword("CustomKeywordField"),
            value="navad"
        ),
        SearchAttributePair(
            key=SearchAttributeKey.for_int("CustomIntField"),
            value=42
        ),
        SearchAttributePair(
            key=SearchAttributeKey.for_bool("CustomBoolField"),
            value=True
        ),
    ])

    result = await client.execute_workflow(
        workflow="AutomationWorkflow",
        id=workflow_id,
        task_queue=AUTOMATION_TASK_QUEUE,
        arg=navad_request,
        memo={
            "description": "Navad auto-processing run",
            "initiated_by": "api",
        },
        search_attributes=search_attrs,
        static_summary="Navad run",
        static_details="Created by API dispatch on request"
    )
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())

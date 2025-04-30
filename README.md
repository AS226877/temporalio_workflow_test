# Temporalio Python Workflow Example

This project demonstrates a simple Temporal workflow in Python, where a dispatcher generates 20 random numbers, sends each as a task to a processor, which computes the square root and returns it. The dispatcher then sums all results.

## Project Structure

- `dispatcher/` - Contains the dispatcher workflow code
- `processor/` - Contains the processor activity code
- `starter_workflow/` - Contains the script to start the workflow
- `workflow_manager/` - (Optional) For workflow management utilities

## Prerequisites

- Python 3.8+
- [Temporal CLI](https://docs.temporal.io/cli) (for running a local Temporal server)
- Install dependencies:

```
pip install temporalio
```

## Running Temporal Server (Development)

You can run a local Temporal server using Docker:

```
docker run --rm -d -p 7233:7233 temporalio/auto
```

## How to Run the Example

1. Start the Temporal server (see above).
2. In one terminal, start the worker:

```
python dispatcher/worker.py
```

3. In another terminal, start the workflow:

```
python starter_workflow/start_workflow.py
```

4. The workflow will print the sum of the square roots of 20 random numbers.

## Notes
- This example is for educational purposes and uses random numbers for demonstration.
- Make sure Docker is running if you use the provided Temporal server command.

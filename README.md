# Temporalio Image Processing Pipeline Example

This project demonstrates a sophisticated Temporal workflow in Python for image processing automation. It handles two types of image processing workflows:

1. Navad Flight Images: Goes through ingestion and accuracy processing
2. Satellite Images: Goes through geolocalization processing

## Project Structure

- `accuracy/` - Contains the accuracy processing logic
  - `dispatcher/` - Handles task distribution for accuracy calculations
  - `processor/` - Performs the actual processing tasks
- `geolocalization/` - Contains the geolocalization workflow for satellite images
- `ingestion/` - Handles initial image ingestion processing
- `orchestrator/` - Contains the main automation pipeline workflow
- `starter_workflow/` - Contains the script to start the workflow

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

2. In separate terminals, start each worker:

```
python orchestrator/automation_pipeline.py
python ingestion/ingestion_worker.py
python accuracy/dispatcher/dispatcher_worker.py
python accuracy/processor/processor_worker.py
python geolocalization/geolocalization.py
```

3. In another terminal, start the workflow:

```
python starter_workflow/start_workflow.py
```

## Workflow Description

The system supports two main processing paths:

### Navad Flight Image Processing
1. Image ingestion validation
2. Accuracy processing with parallel task distribution
3. Results aggregation

### Satellite Image Processing
1. Direct geolocalization processing

## Features

- Parallel task processing
- Automatic retry policies
- Progress monitoring through heartbeats
- Search attributes for workflow tracking
- Child workflow orchestration
- Error handling and validation

## Why Temporal.io?

Temporal.io stands out as a powerful workflow orchestration platform with several key advantages:

### Developer Experience
- **Native Language SDKs**: Write workflows in your preferred language (Python, Java, Go, etc.) with full IDE support
- **Type Safety**: Strong typing and compile-time checks help catch errors early
- **Local Development**: Run and debug workflows locally with minimal setup
- **Intuitive API**: Workflows read like normal code - use standard language constructs (loops, conditionals, etc.)

### Reliability & Durability
- **Exactly-Once Execution**: Guarantees that activities run exactly once, crucial for business logic
- **Built-in Fault Tolerance**: Automatic retry mechanisms and error handling
- **State Management**: Automatically persists workflow state - no need for manual checkpointing
- **Long-Running Operations**: Can handle workflows that run for days or months

### Operational Excellence
- **Visibility**: Rich history of workflow execution, searchable and observable
- **Dynamic Scaling**: Workers can be scaled independently based on load
- **Versioning Support**: Built-in support for workflow versioning and updates

### Comparison with Other Tools

#### vs Apache Airflow
- **State Management**: Temporal handles state automatically; Airflow requires external storage
- **Language Support**: Temporal allows business logic in any supported language; Airflow uses Python DAGs
- **Execution Model**: Temporal provides true durability; Airflow requires manual retry configuration
- **Development**: Temporal enables local testing; Airflow requires more setup
- **Scalability**: Temporal scales individual tasks; Airflow scales entire scheduler

#### vs Dagster
- **Workflow Definition**: Temporal uses native language constructs; Dagster uses custom decorators
- **Error Handling**: Temporal provides automatic retries and failure handling; Dagster requires manual configuration
- **State Persistence**: Temporal handles state automatically; Dagster needs explicit configuration
- **Runtime Model**: Temporal runs distributed by default; Dagster needs additional setup

#### vs Traditional Queue-Based Systems
- **Orchestration**: Temporal handles complex workflows natively; Queue systems need custom orchestration
- **Error Handling**: Temporal provides automatic retries and dead-letter queues; Queue systems need manual implementation
- **Monitoring**: Temporal offers built-in visibility; Queue systems often need external monitoring
- **State Management**: Temporal maintains workflow state; Queue systems require external state storage

### Real-World Use Cases

Temporal.io excels in scenarios like:
- **Microservices Orchestration**: Coordinating multiple service calls
- **Distributed Transactions**: Ensuring consistency across systems
- **Long-Running Processes**: Managing processes that span hours or days
- **Event-Driven Systems**: Handling complex event sequences
- **Approval Workflows**: Managing human-in-the-loop processes

In our image processing pipeline, Temporal.io enables:
1. Parallel processing of tasks with automatic state management
2. Different processing paths based on image type
3. Automatic retries for failed operations
4. Progress tracking through heartbeats
5. Scalable worker deployment
6. Clear visibility into workflow status

## Notes
- Make sure Docker is running if you use the provided Temporal server command
- Each worker needs to be running in its own terminal window
- The system supports custom search attributes and workflow tracking

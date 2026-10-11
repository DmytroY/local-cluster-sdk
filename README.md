# Local Cluster SDK

A lightweight Python SDK for bridging local multi-agent workflows with RAM-booted HPC/LLM infrastructure. This SDK provides a simple interface for executing AI workloads against a local cluster running OpenAI-compatible chat completion endpoints.

## Features

- Execute non-streaming AI workloads on local cluster resources
- Automatic handling of connection timeouts and model swap delays
- Clean exception hierarchy for different failure modes
- OpenAI-compatible payload serialization
- Designed for RAM-constrained environments with configurable timeouts

## Installation

Install the package using pip:

```bash
pip install local-cluster-sdk
```

For development and testing:

```bash
pip install local-cluster-sdk[test]
```

## Quick Start

```python
from local_cluster_sdk import AIClusterClient, AgentWorkload

# Initialize the client (defaults to localhost:11434)
client = AIClusterClient(host="127.0.0.1", port=11434)

# Create a workload
workload = AgentWorkload(
    prompt="Write a Flask health endpoint",
    system_prompt="You are a senior engineer."
)

# Execute the workload
result = client.execute(workload, resource="coder")
print(result)
```

## Configuration

The `AIClusterClient` accepts the following parameters:

- `host` (str): The cluster host address (default: `"127.0.0.1"`)
- `port` (int): The cluster port (default: `11434`)

Network timeouts are preconfigured for RAM-constrained environments:
- Connect timeout: 10 seconds
- Read timeout: 45 seconds

## AgentWorkload

The `AgentWorkload` dataclass represents an AI completion request:

```python
from local_cluster_sdk import AgentWorkload

workload = AgentWorkload(
    prompt="Your user prompt here",
    system_prompt="Optional system prompt",
    temperature=0.2,
    num_ctx=4096
)
```

### Parameters

- `prompt` (str): The user's input prompt
- `system_prompt` (Optional[str]): System instructions for the model
- `temperature` (float): Sampling temperature (default: `0.2`)
- `num_ctx` (int): Context window size (default: `4096`)

## Error Handling

The SDK provides specific exceptions for different failure scenarios:

```python
from local_cluster_sdk import (
    AIClusterClient,
    AgentWorkload,
    ClusterUnreachableError,
    ModelSwapTimeoutError
)

client = AIClusterClient()
workload = AgentWorkload(prompt="Hello")

try:
    result = client.execute(workload, resource="coder")
except ClusterUnreachableError as e:
    print(f"Cluster unreachable: {e}")
except ModelSwapTimeoutError as e:
    print(f"Model swap timeout: {e}")
```

### Exception Hierarchy

- `ClusterSDKError` (base exception)
  - `ClusterUnreachableError`: Raised when the server is down or blocked by firewall
  - `ModelSwapTimeoutError`: Raised when model swapping in limited RAM causes timeout

## Testing

Run the test suite:

```bash
pytest tests/
```

The tests use `requests_mock` to simulate various cluster responses including:
- Successful completions
- Connection timeouts (firewall simulation)
- Read timeouts (RAM swap simulation)

## Requirements

- Python 3.9+
- `requests>=2.31.0`

## License

This project does not currently specify a license.

## Contributing

Contributions are welcome. Feel free to open a pull request.

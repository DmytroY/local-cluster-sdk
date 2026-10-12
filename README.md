# Local Cluster SDK

Local Cluster SDK is a small Python library for sending AI tasks to a local model server.

It is designed for simple use:
- build a request payload
- send it to `/v1/chat/completions`
- read the first answer from the response

This project is useful when you want to run models from a local cluster, or switch to another compatible provider later.

## Install

```bash
pip install git+https://github.com/DmytroY/local-cluster-sdk.git
```

For development:

```bash
git clone https://github.com/DmytroY/local-cluster-sdk.git
cd local-cluster-sdk
pip install -e ".[test]"
```

## Quick start

```python
from local_cluster_sdk import AIClusterClient, AgentWorkload

client = AIClusterClient(host="127.0.0.1", port=11434)

workload = AgentWorkload(
    prompt="Write a Flask health check endpoint",
    system_prompt="You are a senior Python engineer.",
)

result = client.execute(workload, resource="coder")
print(result)
```

## How it works

The client sends a POST request to:

```text
http://{host}:{port}/v1/chat/completions
```

It builds an OpenAI-style JSON payload from `AgentWorkload`.

Example payload:

```python
{
    "model": "coder",
    "messages": [
        {"role": "system", "content": "You are a senior Python engineer."},
        {"role": "user", "content": "Write a Flask health check endpoint"}
    ],
    "temperature": 0.2,
    "options": {
        "num_ctx": 4096
    }
}
```

Then it returns:

```python
data["choices"][0]["message"]["content"]
```

## API

### `AIClusterClient`

```python
from local_cluster_sdk import AIClusterClient

client = AIClusterClient(host="127.0.0.1", port=11434)
```

Parameters:
- `host`: model server host, default is `"127.0.0.1"`
- `port`: model server port, default is `11434`

Method:
- `execute(workload, resource) -> str`

This sends the task and returns the model output as a string.

### `AgentWorkload`

```python
from local_cluster_sdk import AgentWorkload

workload = AgentWorkload(
    prompt="Explain recursion in simple terms",
    system_prompt="You are a teacher.",
    temperature=0.2,
    num_ctx=4096
)
```

Fields:
- `prompt`: the user question
- `system_prompt`: optional system message
- `temperature`: sampling temperature
- `num_ctx`: context window size

## Using other model providers

This SDK is not tied to one provider. It only needs an OpenAI-compatible chat completion endpoint.

That means you can point it to:
- a local Ollama server
- Groq
- OpenRouter
- any other OpenAI-compatible backend

### Local example

```python
from local_cluster_sdk import AIClusterClient, AgentWorkload

client = AIClusterClient(host="127.0.0.1", port=11434)

workload = AgentWorkload(
    prompt="Explain caching in a web app",
    system_prompt="You are a backend engineer.",
)

result = client.execute(workload, resource="llama3.1")
print(result)
```

### Groq example

```python
from local_cluster_sdk import AIClusterClient, AgentWorkload

client = AIClusterClient(host="api.groq.com", port=443)

workload = AgentWorkload(
    prompt="Write a deployment checklist for a Python service",
    system_prompt="You are a DevOps engineer.",
)

result = client.execute(workload, resource="llama-3.1-8b-instant")
print(result)
```

### OpenRouter example

```python
from local_cluster_sdk import AIClusterClient, AgentWorkload

client = AIClusterClient(host="openrouter.ai", port=443)

workload = AgentWorkload(
    prompt="Compare Python async patterns for a web API",
    system_prompt="You are a backend engineer.",
)

result = client.execute(workload, resource="openai/gpt-4o-mini")
print(result)
```

### Switching providers

```python
from local_cluster_sdk import AIClusterClient, AgentWorkload

providers = {
    "local": {"host": "127.0.0.1", "port": 11434},
    "groq": {"host": "api.groq.com", "port": 443},
    "openrouter": {"host": "openrouter.ai", "port": 443},
}

provider = "groq"
config = providers[provider]
client = AIClusterClient(**config)

workload = AgentWorkload(prompt="Explain distributed tracing")
result = client.execute(workload, resource="llama-3.1-8b-instant")
print(result)
```

Note: this SDK currently uses a simple HTTP request and does not add provider-specific authentication or advanced request handling. For providers that need HTTPS or API keys, you may need a small wrapper or client update.

## Error handling

```python
from local_cluster_sdk import (
    AIClusterClient,
    AgentWorkload,
    ClusterUnreachableError,
    ModelSwapTimeoutError,
)

client = AIClusterClient()
workload = AgentWorkload(prompt="Hello")

try:
    result = client.execute(workload, resource="coder")
    print(result)
except ClusterUnreachableError as exc:
    print(f"Cluster unreachable: {exc}")
except ModelSwapTimeoutError as exc:
    print(f"Model swap timeout: {exc}")
```

Exceptions:
- `ClusterSDKError`: base exception
- `ClusterUnreachableError`: server is down or not reachable
- `ModelSwapTimeoutError`: model loading takes too long

## Testing

```bash
pytest tests/
```

The tests cover:
- successful request handling
- connection timeout
- read timeout when model swapping is slow

## Requirements

- Python 3.9+
- `requests>=2.31.0`

## License

This project does not currently specify a license.

## Contributing

Contributions are welcome. Please open a pull request with a small and tested change.

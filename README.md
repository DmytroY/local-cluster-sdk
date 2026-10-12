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

client = AIClusterClient(
    host="192.168.200.23",
    port=11434,
    connect_timeout=2,
    read_timeout=30)
```

 Parameter* | Default value | Type |Description |
|:-:|:-:|:-:|--|
| host | 127.0.0.1 | string | model server host |
| port | 11434 | integer | server port |
| connect_timeout | 10.0 | float | model connection maximum timeout |
| read_timeout | 120.0 | float | model response maximum timeout |


Method:
- `execute(workload, resource) -> str`

where **resource** is your model identificator (name)

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
 Parameter* | Default value | Type |Description |
|:-:|:-:|:-:|--|
| prompt |  | string | required the user question |
| system_prompt |  | string | optional system message |
| temperature | 0.2 | float | sampling temperature |
| read_timeout | 4096 | integer | context window size |

Fields:
- `prompt`: the user question
- `system_prompt`: optional system message
- `temperature`: sampling temperature
- `num_ctx`: context window size

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

Test with mock AI cluster response:
```bash
pytest tests/test_mock_local.py
```

Test with real AI cluster:
```bash
pytest tests\test_real_local.py
```
Note, if you perform test with real AI cluster, do not forget update in **tests\test_real_local.py** paramenters of your real AI cluster:

```                                                    
CORRECT_HOST = "192.168.100.23"
WRONG_HOST = "192.168.99.99"
PORT = 11434
FAST_MODEL = "orchestrator"
SLOW_MODEL = "coder"
```


The tests cover:
- successful request handling
- connection timeout
- read timeout when model swapping is slow

## Requirements
for production:
- Python 3.9+
- requests>=2.31.0

additionaly for testing:
- pytest>=7.0.0
- pytest-mock>=3.10.0

## License

This project does not currently specify a license.

## Contributing

Contributions are welcome. Please open a pull request with a small and tested change.

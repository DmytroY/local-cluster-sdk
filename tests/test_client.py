# local-cluster-sdk/tests/test_client.py
import re
import pytest
import requests
from local_cluster_sdk.client import AIClusterClient
from local_cluster_sdk.models import AgentWorkload
from local_cluster_sdk.exceptions import ClusterUnreachableError, ModelSwapTimeoutError

# ==================== FIXTURES ====================

@pytest.fixture
def client():
    """Initializes a standard test client pointed at your cluster IP."""
    return AIClusterClient(host="192.168.100.23", port=11434)

@pytest.fixture
def workload():
    """Initializes a sample workload payload."""
    return AgentWorkload(
        prompt="Write a Flask health endpoint",
        system_prompt="You are a senior engineer."
    )

# ==================== TEST CASES ====================

def test_execute_success(client, workload, requests_mock):
    """Verifies the SDK successfully parses a standard JSON completion payload."""
    mock_response = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Here is your Flask endpoint..."
                }
            }
        ]
    }
    
    # Use a compiled regex pattern to intercept ANY outbound POST request safely
    any_url_pattern = re.compile(r'.*')
    requests_mock.post(any_url_pattern, json=mock_response, status_code=200)
    
    result = client.execute(workload, resource="coder")
    assert result == "Here is your Flask endpoint..."

def test_execute_firewall_unreachable(client, workload, requests_mock):
    """Simulates an iptables drop rule triggering a connection timeout."""
    any_url_pattern = re.compile(r'.*')
    requests_mock.post(any_url_pattern, exc=requests.exceptions.ConnectTimeout)
    
    with pytest.raises(ClusterUnreachableError) as exc_info:
        client.execute(workload, resource="orchestrator")
        
    assert "Verify your subnet iptables permissions" in str(exc_info.value)

def test_execute_ram_swap_timeout(client, workload, requests_mock):
    """Simulates a model-swapping delay in RAM exceeding the read timeout window."""
    any_url_pattern = re.compile(r'.*')
    requests_mock.post(any_url_pattern, exc=requests.exceptions.ReadTimeout)
    
    with pytest.raises(ModelSwapTimeoutError) as exc_info:
        client.execute(workload, resource="coder")
        
    assert "swapping model binaries in RAM" in str(exc_info.value)
# local-cluster-sdk/tests/test_groq_client.py
import pytest
import requests
from local_cluster_sdk.groq_client import GroqClient, GroqAPIError
from local_cluster_sdk.models import AgentWorkload

@pytest.fixture
def groq_client():
    return GroqClient(api_key="test-api-key")

@pytest.fixture
def workload():
    return AgentWorkload(
        prompt="Write a simple Python function",
        system_prompt="You are a helpful coding assistant"
    )

def test_execute_success(groq_client, workload, requests_mock):
    """Test successful execution with mocked response"""
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "def hello():\n    print('Hello, World!')"
                }
            }
        ]
    }
    
    requests_mock.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=mock_response,
        status_code=200
    )
    
    result = groq_client.execute(workload)
    assert "def hello()" in result

def test_execute_api_error(groq_client, workload, requests_mock):
    """Test handling of API errors"""
    requests_mock.post(
        "https://api.groq.com/openai/v1/chat/completions",
        status_code=401,
        json={"error": {"message": "Invalid API key"}}
    )
    
    with pytest.raises(GroqAPIError):
        groq_client.execute(workload)

def test_execute_network_error(groq_client, workload, requests_mock):
    """Test handling of network errors"""
    requests_mock.post(
        "https://api.groq.com/openai/v1/chat/completions",
        exc=requests.exceptions.ConnectionError
    )
    
    with pytest.raises(GroqAPIError):
        groq_client.execute(workload)

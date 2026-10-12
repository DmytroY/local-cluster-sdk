# local-cluster-sdk/tests/test_real_client.py
import pytest
from local_cluster_sdk.client import AIClusterClient
from local_cluster_sdk.models import AgentWorkload
from local_cluster_sdk.exceptions import ClusterUnreachableError, ModelSwapTimeoutError

# ==================== FIXTURES ====================
# Global configuration                                                                                                                    
CORRECT_HOST = "192.168.100.23"
WRONG_HOST = "192.168.99.99"                                                                                                    
PORT = 11434 
FAST_MODEL = "orchestrator"
SLOW_MODEL = "coder"

@pytest.fixture
def client():
    """Initializes a real test client pointed at the actual cluster."""
    return AIClusterClient(host=CORRECT_HOST, port=PORT)

@pytest.fixture
def workload():
    """Initializes a sample workload payload."""
    return AgentWorkload(
        prompt=f"The user wants a Flask app wich shows current time. Break this down into specific file creation tasks",
        system_prompt="You are project manager."
    )

# ==================== TEST CASES ====================

def test_execute_success(client, workload):
    """Verifies the SDK successfully executes a workload against the real cluster."""
    result = client.execute(workload, resource=FAST_MODEL)
    assert isinstance(result, str)
    assert len(result) > 0

def test_execute_unreachable():
    """Verifies that a ClusterUnreachableError is raised when the cluster is unreachable."""
    client = AIClusterClient(host=WRONG_HOST, port=PORT,connect_timeout=1)
    workload = AgentWorkload(
        prompt="Write a Flask health endpoint",
        system_prompt="You are a senior engineer."
    )
    
    with pytest.raises(ClusterUnreachableError):
        client.execute(workload, resource=FAST_MODEL)

def test_execute_timeout():
    """Verifies that a ModelSwapTimeoutError is raised when the cluster times out."""
    client = AIClusterClient(
        host=CORRECT_HOST,
        port=PORT,
        connect_timeout=5,
        read_timeout=0.001)
    workload = AgentWorkload(
        prompt="Write a Flask health endpoint",
        system_prompt="You are a senior engineer."
    )

    workload = AgentWorkload(                                                                                                             
        prompt="Write a Flask health endpoint",                                                                                           
        system_prompt="You are a senior engineer."                                                                                        
    )                                                                                                                                     
                                                                                                                                          
    with pytest.raises(ModelSwapTimeoutError):                                                                                            
        client.execute(workload, resource=SLOW_MODEL)

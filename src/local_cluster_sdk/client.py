# local-cluster-sdk/src/local_cluster_sdk/client.py
import requests
from typing import Generator
from .models import AgentWorkload
from .exceptions import ClusterUnreachableError, ModelSwapTimeoutError

class AIClusterClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 11434,connect_timeout: float = 10.0, read_timeout: float = 120.0):
        self.base_url = f"http://{host}:{port}"
        self.endpoint = f"{self.base_url}/v1/chat/completions"
        self.network_timeouts = (connect_timeout, read_timeout)

    def execute(self, workload: AgentWorkload, resource: str) -> str:
        """Executes a non-streaming workload on a specified resource target."""
        payload = workload.to_openai_payload(model_name=resource)
        
        try:
            response = requests.post(
                self.endpoint, 
                json=payload, 
                timeout=self.network_timeouts
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
        except requests.exceptions.ConnectTimeout:
            raise ClusterUnreachableError(f"Could not link to cluster at {self.base_url}. Verify your subnet iptables permissions.")
        except requests.exceptions.ReadTimeout:
            raise ModelSwapTimeoutError("The cluster took too long swapping model binaries in RAM. Verify OLLAMA_MAX_LOADED_MODELS configuration.")
        except requests.exceptions.RequestException as e:
            raise ClusterUnreachableError(f"Unexpected underlying communication breakdown: {e}")

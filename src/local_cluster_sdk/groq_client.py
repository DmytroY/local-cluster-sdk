# local-cluster-sdk/src/local_cluster_sdk/groq_client.py
import requests
from typing import Dict
from .models import AgentWorkload
from .exceptions import ClusterSDKError

class GroqAPIError(ClusterSDKError):
    """Raised when there's an error communicating with the Groq API."""
    pass

class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def execute(self, workload: AgentWorkload, model_name: str = "mixtral-8x7b-32768") -> str:
        """Executes a workload using the Groq API."""
        payload = workload.to_openai_payload(model_name=model_name)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self.headers,
                timeout=(10.0, 120.0)
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise GroqAPIError(f"Failed to communicate with Groq API: {e}")

# local-cluster-sdk/src/local_cluster_sdk/openai_client.py
from openai import OpenAI
from .models import AgentWorkload
from .exceptions import ClusterSDKError

class OpenAIClientError(ClusterSDKError):
    """Raised when there's an error communicating with the OpenAI API."""
    pass

class OpenAIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def execute(self, workload: AgentWorkload, model_name: str = "gpt-3.5-turbo") -> str:
        """Executes a workload using the OpenAI API."""
        messages = []
        if workload.system_prompt:
            messages.append({"role": "system", "content": workload.system_prompt})
        messages.append({"role": "user", "content": workload.prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=workload.temperature
            )
            return response.choices[0].message.content
            
        except Exception as e:
            raise OpenAIClientError(f"Failed to communicate with OpenAI API: {e}")

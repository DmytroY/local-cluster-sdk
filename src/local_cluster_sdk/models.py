# local-cluster-sdk/src/local_cluster_sdk/models.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class AgentWorkload:
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.2
    num_ctx: int = 4096
    
    def to_openai_payload(self, model_name: str) -> Dict:
        """Serializes the data into an OpenAI-compatible completion shape."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        
        return {
            "model": model_name,
            "messages": messages,
            "temperature": self.temperature,
            "options": {
                "num_ctx": self.num_ctx
            }
        }

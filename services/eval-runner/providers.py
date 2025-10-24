import os, time, json, base64, requests
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ProviderResp:
    output: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    cost_usd: float
    meta: Dict[str, Any]

class Provider:
    def generate(self, model: str, prompt: str, params: Dict[str, Any]) -> ProviderResp:
        raise NotImplementedError

class OpenAIProvider(Provider):
    def generate(self, model, prompt, params):
        t0 = time.time()
        # TODO: call OpenAI SDK; stub below
        output = f"[openai:{model}] demo-output"
        return ProviderResp(output, 100, 120, int((time.time()-t0)*1000), 0.004, {"provider":"openai","model":model})

class DatabricksProvider(Provider):
    def __init__(self):
        self.host = os.getenv("DATABRICKS_HOST")
        self.token = os.getenv("DATABRICKS_TOKEN")
        self.endpoint = os.getenv("DATABRICKS_MODEL_ENDPOINT")

    def generate(self, model, prompt, params):
        t0 = time.time()
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"inputs": [{"role": "user", "content": prompt}], "params": params}
        # In real call, use requests.post(f"{self.host}{self.endpoint}", json=payload, headers=headers)
        # Here, we stub for offline
        output = f"[databricks:{model}] demo-output"
        return ProviderResp(output, 90, 110, int((time.time()-t0)*1000), 0.003, {"provider":"databricks","model":model})

PROVIDERS = {
    "openai": OpenAIProvider(),
    "databricks": DatabricksProvider(),
}

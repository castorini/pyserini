#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
LLM client supporting OpenAI and vLLM backends via OpenAI-compatible API.

vLLM (https://github.com/vllm-project/vllm) exposes an OpenAI-compatible REST API
so we can reuse the openai Python client with a custom base_url pointing at the
local vLLM server instead of api.openai.com.

Quick start with vLLM:
    # 1. Start a vLLM server (on port 8000 by default):
    #    vllm serve meta-llama/Llama-3.1-8B-Instruct
    #
    # 2. Use LLMClient in Python:
    #    from pyserini.llm import LLMClient
    #    client = LLMClient("meta-llama/Llama-3.1-8B-Instruct", backend="vllm")
    #    response = client.generate([{"role": "user", "content": "Hello!"}])
"""

import os
import time
from typing import Any, Dict, List, Optional, Union

from openai import OpenAI

RETRY_DELAY = 1.0
MAX_RETRIES = 3


class LLMClient:
    """LLM client that supports OpenAI and vLLM backends via the OpenAI-compatible API.

    Parameters
    ----------
    model : str
        Model name to use for generation. For vLLM this is typically the HuggingFace
        model ID (e.g., ``"meta-llama/Llama-3.1-8B-Instruct"``). For OpenAI this is
        the model name (e.g., ``"gpt-4o"``).
    backend : str
        Backend to use. One of:
        - ``"openai"`` – Use the OpenAI API (requires OPENAI_API_KEY env var or api_key).
        - ``"vllm"`` – Use a locally running vLLM server via its OpenAI-compatible API.
        - ``"openai_compatible"`` – Use any OpenAI-compatible endpoint; set base_url
          accordingly.
    api_key : str, optional
        API key. Defaults to the ``OPENAI_API_KEY`` environment variable for OpenAI,
        or ``"EMPTY"`` for vLLM (vLLM doesn't require authentication).
    base_url : str, optional
        Base URL for the API endpoint. Overrides the default per backend. Useful for
        self-hosted or proxy OpenAI-compatible endpoints.
    vllm_port : int
        Port where the vLLM server is running. Used only when ``backend="vllm"`` and
        ``base_url`` is not explicitly provided. Defaults to ``8000``.
    max_tokens : int
        Maximum number of tokens to generate. Defaults to ``1024``.
    temperature : float
        Sampling temperature. Defaults to ``0.0`` (greedy decoding).
    timeout : float
        Request timeout in seconds. Defaults to ``60.0``.
    """

    def __init__(
        self,
        model: str,
        backend: str = 'openai',
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        vllm_port: int = 8000,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        timeout: float = 60.0,
    ):
        self.model = model
        self.backend = backend
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        if backend == 'vllm':
            api_key = api_key or 'EMPTY'
            base_url = base_url or f'http://localhost:{vllm_port}/v1'
        elif backend == 'openai':
            api_key = api_key or os.getenv('OPENAI_API_KEY', '')
            # base_url stays None → points to api.openai.com
        elif backend == 'openai_compatible':
            api_key = api_key or os.getenv('OPENAI_API_KEY', '')
            # caller must supply base_url
        else:
            raise ValueError(
                f"Unknown backend '{backend}'. Choose from: 'openai', 'vllm', 'openai_compatible'."
            )

        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Send a chat request and return the generated text.

        Parameters
        ----------
        messages : list of dict
            Conversation in OpenAI format, e.g.::

                [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",   "content": "What is the capital of France?"},
                ]

        max_tokens : int, optional
            Override the instance-level ``max_tokens`` for this call.
        temperature : float, optional
            Override the instance-level ``temperature`` for this call.

        Returns
        -------
        str
            The model's response text.

        Raises
        ------
        RuntimeError
            If all retry attempts are exhausted.
        """
        _max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        _temperature = temperature if temperature is not None else self.temperature

        last_error: Optional[Exception] = None
        for attempt in range(MAX_RETRIES):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=_max_tokens,
                    temperature=_temperature,
                    timeout=self.timeout,
                )
                content = completion.choices[0].message.content
                return content if content is not None else ''
            except Exception as exc:
                last_error = exc
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)

        raise RuntimeError(
            f'LLM generation failed after {MAX_RETRIES} attempts. '
            f'Last error: {last_error}'
        )

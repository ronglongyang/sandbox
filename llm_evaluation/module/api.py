from typing import Any, Dict


class LLM:
    def __init__(
        self,
        model: str,
        api_token: Any,
    ):
        self.model = model
        if "llama" in self.model:
            from llamaapi import LlamaAPI
            self.client = LlamaAPI(api_token)
        else:
            raise Exception("Model type not supported")

    def template(
        self,
        sys_prompt: str,
        user_prompt: str,
        # todo max_tokens temperature ...
    ) -> Dict[str, str]:
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

    def __call__(self, sys_prompt, user_prompt) -> Dict:
        return self.client.run(self.template(sys_prompt, user_prompt)).json()['choices'][0]['message']

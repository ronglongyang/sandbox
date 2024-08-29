from typing import Union, List

# from llm_evaluation.module.data import fetch_dataset
from llm_evaluation.module.api import LLM
from llm_evaluation.module.prompts.evaluation import evaluate_prompt
from llm_evaluation.module.datatypes import GenerationInput

LLAMA_API_KEY = ...
llm = LLM("llama-70b-chat", LLAMA_API_KEY)


def generate_handler(
    user_prompt: str,
    instruction: str,
    input_text: Union[str, List[dict]],
) -> str:
    user_prompt = user_prompt.replace("{{instruction}}", instruction)
    user_prompt = user_prompt.replace("{{input}}", str(input_text))
    return user_prompt


def experiment():
    instruction = "Given a piece of scientific information, write an example that can help a young child understood the concept."  # noqa
    input_text = "For example, sleep is important for the production of certain hormones, such as the growth hormone, which, among other things, stimulates the regeneration of damaged and dying cells."  # noqa

    user_prompt_1 = """[instruction]
{{instruction}} Ensure that the examples are simple enough for even 8 years old to understood.

[Scientific Explanation]
{{input}}"""
    g1 = GenerationInput(
        input_text=input_text,
        instruction=instruction,
        sys_prompt="Your are a smart and friendly teacher.",
        user_prompt=user_prompt_1,
    )
    user_prompt_2 = """instruction: "{{instruction}}"
Explanation: "{{input}}" """
    g2 = GenerationInput(
        input_text=input_text,
        instruction=instruction,
        sys_prompt="Your are a helpful assistant.",
        user_prompt=user_prompt_2,
    )

    criteria = [
        {"name": "Simplicity", "description": "Does the example use only simple language by avoiding complex words/sentences, and presents situations or actions that a young child would be able to relate to?"},  # noqa
        {"name": "Faithfulness", "description": "The summary is devoid of factual errors, where a factual error is a statement that contradicts the source document, or is not directly stated, heavily implied, or logically entailed by the source document."},  # noqa
    ]

    output1 = llm(g1.sys_prompt, generate_handler(g1.user_prompt, g1.instruction, g1.input_text))["content"]
    output2 = llm(g2.sys_prompt, generate_handler(g2.user_prompt, g2.instruction, g2.input_text))["content"]
    print(output1)
    print(output2)
    prompt_dict = evaluate_prompt(instruction, input_text, output1, output2, criteria)
    output_ = llm(prompt_dict["system"], prompt_dict["user"])["content"]
    print(output_)


if __name__ == "__main__":
    experiment()

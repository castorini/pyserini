import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion

from pyserini.demo.aclchatgpt.skill import PyseriniSkill

kernel = sk.Kernel()

api_key, org_id = sk.openai_settings_from_dot_env()
kernel.add_text_completion_service("dv", OpenAITextCompletion("text-davinci-003", api_key, org_id))

kernel.import_skill(PyseriniSkill(),"pyserini")


sk_prompt = """
ChatBot can answer questions based on query_results.
It can only answer questions based on query_results.
If query_results is empty, say "I don't know"

============
query_results: {{pyserini.search $input}}
============

{{$input}}
"""



context = kernel.create_new_context()
context["url"] = "http://127.0.0.1:8080/search"

acl_chat_function = kernel.create_semantic_function(sk_prompt, max_tokens=200, temperature=0, top_p=0.5)


def chat(input_text: str) -> None:
    # Save new message in the context variables


    # Process the user message and get an answer
    answer = acl_chat_function(input_text,context=context)

    # Show the response
    print(f"ChatBot: {answer}")


while True:
    chat(input("User: "))
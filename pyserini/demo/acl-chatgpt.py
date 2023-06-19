import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion, AzureTextCompletion

from pyserini.demo.skill import PyseriniSkill

kernel = sk.Kernel()

api_key, org_id = sk.openai_settings_from_dot_env()
kernel.add_text_completion_service("dv", OpenAITextCompletion("text-davinci-003", api_key, org_id))

kernel.import_skill(PyseriniSkill(),"pyserini")


sk_prompt = """
{{pyserini.search $input}}

Based on the information provided above, please answer the following question:

{{$input}}
"""

context = kernel.create_new_context()
context["url"] = "http://127.0.0.1:8080/search"

acl_function = kernel.create_semantic_function(sk_prompt, max_tokens=200, temperature=0, top_p=0.5)

print(acl_function("Tell me about the Computational Power of Transformers and Its Implications in Sequence Modeling", context=context))
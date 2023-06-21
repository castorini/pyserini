import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion

from pyserini.demo.aclchatgpt.skill import PyseriniSkill

kernel = sk.Kernel()

api_key, org_id = sk.openai_settings_from_dot_env()
kernel.add_text_completion_service("dv", OpenAITextCompletion("text-davinci-003", api_key, org_id))

kernel.import_skill(PyseriniSkill(),"pyserini")




acl_chat_prompt = """
Given the `query_results` below, your task is to formulate an answer using only the information 
provided in these results. You should not draw from other sources or attempt to provide information that is not 
contained within the `query_results`. If the `query_results` are empty, simply state "I'm sorry, but I do not have 
enough information to provide an answer."

===================
query_results: {{pyserini.search $input}}
===================

Based on the above `query_results`, what is your response to {{$input}}?
"""

absolute_question_prompt = """
Task: You are an AI language model tasked with transforming given questions into 
absolute questions. An absolute question is a question that can stand on its own and carries all the context needed 
to be answered. Here's an example:

User: Who is Alan Turing?
ChatBot: Who is Alan Turing?
User: How old is he?
ChatBot: How old is Alan Turing?

===================
History: {{$history}}
===================

Using the history as context, transform the following question into an absolute question: {{$input}}
"""


context = kernel.create_new_context()
context["url"] = "http://127.0.0.1:8080/search"
context["history"] = ""

acl_chat_function = kernel.create_semantic_function(acl_chat_prompt, max_tokens=200, temperature=0, top_p=0.5)
absolute_question_function = kernel.create_semantic_function(absolute_question_prompt, max_tokens=200, temperature=0, top_p=0.5)


def chat(input_text: str) -> None:

    print("---------------------------------------------")
    absolute_question = absolute_question_function(input_text,context=context)

    print (f"Absolute Question: {absolute_question}")

    # Process the user message and get an answer
    answer = acl_chat_function(str(absolute_question),context=context)

    # Show the response
    print(f"ChatBot: {answer}")

    context["history"] += f"\nUser: {input_text}\nChatBot: {answer}\n"


while True:
    print("=============================================")
    chat(input("User: "))
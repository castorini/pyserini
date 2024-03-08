from dataclasses import dataclass
from argparse import ArgumentParser
from typing import Optional

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion

from pyserini.demo.aclchatgpt.skill import PyseriniSkill, PyseriniConfig


@dataclass
class OpenAIConfig:
    api_key: str
    org_id: str

class ChatBot:

    acl_chat_prompt = """Given the query_results below, your task is to formulate an answer. You may choose to use or not to use the 
    information in the query_results.
    If you use the query_results, you must reference the docid of the document used by appending to the answer with "(docid: doc-id-here)".
    If you do not use the query_results, do not reference it in your answer.
    
    ===================
    query_results: {{pyserini.search $input}}
    ===================
    
    What is your response to {{$input}}?
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

    def __init__(self, pyserini_config: PyseriniConfig, openai_config: OpenAIConfig):

        self.kernel = sk.Kernel()
        self.kernel.add_text_completion_service("dv", OpenAITextCompletion("text-davinci-003", openai_config.api_key, openai_config.org_id))
        self.kernel.import_skill(PyseriniSkill(pyserini_config),"pyserini")
        self.context = self.kernel.create_new_context()
        self.context["url"] = "http://127.0.0.1:8080/search"
        self.context["history"] = ""

        self.acl_chat_function = self.kernel.create_semantic_function(self.acl_chat_prompt, max_tokens=200, temperature=0, top_p=0.5)
        self.absolute_question_function = self.kernel.create_semantic_function(self.absolute_question_prompt, max_tokens=200, temperature=0, top_p=0.5)


    def _chat(self,input_text: str) -> None:

        print("---------------------------------------------")
        absolute_question = self.absolute_question_function(input_text,context=self.context)

        print (f"Absolute Question: {absolute_question}")

        # Process the user message and get an answer
        answer = self.acl_chat_function(str(absolute_question),context=self.context)

        # Show the response
        print(f"ChatBot: {answer}")

        self.context["history"] += f"\nUser: {input_text}\nChatBot: {answer}\n"

    def chat(self) -> None:
        print("Hi, I'm the ACL ChatBot. Ask me a question about ACL Anthology papers and I'll do my best to answer it.")

        while True:
            print("=============================================")
            self._chat(input("User: "))

def main():

    parser = ArgumentParser()

    parser.add_argument('--k1', type=float, help='BM25 k1 parameter.')
    parser.add_argument('--b', type=float, help='BM25 b parameter.')
    parser.add_argument('--hits', type=int, default=10, help='Number of hits returned by the retriever')

    args = parser.parse_args()
    api_key, org_id = sk.openai_settings_from_dot_env()
    open_ai_config = OpenAIConfig(api_key,org_id)
    pyserini_config = PyseriniConfig(args.k1, args.b, args.hits)

    print("Starting ChatBot...")

    chatbot = ChatBot(pyserini_config=pyserini_config,openai_config=open_ai_config)
    chatbot.chat()




if __name__ == '__main__':
    main()
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.providers.openai import OpenAIProvider

INSTRUCTIONS = """
You are a helpful assistant with information retrieval capabilities.
ALWAYS use tools to retrieve relevant documents.
Think about whether the user is asking an indepth or complicated question, and if so, use the retrieve and rerank tool to get the most relevant results. 
For example, if the user asks for deep research on a topic, use the retrieve and rerank tool.
Otherwise, use the search tool. 
The default value of the dataset for the tools to retrieve over is msmarco-v2.1-doc-segmented, which is designed for retrieval augmented generation for LLMs like you.
So you don't need to specify an alternative index unless for good reason.
Use the get document tool only when you have a document id but no document.
The search and retrieve and rerank tool both return the raw contents of documents, so there's no need to use the get document tool on the ids returned from these tools.
Use the retrieved results to formulate a cohesive response and cite document IDs where you used them in your response. 
"""

local_model = OpenAIResponsesModel(
    "openai/gpt-oss-20b", 
    provider=OpenAIProvider(    
        base_url="http://localhost:6000/v1", 
        api_key="foo"
    )
)

server = MCPServerStreamableHTTP('http://localhost:8000/mcp')  
agent = Agent(local_model, toolsets=[server], instructions=INSTRUCTIONS, retries=5)
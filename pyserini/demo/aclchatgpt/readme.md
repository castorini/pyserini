# Talking to ACL Anthology with GPT

By default, GPT-3 text-davinci-003 is used. You can change this in `chatbot.py`.

## Environment Varaibles
You will need to create an `.env` file in directory that you are running in.
The `.env` file should contain the following:
```
OPENAI_API_KEY="<your key>"
OPENAI_ORG_ID="<your org id>"
```

## Setup

1. Follow the instructions in [Indexing the ACL Anthology with Anserini](https://github.com/castorini/pyserini/blob/master/docs/working-with-acl-anthology.md) to setup the project and generate a `lucene-index-acl-paragraph` index.
2. Copy the generated `lucene-index-acl-paragraph` index from the `acl-anthology` folder to `pyserini/indexes`
3. You will need Semantic Kernel as well. 
   - `pip3 install --upgrade semantic-kernel`
4. Start the chatbot with `python -m pyserini.demo.aclchatgpt.chatbot`
5. Start chatting!
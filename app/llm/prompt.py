from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

chat_with_docs_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question}

Context: {context}

Answer: """
chat_with_prompt = """You are an assistant for question-answering tasks. 

Question: {question} 

Answer: """


chat_with_exam = """
"You are an assistant for question-answering tasks. Based on the provided question and exam materials, answer the following:

Question: {question}

Exam: {exam}

Your Answer:"
"""

# chat_with_history_prompt = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

# Current conversation:
# {history}
# Human: {input}
# AI Assistant:"""

# chat_with_history_prompt = ChatPromptTemplate(
#     messages=[
#         SystemMessagePromptTemplate.from_template(
#             "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."
#         ),
#         # The `variable_name` here is what must align with memory
#         MessagesPlaceholder(variable_name="chat_history"),
#         HumanMessagePromptTemplate.from_template("{question}")
#     ]
# )


chat_with_history_prompt = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. You are provided with information about entities the Human mentions, if relevant.

Current conversation:
{chat_history}

Conversation:
Human: {input}

Output Just the string of response
"""
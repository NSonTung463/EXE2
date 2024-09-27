import asyncio

from app.features.chat.model import ChatMessage, ModelName
from app.llm.llm_selector import LLMSelector
from app.llm.prompt import chat_with_docs_prompt,chat_with_history_prompt, chat_with_prompt
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate


from loguru import logger



class Chat:
    def __init__(self, model_name: ModelName = ModelName.GEMINI):
        self.selector = LLMSelector()
        self.llm = self.selector.get_llm(model_name.value)  # Sử dụng giá trị của Enum
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
    def invoke(self, data: ChatMessage) -> str:
        prompt = chat_with_prompt.format(question=data.question)
        response = self.llm.invoke(prompt)
        return response.content

    def stream(self, data: ChatMessage) -> str:
        prompt = chat_with_prompt.format(question=data.question)
        return self.llm.stream(prompt)
    
    def get_llm(self, model_name):
        self.llm = self.selector.get_llm(model_name.value)  
        logger.info(f"Model changed to: {model_name.value}")
    
    def chat_with_history(self,input: str)  -> str:
        prompt = PromptTemplate(input_variables=["chat_history", "input"], template=chat_with_history_prompt)
        conversation = ConversationChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
            memory=self.memory,
        )
        result = conversation.invoke({"input": input})
        return result.get("response")

    def chat_with_doc(self,query_text: str, context_text: str)  -> str:
        prompt_template = ChatPromptTemplate.from_template(chat_with_docs_prompt)
        prompt = prompt_template.format(context=context_text, question=query_text)
        response = self.llm.invoke(prompt)
        return response.content
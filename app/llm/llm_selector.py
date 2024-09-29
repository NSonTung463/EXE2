# from langchain_experimental.llms import ChatLlamaAPI
# from llamaapi import LlamaAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_openai.chat_models import AzureChatOpenAI

from app.settings import AzureOpenAIGPT4
from langchain_groq import ChatGroq
from langchain_anthropic import AnthropicLLM,Anthropic

import os
from dotenv import load_dotenv
from app.settings import AzureOpenAIGPT4

# Load environment variables
load_dotenv()

class LLMSelector:
    def __init__(self):
        self.llama_api_key = os.getenv("LLAMA_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    def get_llm(self, option: str):
        if option == None:
            return
        
        # elif option == "llama":
        #     llama = LlamaAPI(self.llama_api_key)
        #     llm_llama = ChatLlamaAPI(client=llama)
        #     return llm_llama
        
        elif option == "openai":
            llm_openai = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=self.openai_api_key)
            return llm_openai
        
        elif option == "groq":
            llm_groq = ChatGroq(
                temperature=0.5,
                model_name="mixtral-8x7b-32768",
                groq_api_key=self.groq_api_key
            )
            return llm_groq
        
        elif option == "gemini":
            llm_gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=self.google_api_key)
            return llm_gemini
        
        elif option == "azure_openai":
            llm_azure = AzureChatOpenAI(
                **AzureOpenAIGPT4().__dict__,
                temperature=0,
            )
            return llm_azure
        
        elif option == "anthropic2":
            llm_anthropic2 = AnthropicLLM(model='claude-2.1', anthropic_api_key=self.anthropic_api_key)
            return llm_anthropic2
        
        elif option == "anthropic3":
            llm_anthropic3 = Anthropic(model='claude-3-sonnet-20240229', anthropic_api_key=self.anthropic_api_key)
            return llm_anthropic3
        
        else:
            raise ValueError(f"Unknown LLM option: {option}")

# Usage example
selector = LLMSelector()
llm = selector.get_llm("gemini")
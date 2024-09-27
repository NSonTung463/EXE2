from langchain_openai.chat_models import AzureChatOpenAI
from app.settings import AzureOpenAIGPT4

llm = AzureChatOpenAI(
    **AzureOpenAIGPT4().__dict__,
    temperature=0,
)

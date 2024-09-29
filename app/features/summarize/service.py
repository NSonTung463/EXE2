from app.features.summarize.model import SUMARIZE_QUESTION
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from app.features.search.service import DocumentSearch
from.prompt import summarizes_task_prompt
from app.llm.llm_selector import llm
class Sumarizer:
    def __init__(self,llm=llm):
        super().__init__()
        self.model = llm
        self.search = DocumentSearch()
    def retrivial_data(self):
        retrivial_infor=[]
        for question_retrivial in SUMARIZE_QUESTION['list_retrivial_questions']:
            infor = self.search.db.similarity_search(question_retrivial.get("question"), k=10)
            infor = [x.page_content for x in infor]
            retrivial_infor.extend(infor)
        retrivial_infor = list(set(retrivial_infor))
        exam_information = ".\\n".join(list(set(retrivial_infor)))
        return exam_information
    def run(self,exam_information):
        promtp = summarizes_task_prompt.format(exam_information=exam_information)
        response = self.model.invoke(promtp)
        return response.content
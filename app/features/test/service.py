from app.features.test.prompt import create_test_prompt
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from app.features.search.service import DocumentSearch
from app.features.summarize.service import Sumarizer
from app.llm.llm_selector import llm

class CreateExam:
    def __init__(self,llm=llm):
        super().__init__()
        self.model = llm
        self.search = DocumentSearch()
        self.summarize  = Sumarizer(llm=self.model)
    def run(self):
        exam_information = self.summarize.retrivial_data()
        summary_content = self.summarize.run(exam_information)
        prompt = create_test_prompt.format(exam_information=exam_information,summary_information=summary_content)
        response = self.model.invoke(prompt)
        return response.content
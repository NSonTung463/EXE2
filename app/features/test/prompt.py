create_test_prompt = """
"Given the provided exam information:
<exam_information>
{exam_information}
</exam_information>

And a summary of its content:
<summary_information>
{summary_information}
</summary_information>

Create a new, customized test in the same language as the provided exam information. Maintain the original exam's format, question types, and difficulty level. However, adapt the content to a different topic, ensuring it aligns with the overall theme and scope of the original exam."

### Additional Considerations:
* **Topic Selection:** Choose a topic that is relevant to the original exam's subject area or broader field.
* **Content Alignment:** Ensure the new content matches the depth and complexity of the original exam questions.
* **Question Variety:** Maintain a balance of question types (e.g., multiple choice, short answer, essay) to assess different skills.
* **Instruction Clarity:** Provide clear and concise instructions for each question to avoid confusion.
By following these guidelines, you can effectively create a customized test that accurately reflects the original exam's structure and difficulty while addressing a new topic.
Remember, when generating questions for the test, make sure you know the answers and put them, the answers are at the end of the test.
Concise answer key: At the end of the exam, provide a concise answer key using the question number and corresponding letter of the correct answer (e.g., 1c, 2b, 3a, 4d).
"""
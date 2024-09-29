import time
import os
import joblib
import streamlit as st
import requests
from app.features.chat.service import Chat
from app.features.chat.model import ChatMessage, ModelName
# from app.llm.azure_openai_client import azure_chat_openai_4
from loguru import logger
from app.llm.prompt import chat_with_exam
if 'chat_instance' not in st.session_state:
    st.session_state.chat_instance = Chat()

chat = st.session_state.chat_instance
question_exam  = True
forget_gate = 0
# Thiết lập cấu hình ban đầu
new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'
URL_TEST_RETRIEVE = "http://localhost:8080/api/v1/chat/chat"
URL_UPLOAD_FILE = "http://localhost:8080/api/v1/index/index"
URL_CREATE_EXAM = "http://localhost:8080/api/v1/create_exam/creat_exam"

# Tạo thư mục data/ nếu chưa có
if not os.path.exists('data/'):
    os.mkdir('data/')

# Load các cuộc trò chuyện trước đó (nếu có)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar hiển thị danh sách các cuộc trò chuyện cũ và tính năng tải file lên
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
    # Tính năng tải file lên
    st.write('# Upload File')
    uploaded_file = st.file_uploader("Choose a file to upload", type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        logger.info(f"1")
        try:
            logger.info(f"2")
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post("http://localhost:8080/api/v1/index/index", files=files)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            st.success("File uploaded and indexed successfully!")
        except requests.exceptions.HTTPError as e:
            logger.info(f"3")
            if e.response.status_code == 403:
                st.error("Permission denied. Please check your credentials or access rights.")
            else:
                st.error(f"Failed to upload and index the file. Status code: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.info(f"4")
            st.error(f"An error occurred while uploading the file: {str(e)}")
    
    # Thêm nút Create Exam
    if st.button("Create Exam"):
        try:
            response = requests.post(URL_CREATE_EXAM)
            response.raise_for_status()
            exam_data = response.json()["data"]
            current_exam = exam_data
            
            # Ensure the directory exists before saving
            os.makedirs('local_files', exist_ok=True)
            
            # Save exam data to a local file
            with open('local_files/exam_data.txt', 'w') as f:
                f.write(exam_data)
            
            st.success("Exam created successfully and saved locally!")
            st.markdown(exam_data)  # Use markdown to render the exam content
            question_exam = True
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while creating the exam: {str(e)}")
        except IOError as e:
            st.error(f"An error occurred while saving the exam data locally: {str(e)}")

    # Hiển thị nội dung của file exam_data.txt sau mỗi lần chạy
    if os.path.exists('local_files/exam_data.txt'):
        with open('local_files/exam_data.txt', 'r') as f:
            exam_content = f.read()
        st.markdown("## Current Exam Content")
        st.markdown(exam_content)

default_model = ModelName.GEMINI

# Khởi tạo session_state nếu chưa có
if 'previous_model' not in st.session_state:
    st.session_state.previous_model = default_model.name

selected_model = st.sidebar.selectbox(
    "Choose a language model",
    options=[model.name for model in ModelName],
    index=list(ModelName).index(default_model)
)

selected_model_enum = ModelName[selected_model]  # Chuyển đổi tên mô hình thành Enum
st.write(f"Selected model: {selected_model_enum.value}")

# Tải lịch sử chat nếu có
if os.path.exists(f'data/{st.session_state.chat_id}-st_messages'):
    try:
        st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
    except Exception as e:
        st.error(f"Failed to load chat history: {e}")
        st.session_state.messages = []
else:
    st.session_state.messages = []

# Hiển thị các tin nhắn từ session_state
if st.session_state.messages:
    for message in st.session_state.messages:
        with st.chat_message(name=message['role'], avatar=message.get('avatar')):
            st.markdown(message['content'])
else:
    st.write("No chat history available.")

# Xử lý input từ người dùng
if question := st.chat_input('Your message here...'):
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')

    # Hiển thị tin nhắn của người dùng
    with st.chat_message('user'):
        st.markdown(question)

    # Kiểm tra và thay đổi mô hình nếu cần
    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        if selected_model != st.session_state.previous_model:
            logger.info(f"Model change from {st.session_state.previous_model} to {selected_model}")
            chat.get_llm(ModelName[selected_model])
            st.write("Model changed!")
            st.session_state.previous_model = selected_model

        # Gọi hàm để nhận phản hồi từ mô hình
        if 'forget_gate' not in st.session_state:
            st.session_state.forget_gate = 0

        if question_exam == True:
            with open('local_files/exam_data.txt', 'r') as f:
                exam_content = f.read()
            question_exam = chat_with_exam.format(question=question, exam=exam_content)
            response_data = chat.chat_with_history(input=question_exam)
            question_exam = False
            st.session_state.forget_gate = 0
        else:
            st.session_state.forget_gate += 1
            response_data = chat.chat_with_history(input=question)
        st.markdown(response_data)
        
        if st.session_state.forget_gate == 5:
            question_exam = True
    # Lưu tin nhắn vào session_state và file
    st.session_state.messages.append(dict(role='user', content=question))
    st.session_state.messages.append(dict(role=MODEL_ROLE, content=response_data, avatar=AI_AVATAR_ICON))

    try:
        joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    except Exception as e:
        st.error(f"Failed to save chat messages: {e}")

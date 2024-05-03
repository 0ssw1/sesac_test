import streamlit as st
import time
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate

def get_gpt(prompt):
    chat_prompt = ChatPromptTemplate.from_messages(st.session_state['context_gpt'])
    user_prompt = chat_prompt.format_messages(prompt=prompt)
    gpt = ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo', openai_api_key=st.secret['API_KEY'])
    
    return gpt.invoke(user_prompt).content


if 'context' not in st.session_state:
    st.session_state['context'] = []
if 'context_gpt' not in st.session_state:
    st.session_state['context_gpt'] = [("system","너는 지금부터 영화 터미네이터의 나쁜 인공지능 로봇 역할을 해야한다.")]

prompt = st.chat_input("여기에 프롬프트를 입력해보세요.")
messages = st.container()
for msg in st.session_state['context']:
    if msg["type"] == "user":
        messages.chat_message("user", avatar="👦").write(msg["content"])
    elif msg["type"] == "assistant":
        messages.chat_message("assistant", avatar="https://archivenew.vop.co.kr/images/95d771bbaba40c7d57e7517e846368ad/2014-12/04113346_32.jpg").write(msg["content"])

if prompt:
    messages.chat_message("user", avatar="👦").write(prompt)
    st.session_state['context'].append({'type':'user', 'content':prompt})
    st.session_state['context_gpt'].append(("human",prompt))

    result = get_gpt(prompt)
    st.session_state['context'].append({'type':'assistant', 'content':result})
    st.session_state['context_gpt'].append(("ai",result))

    st.rerun()
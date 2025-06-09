import streamlit as st
from chains.final_chain import final_chain
from dotenv import load_dotenv, find_dotenv
from utils.st_utils import setup_sidebar
from utils.db import load_history_from_db, clear_db_history

load_dotenv(find_dotenv())

st.set_page_config(page_title="Clash of Clans Assistant", layout="wide", page_icon="🤖")

st.title("🤖 Assistente de Clash of Clans")

if "session_id" not in st.session_state:
  st.session_state.session_id = 'Anônimo'
  
if "history" not in st.session_state:
  st.session_state.history = load_history_from_db(st.session_state.session_id)

with st.sidebar:
  name_changed = st.text_input("Digite seu nome de jogador:", key="username", value=st.session_state.session_id)
  if name_changed != st.session_state.session_id:
    st.session_state.session_id = name_changed
    st.session_state.history = load_history_from_db(name_changed)
    st.rerun()

  if st.session_state.history:
    st.title(f"🕘 Histórico de Conversa - {st.session_state.session_id}")
    history_title = f"• Título: {st.session_state.history[0]['user'][0:50]}{'...' if len(st.session_state.history[0]['user']) > 50 else ''}"
    st.write(history_title)
    
    if st.button("🗑️ Limpar histórico", use_container_width=True):
      st.session_state.history.clear()
      clear_db_history(st.session_state.session_id)
      st.rerun()

user_input = st.chat_input("Digite sua pergunta...")

if st.session_state.history:
  for msg in st.session_state.history:
    st.chat_message("user").write(msg["user"])
    st.chat_message("assistant").write(msg["bot"])

if user_input:
  st.chat_message("user").write(user_input)

  with st.chat_message("assistant"):
    response_stream = final_chain.stream(
      {"user_message": user_input},
      config={"configurable": {"session_id": st.session_state.session_id}}
    )

    collected_chunks = []

    def stream_and_collect():
      for chunk in response_stream:
        collected_chunks.append(chunk)
        yield chunk.content

    st.write_stream(stream_and_collect())
    
    full_response = ''.join(chunk.content for chunk in collected_chunks)
    st.session_state.history.append({"user": user_input, "bot": full_response})
    st.rerun()

setup_sidebar()

import streamlit as st
from chains.final_chain import final_chain
from dotenv import load_dotenv, find_dotenv
from utils.st_utils import setup_sidebar
from utils.db import load_history_from_db, clear_db_history
import tempfile
from PIL import Image
import os

load_dotenv(find_dotenv())

os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = os.getenv("STREAMLIT_SERVER_MAX_UPLOAD_SIZE", "2")

st.set_page_config(page_title="Clash of Clans Assistant", layout="wide", page_icon="🤖")

st.title("🤖 Assistente de Clash of Clans")

if "session_id" not in st.session_state:
  st.session_state.session_id = 'Anônimo'
  
if "history" not in st.session_state:
  st.session_state.history = load_history_from_db(st.session_state.session_id)
  
if "upload_key" not in st.session_state:
  st.session_state.upload_key = 0

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

uploaded_file = st.file_uploader("📷 Envie uma imagem da vila", type=["jpg", "jpeg", "png"], key=st.session_state.upload_key)

user_input = st.chat_input("Digite sua pergunta...")

if st.session_state.history:
  for msg in st.session_state.history:
    st.chat_message("user").write(msg["user"])
    st.chat_message("assistant").write(msg["bot"])
    
if user_input:
  st.chat_message("user").write(user_input)

  image_path = None

  if uploaded_file:
    if uploaded_file.size > 2 * 1024 * 1024:
      st.error("O arquivo enviado é muito grande. Por favor, envie uma imagem de até 2MB.")
      st.stop()
      
    user_message = f'Imagem enviada: {uploaded_file.name}'
    bot_message = "Processando a imagem..."
      
    st.chat_message("user").write(user_message)
    st.chat_message("bot").write(bot_message)
    
    st.session_state.history.append({
      "user": user_message,
      "bot": bot_message
    })
    
    image = Image.open(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
      image.save(tmp.name)
      image_path = tmp.name

  with st.chat_message("assistant"):
    input_data = {"user_message": user_input}
    if image_path:
      input_data["image_path"] = image_path

    response_stream = final_chain.stream(
      input_data,
      config={"configurable": {"session_id": st.session_state.session_id}}
    )

    collected_chunks = []

    def stream_and_collect():
      for chunk in response_stream:
        collected_chunks.append(chunk)
        yield chunk.content

    st.write_stream(stream_and_collect())

    full_response = ''.join(chunk.content for chunk in collected_chunks)
    st.session_state.history.append({
      "user": user_input,
      "bot": full_response
    })

    if image_path and os.path.exists(image_path):
      os.remove(image_path)
      st.session_state.upload_key += 1

    st.rerun()

setup_sidebar()

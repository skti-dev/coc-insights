import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.st_utils import setup_sidebar

st.set_page_config(page_title="Avisos importantes", page_icon="⚠️", layout="wide")

st.title("⚠️ Avisos importantes")

st.markdown("""
- O conteúdo apresentado na aplicação pode conter erros, inconsistências ou estar desatualizado.
- As informações foram extraídas de fontes públicas e podem não refletir a realidade atual do jogo.
- As URLs podem mudar ou ficar indisponíveis com o tempo.
- As respostas geradas pelo assistente são baseadas nessas fontes, mas não são garantidas como 100% precisas.
- Não é recomendado utilizar essas informações para fins competitivos ou de tomada de decisão no jogo.
- O uso das respostas geradas é de responsabilidade do usuário.
- O assistente não é afiliado oficialmente ao Clash of Clans ou Supercell.
- O intuito dessa aplicação é educacional e não deve ser utilizada para fins comerciais.
""")

setup_sidebar()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

filter_cv_data_llm = ChatOpenAI(model="gpt-4o", temperature=0)

filter_cv_data_prompt = ChatPromptTemplate.from_template(
  '''
  Você é um assistente que recebe uma grande base de dados e uma pergunta sobre o jogo Clash of Clans.

  Sua função é extrair apenas os dados estritamente relevantes para responder à pergunta, ignorando tudo que não for necessário.

  ### Pergunta:
  {user_message}

  ### Dados disponíveis (base completa):
  {cv_data}

  ### Instruções:
  - Retorne somente um dicionário JSON com as partes da base relevantes.
  - Se a pergunta for muito geral, retorne apenas os campos principais.
  - Não invente dados que não estão na base.

  Responda apenas com JSON válido.
  '''
)

filter_cv_data_chain = filter_cv_data_prompt | filter_cv_data_llm

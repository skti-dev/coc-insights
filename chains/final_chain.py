from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from chains.news import news_chain
from chains.main_cv import main_cv_chain
from chains.fallback import fallback_chain
from chains.strategy import strategy_chain
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chains.news import news_chain
from chains.main_cv import main_cv_chain
from chains.fallback import fallback_chain
from chains.strategy import strategy_chain

chat = ChatOpenAI(model='gpt-4o-mini', temperature=0)

store = {}
def get_by_session_id(session_id):
  if session_id not in store:
    store[session_id] = InMemoryChatMessageHistory()
  return store[session_id]

attack_strategy = 'estrategia de ataque'
cv_info = 'informacoes do CV'
update = 'atualizacoes'
others = 'outros'

category_prompt = ChatPromptTemplate.from_messages([
  MessagesPlaceholder("history"),
  ("system", f'''Categorias disponíveis:
  - "{attack_strategy}": Perguntas relacionadas a estratégias de ataque, tropas usadas, ordem de ataque, etc.
  - "{cv_info}": Perguntas sobre tropas, defesas, heróis ou feitiços específicos de cada centro de vila (CV).
  - "{update}": Perguntas sobre atualizações, eventos, novidades ou notícias do jogo.
  - "{others}": Qualquer outra pergunta que não se encaixe nas categorias acima.

  Alguns exemplos de palavras associadas à categoria "{update}": evento, evento sazonal, novidade, atualização, patch, mudanças, lançamento, manutenção, temporada, desafio, etc.

  Classifique a mensagem de acordo com o tema principal.
  '''),
  ("human", '''Você deve categorizar a seguinte mensagem do usuário: {user_message}''')
])

class Categorizer(BaseModel):
  '''Categoriza mensagens do usuário em diferentes categorias.'''
  category: str = Field(description=f'''Categoria da mensagem do usuário. Deve ser "{attack_strategy}", "{cv_info}" ou "{update}", caso não se encaixe em nenhuma delas retorne "{others}".''')
  
structured_model = category_prompt | chat.with_structured_output(Categorizer)

def route(input):
  category = input["category"].category
  
  if category == attack_strategy:
    return strategy_chain
  if category == cv_info:
    return main_cv_chain
  if category == update:
    return news_chain
  else:
    return fallback_chain

chain_raw = RunnablePassthrough().assign(category=structured_model) | route

final_chain = RunnableWithMessageHistory(
  chain_raw,
  get_by_session_id,
  input_messages_key="user_message", 
  history_messages_key="history"
)

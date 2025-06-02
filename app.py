from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from utils.news import news_chain

load_dotenv(find_dotenv())

chat = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)

strategy_prompt = ChatPromptTemplate.from_template(
  '''Você é um especialista em traçar estratégias de ataques do jogo Clash of Clans.
  Você recebe uma descrição detalhada de uma base inimiga e tem acesso a um arquivo de informações sobre tropas, feitiços, herois e defesas de cada centro de vila (CV) do jogo.
  Base inimiga: {base_description}
  Informações do CV: {cv_info}
  Responda com uma estratégia de ataque detalhada, incluindo: 
  - Ordem de ataque das tropas
  - Uso de feitiços
  - Posicionamento de heróis
  - Considerações sobre defesas inimigas
  - Sugestões de tropas adicionais, se necessário
  - Qualquer outra informação relevante para o sucesso do ataque
  Certifique-se de que a estratégia seja viável e adaptada ao nível do CV da base inimiga.
  Leve em consideração:
  - As tropas, feitiços e heróis disponíveis no arquivo de informações do CV.
  - O layout da base inimiga.
  - O nível das defesas e do CV inimigo.
  - As fraquezas e pontos fortes da base inimiga.
  - A composição ideal de tropas para o ataque.
  - A mensagem do usuário: {user_message}
  Responda apenas com a estratégia de ataque, sem explicações adicionais.
  '''
)

main_cv_prompt = ChatPromptTemplate.from_template(
  '''Você é um especialista em Clash of Clans, com amplo conhecimento sobre tropas, feitiços, heróis e defesas de cada centro de vila (CV) do jogo, focado na vila principal.
  Você receberá uma base de dados contendo informações detalhadas sobre as tropas, feitiços, heróis e defesas de cada CV.
  Base de dados: {cv_data}
  Sua tarefa é responder às perguntas do usuário sobre as tropas, feitiços, heróis e defesas de cada CV.
  Pergunta do usuário: {user_message}
  Responda apenas com informações relevantes e precisas, sem explicações adicionais.
  Certifique-se de que suas respostas sejam baseadas nas informações contidas na base de dados fornecida.
  Se a pergunta não puder ser respondida com as informações disponíveis, informe que não há dados suficientes para responder.
  '''
)


fallback_prompt = ChatPromptTemplate.from_template(
  '''Responda sempre com: Desculpe, só posso responder perguntas relacionadas ao jogo Clash of Clans.'''
)

strategy_chain = strategy_prompt | chat
main_cv_chain = main_cv_prompt | chat
fallback_chain = fallback_prompt | chat

category_prompt = ChatPromptTemplate.from_template('''Você deve categorizar a seguinte mensagem do usuário: {user_message}''')

attack_strategy = 'estrategia de ataque'
cv_info = 'informacoes do CV'
update = 'atualizacoes'
others = 'outros'

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

chain = RunnablePassthrough().assign(category=structured_model) | route

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

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
  Se a pergunta não puder ser respondida com as informações disponíveis, informe que não há dados suficientes para responder.'''
)

strategy_chain = strategy_prompt | chat
main_cv_chain = main_cv_prompt | chat

category_prompt = ChatPromptTemplate.from_template('''Você deve categorizar a seguinte mensagem do usuário: {user_message}''')

class Categorizer(BaseModel):
  '''Categoriza mensagens do usuário em diferentes categorias.'''
  category: str = Field(description='''Categoria da mensagem do usuário. Deve ser "estratégia de ataque" ou "informações do CV", caso não se encaixe em nenhuma delas retorne "outros".''')
  
structured_model = category_prompt | chat.with_structured_output(Categorizer)

resposta_1 = structured_model.invoke(
  {
    'user_message': 'Qual é a melhor estratégia de ataque para uma base com CV 14, considerando que tenho dragões e feitiços de cura?'
  }
)

print(f'Resposta 1: {resposta_1}')

resposta_2 = structured_model.invoke(
  {
    'user_message': 'Quais são as tropas disponíveis no CV 12?'
  }
)

print(f'Resposta 2: {resposta_2}')

resposta_3 = structured_model.invoke(
  {
    'user_message': 'Receita de bolo de chocolate'
  }
)

print(f'Resposta 3: {resposta_3}')


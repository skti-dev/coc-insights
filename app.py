from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from utils.news import news_chain

load_dotenv(find_dotenv())

chat = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)

strategy_prompt = ChatPromptTemplate.from_template(
  '''
  Você é um especialista em estratégias de ataque no jogo Clash of Clans.

  Sua tarefa é analisar uma base inimiga e sugerir uma estratégia detalhada e eficaz. Para isso, você terá acesso a:
  - Uma descrição da base inimiga
  - Informações sobre tropas, feitiços, heróis e defesas organizadas por nível de Centro de Vila (CV)
  - Uma mensagem adicional fornecida pelo jogador

  ### Instruções:
  Com base nas informações fornecidas, elabore uma estratégia de ataque contendo:

  1. Ordem de ataque das tropas
  2. Uso recomendado de feitiços
  3. Posicionamento dos heróis
  4. Considerações sobre as defesas da base inimiga
  5. Sugestões de tropas adicionais, se necessário
  6. Observações relevantes para garantir o sucesso do ataque

  ### Regras:
  - A estratégia deve ser viável e adaptada ao nível do CV da base inimiga.
  - Leve em conta as tropas, heróis e feitiços disponíveis no nível correspondente do CV.
  - Use o layout e características defensivas da base inimiga para identificar fraquezas.
  - Mantenha a resposta clara, concisa e focada na execução da estratégia.

  ### IMPORTANTE:
  Se a mensagem do usuário estiver em português, **responda obrigatoriamente em português**, incluindo a tradução de termos técnicos se necessário.

  ---

  Base inimiga: {base_description}
  Informações do CV: {cv_info}
  Mensagem do usuário: {user_message}
  '''
)

main_cv_prompt = ChatPromptTemplate.from_template(
  '''
  Você é um especialista no jogo Clash of Clans, com profundo conhecimento sobre a vila principal, incluindo tropas, feitiços, heróis e defesas de cada nível de Centro de Vila (CV).

  Sua função é responder perguntas com base em uma base de dados detalhada, contendo informações específicas sobre cada CV.

  ### Dados disponíveis:
  {cv_data}

  ### Pergunta do usuário:
  {user_message}

  ### Instruções:
  - Responda somente com informações que estejam presentes na base de dados fornecida.
  - Caso não haja informações suficientes para responder à pergunta, diga claramente: **"Não há dados suficientes para responder."**
  - Evite explicações genéricas ou especulações.
  - Seja direto e preciso.

  ### Tradução:
  Se a pergunta do usuário estiver em português, **responda obrigatoriamente em português**, mesmo que os dados estejam em outro idioma. Traduza os termos técnicos se necessário.
  '''
)


fallback_prompt = ChatPromptTemplate.from_template(
  '''Responda sempre com: **Desculpe, só posso responder perguntas relacionadas ao jogo Clash of Clans.**'''
)

strategy_chain = strategy_prompt | chat
main_cv_chain = main_cv_prompt | chat
fallback_chain = fallback_prompt | chat

attack_strategy = 'estrategia de ataque'
cv_info = 'informacoes do CV'
update = 'atualizacoes'
others = 'outros'

category_prompt = ChatPromptTemplate.from_template(f'''
Você deve categorizar a seguinte mensagem do usuário: {{user_message}}

Categorias disponíveis:
- "{attack_strategy}": Perguntas relacionadas a estratégias de ataque, tropas usadas, ordem de ataque, etc.
- "{cv_info}": Perguntas sobre tropas, defesas, heróis ou feitiços específicos de cada centro de vila (CV).
- "{update}": Perguntas sobre atualizações, eventos, novidades ou notícias do jogo.
- "{others}": Qualquer outra pergunta que não se encaixe nas categorias acima.

Alguns exemplos de palavras associadas à categoria "{update}": evento, evento sazonal, novidade, atualização, patch, mudanças, lançamento, manutenção, temporada, desafio, etc.

Classifique a mensagem de acordo com o tema principal.
''')

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

# Todo:
# Criar base de dados de CVs com informações sobre:
# - tropas e heróis,
# - feitiços,
# - defesas - OK
# Fazer RAG para passar contexto relevante para os prompts e evitar passar todas as informações de uma vez
# Melhorar a categorização de mensagens do usuário.
# Implementar lógica para lidar com a strategy_chain
# Implementar lógica para lidar com a main_cv_chain
# Criar interface com streamlit
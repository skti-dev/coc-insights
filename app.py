from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import tool
from langchain_community.document_loaders.web_base import WebBaseLoader
import re
from slugify import slugify
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.agents import AgentFinish

load_dotenv(find_dotenv())

def get_news_data():
  '''Carrega os dados de notícias do Clash of Clans.'''
  url_news = 'https://supercell.com/en/games/clashofclans/pt/blog/'
  possible_paths = ["news", "release-notes"]

  loader = WebBaseLoader(url_news)
  documents = loader.load()
  document = documents[0].page_content

  pattern = r"(\d{1,2}/\d{1,2}/\d{4})Blog – Clash of Clans([^\d]+)"
  news = re.findall(pattern, document)

  news_base_url = "https://supercell.com/en/games/clashofclans/pt/blog/"
  news_data = []

  for data, title in news:
    clean_title = title.strip()
    slug = slugify(clean_title, lowercase=True)
    
    urls = [f'{news_base_url}{path}/{slug}/' for path in possible_paths]
    
    news_data.append({
      'data': data,
      'title': clean_title,
      'slug': slug,
      'urls': urls
    })
  
  return news_data

def get_news_content(possible_urls):
  for url in possible_urls:
    try:
      loader = WebBaseLoader(url)
      documents = loader.load()
      if not documents:
        continue
      
      doc = documents[0].page_content.strip()

      erro = any(err_msg in doc for err_msg in [
        "Page not found",
        "Sorry, but the page or file you were trying to access does not exist."
      ])

      if not doc or erro:
        continue
      
      return doc, url
    except Exception:
      continue
  return None, None

class NewsArgs(BaseModel):
  '''Título da notícia a ser buscada.'''
  title: str = Field(description='''Parte do título da notícia desejada (pode ser uma palavra-chave)''')
  
@tool(args_schema=NewsArgs) 
def get_news_by_title(title: str):
  """
  Busca uma notícia do Clash of Clans a partir de uma palavra-chave no título e retorna os detalhes.
  """
  news_data = get_news_data()
  if not news_data:
    return "Nenhuma notícia encontrada."
  
  for item in news_data:
    if title.lower() in item['title'].lower():
      content, url = get_news_content(item['urls'])
      if content:
        return {
          'data': item['data'],
          'title': item['title'],
          'url': url,
          'content': content
        }

  return "Nenhuma notícia encontrada com esse título."

@tool
def get_all_news():
  """
  Retorna uma lista de todas as notícias do Clash of Clans.
  """
  news_data = get_news_data()
  if not news_data:
    return "Nenhuma notícia encontrada."

  return news_data

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

news_prompt = ChatPromptTemplate.from_template(
  '''Você é um especialista em Clash of Clans com amplo conhecimento sobre as notícias do jogo.
  Receberá uma pergunta do usuário sobre notícias do jogo e deve responder com informações precisas e atualizadas.
  Pergunta do usuário: {user_message}
  Se a pergunta for sobre uma notícia específica, busque a notícia pelo título e forneça os detalhes relevantes.
  Se a pergunta for sobre notícias em geral, forneça uma lista de todas as notícias disponíveis.
  Se não houver notícias disponíveis, informe que não há notícias recentes.
  Responda apenas com informações relevantes e precisas, sem explicações adicionais.
  Se a pergunta não puder ser respondida com as informações disponíveis, informe que não há dados suficientes para responder.
  '''
)

fallback_prompt = ChatPromptTemplate.from_template(
  '''Responda sempre com: Desculpe, só posso responder perguntas relacionadas ao jogo Clash of Clans.'''
)

news_tools = [
  get_news_by_title,
  get_all_news
]
news_tools_json = [convert_to_openai_function(tool) for tool in news_tools]
news_tool_run = {tool.name: tool for tool in news_tools}
def news_tool_route(result):
  if isinstance(result, AgentFinish):
    return result.return_values['output']

  return main_cv_tool_run[result.tool].run(result.tool_input)

news_chain = news_prompt | chat.bind(functions=news_tools_json) | OpenAIFunctionsAgentOutputParser() | news_tool_route
strategy_chain = strategy_prompt | chat
main_cv_chain = main_cv_prompt | chat
fallback_chain = fallback_prompt | chat

category_prompt = ChatPromptTemplate.from_template('''Você deve categorizar a seguinte mensagem do usuário: {user_message}''')

class Categorizer(BaseModel):
  '''Categoriza mensagens do usuário em diferentes categorias.'''
  category: str = Field(description='''Categoria da mensagem do usuário. Deve ser "estratégia de ataque", "informações do CV" ou "atualizações", caso não se encaixe em nenhuma delas retorne "outros".''')
  
structured_model = category_prompt | chat.with_structured_output(Categorizer)

def route(input):
  if input['categoria'] == 'estratégia de ataque':
    return strategy_chain
  if input['categoria'] == 'informações do CV':
    return main_cv_chain
  if input['categoria'] == 'atualizações':
    return news_chain
  return fallback_chain

chain = RunnablePassthrough().assign(category=structured_model) | route

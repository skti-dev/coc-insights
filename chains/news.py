from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.agents import tool
from langchain_community.document_loaders.web_base import WebBaseLoader
import re
from slugify import slugify
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.agents import AgentFinish

def get_news_data(return_slug_and_urls=True):
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
    
    if return_slug_and_urls:
      news_data.append({
        'data': data,
        'title': clean_title,
        'slug': slug,
        'urls': urls
      })
    else:
      news_data.append({
        'data': data,
        'title': clean_title
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
  news_data = get_news_data(return_slug_and_urls=False)
  if not news_data:
    return "Nenhuma notícia encontrada."

  return news_data

news_prompt = ChatPromptTemplate.from_template(
  '''Você é um especialista em Clash of Clans com amplo conhecimento sobre as notícias do jogo.

  Receberá uma pergunta do usuário relacionada às notícias mais recentes e deverá responder com base nas informações disponíveis.

  Instruções:
  - Se a pergunta for sobre uma notícia específica, localize-a pelo título e forneça os principais detalhes.
  - Se for sobre notícias em geral, liste todas as disponíveis de forma resumida.
  - Caso não existam notícias, informe que não há atualizações recentes.
  - Se os dados disponíveis não forem suficientes para responder à pergunta, deixe isso claro.

  Responda apenas com informações objetivas e relevantes, sem explicações adicionais.

  Pergunta do usuário: {user_message}
'''
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

  return news_tool_run[result.tool].run(result.tool_input)

news_chat = ChatOpenAI(model='gpt-4o-mini', temperature=0)

news_chain_raw = news_prompt | news_chat.bind(functions=news_tools_json) | OpenAIFunctionsAgentOutputParser() | news_tool_route

format_prompt = ChatPromptTemplate.from_template(
  '''Você é um assistente que recebe dados de notícias do Clash of Clans em formato bruto e deve formatar a resposta para o usuário de forma amigável e clara.
  
  Dados crus: {raw_data}
  
  Retorne a lista de notícias formatada, usando markdown, por exemplo:
  #### Lista de notícias:
  - Título 1 (data)
  - Título 2 (data)
  '''
)

format_chain = format_prompt | news_chat

news_chain = news_chain_raw.pipe(lambda x: {"raw_data": x}) | format_chain

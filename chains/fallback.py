from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

fallback_chat = ChatOpenAI(model='gpt-4o-mini', temperature=0)

fallback_prompt = ChatPromptTemplate.from_template(
  '''Responda sempre com: **Desculpe, só posso responder perguntas relacionadas ao jogo Clash of Clans.**'''
)

fallback_chain = fallback_prompt | fallback_chat

import json
import os
import hashlib
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

SUMMARY_CACHE_FILE = 'data/summary_cache.json'
summary_cache = {}

def load_summary_cache():
  global summary_cache
  if os.path.exists(SUMMARY_CACHE_FILE):
    try:
      with open(SUMMARY_CACHE_FILE, 'r', encoding='utf-8') as f:
        summary_cache = json.load(f)
    except Exception as e:
      print(f"Erro ao carregar cache: {e}")
      summary_cache = {}
  else:
    summary_cache = {}

def save_summary_cache():
  try:
    with open(SUMMARY_CACHE_FILE, 'w', encoding='utf-8') as f:
      json.dump(summary_cache, f, ensure_ascii=False, indent=2)
  except Exception as e:
    print(f"Erro ao salvar cache: {e}")

def hash_strategy(strategy: list[str]) -> str:
  joined = '\n'.join(sorted(strategy))
  return hashlib.md5(joined.encode('utf-8')).hexdigest()

def summarize_with_cache(strategies: list[str]) -> str:
  if not strategies:
    return "Nenhuma estratégia fornecida."
  
  key = hash_strategy(strategies)
  if key in summary_cache:
    return summary_cache[key]
  summarize_chat = ChatOpenAI(model="gpt-4o-mini", max_tokens=256)
  summarize_prompt = ChatPromptTemplate.from_template(
    """Resuma as estratégias ofensivas abaixo, mantendo apenas as ideias principais em no máximo 2 frases:
    ### IMPORTANTE:
    **Responda obrigatoriamente em português**, incluindo a tradução de termos técnicos se necessário.
    
    Estratégias:
    {strategies}

    Resumo:"""
  )
  summarize_chain = summarize_prompt | summarize_chat
  joined_strategies = '\n-' + '\n-'.join(strategies)
  summary = summarize_chain.invoke({"strategies": joined_strategies}).content.strip()
  summary_cache[key] = summary
  save_summary_cache()
  return summary

load_summary_cache()
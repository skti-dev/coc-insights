from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.cv_data import get_cv_data
from chains.filter_cv_data import filter_cv_data_chain

main_cv_chat = ChatOpenAI(model="gpt-4o-mini", temperature=0)

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

def prepare_filtered_data(input: dict):
  user_message = input["user_message"]
  full_data = get_cv_data(user_message)
  
  raw_filtered = filter_cv_data_chain.invoke({
    "user_message": user_message,
    "cv_data": full_data
  })

  try:
    try:
      cleaned_str = raw_filtered.content.strip().removeprefix("```json").removesuffix("```")
      filtered_data = json.loads(cleaned_str)
    except json.JSONDecodeError:
      raise ValueError("Resposta do filtro não é um JSON válido")

    if not isinstance(filtered_data, dict) or not filtered_data:
      raise ValueError("Filtragem inválida ou vazia")

    return {
      "cv_data": filtered_data,
      "user_message": user_message
    }

  except Exception as e:
    print(f"[⚠️ Fallback ativado] Motivo: {e}")
    return {
      "cv_data": full_data,
      "user_message": user_message
    }

main_cv_chain = RunnableLambda(prepare_filtered_data) | main_cv_prompt | main_cv_chat

# Testing purpose
if __name__ == "__main__":
  response = main_cv_chain.invoke({
    "user_message": "Quantas tropas eu posso ter no CV 9?"
  })
  print(response.content)

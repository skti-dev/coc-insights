from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.cv_data import get_cv_data
from chains.filter_cv_data import filter_cv_data_chain
from utils.base_description import image_analysis, extract_defense_details

strategy_chat = ChatOpenAI(model='gpt-4o-mini', temperature=0)

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
  - Leve em conta as tropas, heróis e feitiços disponíveis no nível correspondente do CV do atacante caso seja informado.
  - Use o layout e características defensivas da base inimiga para identificar fraquezas.
  - Mantenha a resposta clara, concisa e focada na execução da estratégia.

  ### IMPORTANTE:
  Se a mensagem do usuário estiver em português, **responda obrigatoriamente em português**, incluindo a tradução de termos técnicos se necessário.

  ---

  Base inimiga: {base_description}\n
  Informações do CV: {cv_data}\n
  Mensagem do usuário: {user_message}
  '''
)

def prepare_filtered_data(input: dict):
  user_message = input["user_message"]
  image_path = input.get("image_path") 
  base_description = "Nenhuma imagem fornecida para análise."

  if image_path:
    try:
      analysis = image_analysis(image_path)
      base_info = extract_defense_details(analysis, 'data/defenses_database.json')
      base_description = json.dumps(base_info, ensure_ascii=False, indent=2)
    except Exception as e:
      base_description = f"Erro na análise de imagem: {e}"

  full_data = get_cv_data(user_message)
  try:
    raw_filtered = filter_cv_data_chain.invoke({
      "user_message": user_message,
      "cv_data": full_data
    })

    try:
      cleaned_str = raw_filtered.content.strip().removeprefix("```json").removesuffix("```")
      filtered_data = json.loads(cleaned_str)
    except json.JSONDecodeError:
      raise ValueError("Resposta do filtro não é um JSON válido")

    if not isinstance(filtered_data, dict) or not filtered_data:
      raise ValueError("Filtragem inválida ou vazia")

    return {
      "cv_data": filtered_data,
      "base_description": base_description,
      "user_message": user_message
    }

  except Exception as e:
    print(f"[⚠️ Fallback ativado] Motivo: {e}")
    return {
      "cv_data": full_data,
      "base_description": base_description,
      "user_message": user_message
    }

strategy_chain = RunnableLambda(prepare_filtered_data) | strategy_prompt | strategy_chat

# Testing purpose
if __name__ == "__main__":
  response = strategy_chain.invoke({
    "user_message": "Quero uma estratégia de ataque para essa vila. Meu CV é 9.",
    "image_path": "data/vila_cv_15.jpg"  # optional, can be omitted
  })
  
  print(response.content)
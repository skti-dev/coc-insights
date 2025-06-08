from dotenv import load_dotenv, find_dotenv
from chains.final_chain import final_chain

load_dotenv(find_dotenv())

def test_chain():
  response = final_chain.invoke(
    {"user_message": "Como ataco uma vila com duas torres inferno?"},
    config={"configurable": {"session_id": "Augusto"}}
  )
  print(response.content)

if __name__ == '__main__':
  test_chain()

# Todo:
# Criar interface com streamlit
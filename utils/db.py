from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sqlite_connection_string = "sqlite:///db/chat_history.db"

def load_history_from_db(session_id):
  db_history = SQLChatMessageHistory(session_id=session_id, connection_string=sqlite_connection_string)
  messages = db_history.messages

  history_as_dict = []
  user_msg = None

  for msg in messages:
    if isinstance(msg, AIMessage) or isinstance(msg, HumanMessage):
      if isinstance(msg, HumanMessage):
        user_msg = msg.content
      elif isinstance(msg, AIMessage) and user_msg is not None:
        history_as_dict.append({"user": user_msg, "bot": msg.content})
        user_msg = None

  return history_as_dict

def clear_db_history(session_id=None):
  if session_id is None:
    session_id = 'Anônimo'

  db_history = SQLChatMessageHistory(session_id=session_id, connection_string=sqlite_connection_string)
  db_history.clear()
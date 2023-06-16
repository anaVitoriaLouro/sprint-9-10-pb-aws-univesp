import hashlib

def generate_session_id(chat_id):
  # This creates the chat_id for the connection
  return hashlib.sha256(chat_id.encode('utf-8')).hexdigest()[:8]
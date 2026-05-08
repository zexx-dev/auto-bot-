import os

class Config:
    # --- REQUIRED ---
    API_ID = int(os.environ.get("API_ID", "1234567")) # Apna API_ID dalo
    API_HASH = os.environ.get("API_HASH", "your_hash") # Apna Hash dalo
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token") # Apna Token dalo
    ADMIN_ID = int(os.environ.get("ADMIN_ID", "00000000")) # Apni User ID dalo
    
    # --- OPTIONAL ---
    DB_NAME = "bot_data.db"

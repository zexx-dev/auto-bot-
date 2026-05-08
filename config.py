import os

class Config:
    # --- REQUIRED ---
    API_ID = int(os.environ.get("API_ID", "22346961")) # Apna API_ID dalo
    API_HASH = os.environ.get("API_HASH", "d68fc6ff87a69a39efdc1656acd001d4") # Apna Hash dalo
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7848192544:AAEPLywZ09vi4lis2yiYdGvpwotZZpGyxeo") # Apna Token dalo
    ADMIN_ID = int(os.environ.get("ADMIN_ID", "6715373877")) # Apni User ID dalo
    
    # --- OPTIONAL ---
    DB_NAME = "bot_data.db"

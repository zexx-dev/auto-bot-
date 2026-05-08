import asyncio
import sqlite3
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, Message
from config import Config

app = Client(
    "pro_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Database Initialize
def init_db():
    conn = sqlite3.connect(Config.DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, val_text TEXT, val_file_id TEXT, val_type TEXT)")
    c.execute("INSERT OR IGNORE INTO settings VALUES ('welcome', 'Hello! I am your Request Acceptor Bot.', NULL, 'text')")
    conn.commit()
    conn.close()

init_db()

# 1. AUTO ACCEPT REQUESTS
@app.on_chat_join_request()
async def auto_approve(client, request: ChatJoinRequest):
    try:
        await request.approve()
        conn = sqlite3.connect(Config.DB_NAME)
        conn.execute("INSERT OR IGNORE INTO users VALUES (?)", (request.from_user.id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error approving: {e}")

# 2. START COMMAND (USER GETS CUSTOM MESSAGE)
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    uid = message.from_user.id
    conn = sqlite3.connect(Config.DB_NAME)
    conn.execute("INSERT OR IGNORE INTO users VALUES (?)", (uid,))
    data = conn.execute("SELECT val_text, val_file_id, val_type FROM settings WHERE key='welcome'").fetchone()
    conn.commit()
    conn.close()

    text, file_id, m_type = data
    try:
        if m_type == "photo":
            await client.send_photo(uid, file_id, caption=text)
        elif m_type == "video":
            await client.send_video(uid, file_id, caption=text)
        elif m_type == "document":
            await client.send_document(uid, file_id, caption=text)
        elif m_type == "voice":
            await client.send_voice(uid, file_id, caption=text)
        else:
            await client.send_message(uid, text)
    except Exception:
        await message.reply("Bot is active!")

# 3. SET WELCOME MESSAGE (ADMIN ONLY)
@app.on_message(filters.command("set_welcome") & filters.user(Config.ADMIN_ID) & filters.private)
async def set_welcome(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Kisi message ko reply karke `/set_welcome` likho!")
    
    rep = message.reply_to_message
    m_type = "text"
    f_id = None
    caption = rep.caption or rep.text or ""

    if rep.photo: m_type, f_id = "photo", rep.photo.file_id
    elif rep.video: m_type, f_id = "video", rep.video.file_id
    elif rep.document: m_type, f_id = "document", rep.document.file_id
    elif rep.voice: m_type, f_id = "voice", rep.voice.file_id

    conn = sqlite3.connect(Config.DB_NAME)
    conn.execute("INSERT OR REPLACE INTO settings VALUES ('welcome', ?, ?, ?)", (caption, f_id, m_type))
    conn.commit()
    conn.close()
    await message.reply(f"Done! Ab naye users ko ye {m_type} milega. ✅")

# 4. BROADCAST (ADMIN ONLY)
@app.on_message(filters.command("broadcast") & filters.user(Config.ADMIN_ID) & filters.private)
async def broadcast(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Broadcast ke liye kisi post ko reply karo!")
    
    conn = sqlite3.connect(Config.DB_NAME)
    users = [row[0] for row in conn.execute("SELECT user_id FROM users").fetchall()]
    conn.close()

    sent = 0
    msg = await message.reply(f"Broadcast shuru... {len(users)} users ko bhejna hai.")
    for u_id in users:
        try:
            await message.reply_to_message.copy(u_id)
            sent += 1
            await asyncio.sleep(0.1)
        except: pass
    await msg.edit(f"**Broadcast Done!**\nSent to: {sent} users.")

print("Your Pro Bot is running...")
app.run()

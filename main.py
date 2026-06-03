import asyncio
from pyrogram import Client, filters, enums
from dotenv import load_dotenv
import os

load_dotenv()

# --- SOZLAMALAR ---
API_ID = int(os.getenv("30302100"))
API_HASH = os.getenv("3fd819978fa769fb0fae89d14923fd74")
STRING_SESSION = os.getenv("BQHOX5QAv4GNGfkgn63CY9aW_YoOVleew34Kb3DM-AE2-iC_NAYqNHZ7CtUdsRVzJKAD1X8O-3JXiKDCAtb_5l3KT04q98Uo4QDCr6pXvSpnY10dG0qu9t9s66Xka7kFYfFeLiWc3473n92SNEIqShFE9YwHRaopSXaOmDNubjL0NRDp547a_UHgt3ukai5eijjZYclkNHkFqXRsO8PsFhVEwCqrTfZJ1XonyrTPOPUx1m8-cfjsbHBShLJGde797lWf075pHLIaTdwL-UBUie-5P6bn6q6uocLY0G4634K61Xv93qQ3Rex0AYPjtHIQTEosHLVkFZV4K4HkXfDG1JDfhgF0HQAAAAH_Acc2AA")
SOURCE_CHANNEL = os.getenv("3915622076") # Kanal ID yoki username

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# Global o'zgaruvchilar (Bazasiz ishlaydi)
is_running = False
interval_minutes = 5
last_message_id = 0

# --- KOMANDALAR ---
@app.on_message(filters.me & filters.command("on", prefixes="."))
async def start_bot(client, message):
    global is_running
    is_running = True
    await message.edit("✅ **Bot yoqildi!**")

@app.on_message(filters.me & filters.command("off", prefixes="."))
async def stop_bot(client, message):
    global is_running
    is_running = False
    await message.edit("❌ **Bot o‘chirildi!**")

@app.on_message(filters.me & filters.command("status", prefixes="."))
async def status_bot(client, message):
    status = "🟢 **Online**" if is_running else "🔴 **Offline**"
    await message.edit(f"Bot holati: {status}\nInterval: {interval_minutes} daqiqa")

@app.on_message(filters.me & filters.command("edit_time", prefixes="."))
async def set_time(client, message):
    global interval_minutes
    try:
        new_time = int(message.command[1])
        if 1 <= new_time <= 60:
            interval_minutes = new_time
            await message.edit(f"⏱ Interval {new_time} daqiqaga o‘zgartirildi.")
        else:
            await message.edit("⚠️ Iltimos, 1 dan 60 gacha raqam kiriting.")
    except:
        await message.edit("⚠️ Format: `.edit_time 5`")

# --- ASOSIY LOGIKA ---
async def distribution_task():
    global last_message_id
    while True:
        if is_running:
            try:
                # Kanalni tekshirish
                async for msg in app.get_chat_history(SOURCE_CHANNEL, limit=1):
                    if msg.id > last_message_id:
                        last_message_id = msg.id
                        
                        # Guruhlarni olish
                        dialogs = [d async for d in app.get_dialogs() if d.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]]
                        
                        for dialog in dialogs:
                            try:
                                await app.forward_messages(dialog.chat.id, SOURCE_CHANNEL, [last_message_id])
                                await asyncio.sleep(10) # Anti-spam kechikishi
                            except:
                                continue
            except Exception as e:
                print(f"Xatolik: {e}")
        
        await asyncio.sleep(interval_minutes * 60)

async def main():
    await app.start()
    print("Bot muvaffaqiyatli ishga tushdi!")
    app.loop.create_task(distribution_task())
    await asyncio.gather(app.get_me()) # Botni ushlab turish

if __name__ == "__main__":
    app.run(main())
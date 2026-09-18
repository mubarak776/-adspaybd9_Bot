import logging
import os
import sqlite3
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Flask app keeping Render Web Service alive for FREE
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = "8728150460:AAEaL3Adfna9EKhJo02dLqRrqO2i9FjLNX8"
CHANNEL_USERNAME = "@IslamicNoorBD09"
GROUP_INVITE_LINK = "https://t.me/EasilySuhogEinw21"
MINI_APP_URL = "https://mubarak776.github.io/-adspaybd9_Bot/"

conn = sqlite3.connect('bot_users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
conn.commit()

def save_user(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    save_user(user_id)

    is_subscribed = await check_subscription(user_id, context)

    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 চ্যানেল জয়েন করুন", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton("💬 গ্রুপ জয়েন করুন", url=GROUP_INVITE_LINK)],
            [InlineKeyboardButton("✅ Verify করুন", callback_data="verify_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"👋 আসসালামু আলাইকুম, {user.first_name}!\n\n"
            f"⚠️ বটে পরবর্তী কাজ করার জন্য আমাদের অফিশিয়াল চ্যানেল ও গ্রুপে জয়েন করতে হবে।\n\n"
            f"👉 নিচে জয়েন করে এরপরে **'Verify'** বাটنه ক্লিক করুন 👈",
            reply_markup=reply_markup
        )
    else:
        await send_welcome_screen(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    save_user(user_id)

    if query.data == "verify_sub":
        is_subscribed = await check_subscription(user_id, context)
        if is_subscribed:
            try:
                await query.message.delete()
            except Exception:
                pass
            await send_welcome_screen(query, context)
        else:
            await query.answer("❌ আপনি এখনো চ্যানেল বা গ্রুপে জয়েন করেননি! দয়া করে জয়েন করে আবার চেষ্টা করুন।", show_alert=True)

async def send_welcome_screen(update_obj, context):
    user = update_obj.effective_user if hasattr(update_obj, 'effective_user') else update_obj.from_user
    keyboard = [
        [InlineKeyboardButton("🚀 Open Telegram App", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        f"🎉 স্বাগতম {user.first_name}!\n\n"
        f"আপনার সাবস্ক্রিপশন সফলভাবে যাচাই করা হয়েছে। নিচের বাটনে ক্লিক করে অ্যাপে প্রবেশ করুন 👇"
    )
    if hasattr(update_obj, 'message') and update_obj.message:
        await update_obj.message.reply_text(text, reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=user.id, text=text, reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    await update.message.reply_text(f"📊 মোট ব্যবহারকারী (Total Users): {total_users}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start bot polling in background
    application.run_polling()

if __name__ == '__main__':
    # Run Flask on port 10000 for Render Free Web Service
    port = int(os.environ.get("PORT", 10000))
    from threading import Thread
    Thread(target=main).start()
    app.run(host='0.0.0.0', port=port)
        

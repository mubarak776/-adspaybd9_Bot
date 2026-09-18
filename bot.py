import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = "8728150460:AAEaL3Adfna9EKhJo02dLqRrqO2i9FjLNX8"
CHANNEL_USERNAME = "@IslamicNoorBD09"
GROUP_INVITE_LINK = "https://t.me/+eauIySuhogEwNmZl"
WEB_APP_URL = "https://mubarak776.github.io/-adspaybd9_Bot/"

conn = sqlite3.connect('bot_users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
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
            [InlineKeyboardButton("👥 গ্রুপে জয়েন করুন", url=GROUP_INVITE_LINK)],
            [InlineKeyboardButton("✅ Verify করুন", callback_data="verify_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"👋 আসসালামু আলাইকুম, {user.first_name}!\n\n"
            f"⚠️ বটের পরবর্তী ফিচারগুলো ব্যবহার করতে হলে আপনাকে অবশ্যই আমাদের চ্যানেল ও গ্রুপে জয়েন করতে হবে!\n"
            f"👉 নিচে দেওয়া লিংকে জয়েন করে নিচে **\"Verify\"** বাটনে ক্লিক করুন ✨",
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
            await send_welcome_screen_by_query(query, context)
        else:
            await query.answer("❌ আপনি এখনো চ্যানেলে বা গ্রুপে জয়েন করেননি! দয়া করে জয়েন করে আবার চেষ্টা করুন।", show_alert=True)

async def send_welcome_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🚀 Open Telegram App", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🎉 স্বাগতম {user.first_name}!\n\n"
        f"আপনার সাবস্ক্রিপশন সফলভাবে যাচাই করা হয়েছে। নিচের বাটনে ক্লিক করে অ্যাপে প্রবেশ করুন 👇",
        reply_markup=reply_markup
    )

async def send_welcome_screen_by_query(query, context: ContextTypes.DEFAULT_TYPE):
    user = query.from_user
    keyboard = [
        [InlineKeyboardButton("🚀 Open Telegram App", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=user.id,
        text=f"🎉 স্বাগতম {user.first_name}!\n\n"
        f"আপনার সাবস্ক্রিপশন সফলভাবে যাচাই করা হয়েছে। নিচের বাটনে ক্লিক করে অ্যাপে প্রবেশ করুন 👇",
        reply_markup=reply_markup
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        conn_db = sqlite3.connect('bot_users.db')
        cursor_db = conn_db.cursor()
        cursor_db.execute("SELECT COUNT(*) FROM users")
        count = cursor_db.fetchone()[0]
        conn_db.close()
        await update.message.reply_text(f"📊 মোট ব্যবহারকারী/রোজা আছে: {count} জন")
    except Exception as e:
        await update.message.reply_text("⚠️ ডেটাবেস থেকে তথ্য পড়তে সমস্যা হচ্ছে।")

async def auto_forward_channel_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        message_id = update.channel_post.message_id
        from_chat_id = update.channel_post.chat.id

        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()

        for (user_id,) in users:
            try:
                await context.bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=from_chat_id,
                    message_id=message_id
                )
            except Exception as e:
                logger.error(f"Failed to send message to {user_id}: {e}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Chat(chat_id=CHANNEL_USERNAME), auto_forward_channel_posts))

    print("Bot is running successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()

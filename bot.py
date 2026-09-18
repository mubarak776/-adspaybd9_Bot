import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# আপনার টেলিগ্রাম বটের টোকেন এখানে বসাবেন (যদি আগে অন্য টোকেন দিয়ে থাকেন)
TOKEN = "8728150460:AAEaL3Adfna9EKhJo02dLqRrqO2i9FjLNX8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # স্বাগত বার্তা
    welcome_text = (
        f"👋 আসসালামু আলাইকুম, {user.first_name}!\n"
        "স্বাগতম আমাদের অফিসিয়াল AdsPayBD বটে! 🚀\n"
        "এখানে আপনি খুব সহজে প্রতিদিন এড দেখে এবং ছোটখাটো টাস্ক পূরণ করে অনলাইন থেকে আয় করতে পারবেন।\n\n"
        "⚠️ গুরুত্বপূর্ণ নিয়মাবলী ও শর্ত:\n"
        "বটের সব ফিচার এবং আপডেট পেতে হলে অবশ্যই আমাদের নিচের চ্যানেল ও গ্রুপে জয়েন করতে হবে।"
    )
    
    # বাটনগুলো তৈরি করা
    keyboard = [
        [InlineKeyboardButton("📢 অফিসিয়াল চ্যানেল", url="https://t.me/IslamicNoorBD09")],
        [InlineKeyboardButton("💬 সাপোর্ট গ্রুপ", url="https://t.me/Community_Task2")],
        [InlineKeyboardButton("🚀 আয় করুন (Mini App)", web_app=WebAppInfo(url="https://mubarak776.github.io/-adspaybd9_Bot/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ছবি ও মেসেজ পাঠানো
    photo_url = "https://i.ibb.co.com/84j7qG1/photo-2024-09-18-19-12-50.jpg" # চাইলে আপনার ছবির লিংক দিতে পারেন
    await update.message.reply_photo(photo=photo_url, caption=welcome_text, reply_markup=reply_markup)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
    

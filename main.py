import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load API keys from Railway environment variables
API_URL = f"https://keyauth.win/api/seller/?sellerkey={os.getenv('KEYAUTH_SELLER_KEY')}&type=check&key="
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def check_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = ' '.join(context.args)
    response = requests.get(API_URL + key).json()
    
    if response.get("success"):
        await update.message.reply_text(f"✅ Key is valid! Expires: {response['expiry']}")
    else:
        await update.message.reply_text("❌ Invalid or expired key.")

# Start Telegram bot using the new API
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("check", check_license))

# Run the bot
app.run_polling()

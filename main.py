import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load API keys from Railway environment variables
KEYAUTH_SELLER_KEY = os.getenv("KEYAUTH_SELLER_KEY")
API_URL = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTH_SELLER_KEY}&type=check&key="
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def check_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a license key. Example: `/check YOUR_KEY`")
        return

    key = ' '.join(context.args)
    url = API_URL + key

    try:
        response = requests.get(url)
        response_json = response.json()  # Convert to dictionary

        print(f"API Request URL: {url}")  # Debug log
        print(f"API Response: {response_json}")  # Debug log

        if response_json.get("success"):
            await update.message.reply_text(f"✅ Key is valid! Expires: {response_json['expiry']}")
        else:
            await update.message.reply_text(f"❌ Invalid or expired key.\n\nResponse: {response_json}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error checking key: {e}")

# Start Telegram bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("check", check_license))

# Run the bot
app.run_polling()

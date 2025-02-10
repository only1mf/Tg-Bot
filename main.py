import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load API keys from Railway environment variables
KEYAUTH_SELLER_KEY = os.getenv("KEYAUTH_SELLER_KEY")
API_URL = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTH_SELLER_KEY}&type="
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def check_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a license key. Example: `/check YOUR_KEY`")
        return

    key = ' '.join(context.args)
    url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTH_SELLER_KEY}&type=verify&key={key}"

    try:
        response = requests.get(url).json()
        print(f"API Request URL: {url}")  # Debugging log
        print(f"API Response: {response}")  # Debugging log

        if response.get("success"):
            await update.message.reply_text(f"✅ Key exists and is valid.")
        else:
            await update.message.reply_text(f"❌ Key does not exist or is invalid.\n\nResponse: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error checking key: {e}")
        
async def add_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: `/add <license_key> <duration_in_days>`")
        return

    key, duration = context.args[0], context.args[1]
    url = API_URL + f"add&key={key}&duration={duration}"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ License key added! Expires in {duration} days.")
        else:
            await update.message.reply_text(f"❌ Error adding key: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def ban_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/ban <license_key>`")
        return

    key = ' '.join(context.args)
    url = API_URL + f"ban&key={key}"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ License key `{key}` has been banned.")
        else:
            await update.message.reply_text(f"❌ Error banning key: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def unban_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/unban <license_key>`")
        return

    key = ' '.join(context.args)
    url = API_URL + f"unban&key={key}"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ License key `{key}` has been unbanned.")
        else:
            await update.message.reply_text(f"❌ Error unbanning key: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def info_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/info <license_key>`")
        return

    key = ' '.join(context.args)
    url = API_URL + f"info&key={key}"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            details = f"🔹 **Key:** {key}\n🔹 **Created:** {response['created']}\n🔹 **Expires:** {response['expiry']}\n🔹 **HWID:** {response.get('hwid', 'N/A')}\n🔹 **Status:** {'Banned' if response.get('banned') else 'Active'}"
            await update.message.reply_text(details)
        else:
            await update.message.reply_text(f"❌ Error fetching key info: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def extend_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: `/extend <license_key> <days>`")
        return

    key, days = context.args[0], context.args[1]
    url = API_URL + f"extend&key={key}&duration={days}"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ License key `{key}` extended by {days} days.")
        else:
            await update.message.reply_text(f"❌ Error extending key: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """🤖 **KeyAuth Bot Commands:**
🔹 `/check <key>` – Check if a key is valid
🔹 `/add <key> <days>` – Add a new license key
🔹 `/ban <key>` – Ban a license key
🔹 `/unban <key>` – Unban a license key
🔹 `/info <key>` – Get info about a license key
🔹 `/extend <key> <days>` – Extend a license key
🔹 `/help` – Show this help message"""
    await update.message.reply_text(help_text)

# Start Telegram bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Register command handlers
app.add_handler(CommandHandler("check", check_license))
app.add_handler(CommandHandler("add", add_license))
app.add_handler(CommandHandler("ban", ban_license))
app.add_handler(CommandHandler("unban", unban_license))
app.add_handler(CommandHandler("info", info_license))
app.add_handler(CommandHandler("extend", extend_license))
app.add_handler(CommandHandler("help", help_command))

# Run the bot
app.run_polling()

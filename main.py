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
    url = API_URL + f"verify&key={key}"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ Key exists and is valid.")
        else:
            await update.message.reply_text(f"❌ Key does not exist or is invalid.\n\nResponse: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error checking key: {e}")

async def retrieve_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = API_URL + "fetchallsessions"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            sessions = response.get("sessions", [])
            if not sessions:
                await update.message.reply_text("✅ No active sessions found.")
                return

            session_list = "\n".join([f"🔹 {s['id']} - {s['ip']}" for s in sessions])
            await update.message.reply_text(f"✅ Active Sessions:\n{session_list}")
        else:
            await update.message.reply_text(f"❌ Error fetching sessions: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def end_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/endsession <session_id>`")
        return

    sessid = context.args[0]
    url = API_URL + f"kill&sessid={sessid}"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ Session `{sessid}` has been ended.")
        else:
            await update.message.reply_text(f"❌ Error ending session: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def end_all_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = API_URL + "killall"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ All sessions have been ended.")
        else:
            await update.message.reply_text(f"❌ Error ending all sessions: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def pause_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = API_URL + "pauseapp"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"⏸️ Application is now paused.")
        else:
            await update.message.reply_text(f"❌ Error pausing application: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def unpause_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = API_URL + "unpauseapp"

    try:
        response = requests.get(url).json()
        if response.get("success"):
            await update.message.reply_text(f"▶️ Application is now unpaused.")
        else:
            await update.message.reply_text(f"❌ Error unpausing application: {response}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """🤖 **KeyAuth Bot Commands:**
🔹 `/check <key>` – Check if a key is valid
🔹 `/sessions` – Retrieve all active sessions
🔹 `/endsession <session_id>` – End a specific session
🔹 `/endsessions` – End all active sessions
🔹 `/pause` – Pause the application
🔹 `/unpause` – Unpause the application
🔹 `/help` – Show this help message"""
    await update.message.reply_text(help_text)

# Start Telegram bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Register command handlers
app.add_handler(CommandHandler("check", check_license))
app.add_handler(CommandHandler("sessions", retrieve_sessions))
app.add_handler(CommandHandler("endsession", end_session))
app.add_handler(CommandHandler("endsessions", end_all_sessions))
app.add_handler(CommandHandler("pause", pause_application))
app.add_handler(CommandHandler("unpause", unpause_application))
app.add_handler(CommandHandler("help", help_command))

# Run the bot
app.run_polling()

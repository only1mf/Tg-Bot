import requests  
from telegram.ext import Updater, CommandHandler  

API_URL = "https://keyauth.win/api/seller/?sellerkey=YOUR_SELLER_KEY&type=check&key="  
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  

def check_license(update, context):  
    key = ' '.join(context.args)  
    response = requests.get(API_URL + key).json()  
    if response["success"]:  
        update.message.reply_text(f"✅ Key is valid! Expires: {response['expiry']}")  
    else:  
        update.message.reply_text("❌ Invalid or expired key.")  

updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)  
dp = updater.dispatcher  
dp.add_handler(CommandHandler("check", check_license))  

updater.start_polling()  

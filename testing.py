import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your API keys
FACT_CHECK_API_KEY = "YOUR_GOOGLE_FACT_CHECK_API_KEY"
BOT_TOKEN = "7881611515:AAH0frSHiS-1JN0r_Jme_5cYJeNbExhPyJo"

# Function to check news credibility
def check_news(query):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={FACT_CHECK_API_KEY}"
    response = requests.get(url).json()

    if "claims" in response:
        claim = response["claims"][0]
        title = claim["text"]
        rating = claim["claimReview"][0]["textualRating"]
        source = claim["claimReview"][0]["publisher"]["name"]
        link = claim["claimReview"][0]["url"]
        return f"🕵️ **Fact Check Result:**\n📌 *{title}*\n✅ **Rating:** {rating}\n📰 **Source:** {source}\n🔗 [More Info]({link})"
    else:
        return "⚠️ No fact-check data found for this news. Verify from trusted sources!"

# Handle /checknews command
def checknews(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Usage: /checknews [news link or headline]")
        return

    query = " ".join(context.args)
    result = check_news(query)
    update.message.reply_text(result, parse_mode="Markdown")

# Handle /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🕵️ Welcome to Fake News Detector Bot!\nSend a news headline or link using /checknews to verify its credibility.")

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("checknews", checknews, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

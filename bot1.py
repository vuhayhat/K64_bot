# Done! Congratulations on your new bot. You will find it at t.me/K64qbu_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
#
# Use this token to access the HTTP API:
# 8192359925:AAEeuvgX2TwnQi-eEGZg_PXKTNeIS48dgjw
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
# Replace with your Bot Token from BotFather
BOT_TOKEN = '8192359925:AAEeuvgX2TwnQi-eEGZg_PXKTNeIS48dgjw'
REGISTER_FILE = 'register.txt'

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from datetime import datetime



# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me your name, and I'll greet you!")


# Handle Text Messages (User Sends Name)
async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text.strip()
    await update.message.reply_text(f"Hello, {user_name}!")


# Register Command
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "Please provide your name after /register. Example: /register JohnDoe"
        )
        return

    user_name = " ".join(context.args)
    user_id = update.effective_user.id
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write to file
    with open(REGISTER_FILE, "a") as file:
        file.write(f"{user_id}, {user_name}, {current_time}\n")

    await update.message.reply_text(
        f"✅ User '{user_name}' registered at {current_time}"
    )


# Broadcast Command (Admin Only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_ADMIN_USER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "Please provide a message to broadcast. Example: /broadcast Hello everyone!"
        )
        return

    message = " ".join(context.args)
    sent_count = 0

    try:
        with open(REGISTER_FILE, "r") as file:
            for line in file:
                try:
                    user_id = int(line.split(",")[0])
                    await context.bot.send_message(
                        chat_id=user_id, text=f"📢 Broadcast: {message}"
                    )
                    sent_count += 1
                except Exception as e:
                    print(f"Failed to send message to user {user_id}: {e}")

        await update.message.reply_text(f"✅ Broadcast sent to {sent_count} users.")
    except FileNotFoundError:
        await update.message.reply_text("No registered users found.")


# Main Function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_user))

    # Start the Bot
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    YOUR_ADMIN_USER_ID = 5599961581  # Replace with your Telegram user ID
    main()

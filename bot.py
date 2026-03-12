from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

TOKEN = "8769882137:AAENSY3nUv-fE3beMDQpOCmxTaEg1ffeaYw"

WEBSITE = "https://yourwebsite.com"
UPI = "upi://pay?pa=pankajratrey7@axl"
FREEFIRE = "https://yourfreefirepanel.com"

menu = [
    ["👤 My Info", "🌐 Website"],
    ["📥 Download Video", "❓ Help"],
    ["🎮 Free Fire Panel", "💰 UPI Payment"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Welcome to Pankaj Helper Bot\nChoose an option:",
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send a video link from YouTube, Instagram, Facebook etc.\n"
        "Bot will download it."
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"👤 Name: {user.first_name}\n🆔 ID: {user.id}"
    )

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "👤 My Info":
        user = update.message.from_user
        await update.message.reply_text(f"Name: {user.first_name}\nID: {user.id}")

    elif text == "🌐 Website":
        await update.message.reply_text(f"🌐 Visit Website:\n{WEBSITE}")

    elif text == "🎮 Free Fire Panel":
        await update.message.reply_text(f"🎮 Free Fire Panel:\n{FREEFIRE}")

    elif text == "💰 UPI Payment":
        await update.message.reply_text(f"💰 Pay using UPI:\n{UPI}")

    elif text == "❓ Help":
        await update.message.reply_text("Send any video link to download.")

    elif "http" in text:
        await update.message.reply_text("📥 Downloading video...")

        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.%(ext)s'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                file = ydl.prepare_filename(info)

            await update.message.reply_video(open(file, "rb"))

            os.remove(file)

        except Exception as e:
            await update.message.reply_text("❌ Download failed")

    else:
        await update.message.reply_text("🤖 Send a video link to download.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("info", info))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("🤖 Pankaj Helper Bot Running...")
app.run_polling()

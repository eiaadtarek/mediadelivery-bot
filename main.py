import os
import telebot
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط media delivery وسأقوم بتحميله ورفعه لك مباشرة من السحاب.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    if not url.startswith("http"):
        return
    
    msg = bot.reply_to(message, "⏳ جاري جلب وتحميل الفيديو على السيرفر السحابي...")
    
    output_template = "video_%(id)s.%(ext)s"
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'socket_timeout': 30,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        bot.edit_message_text("⬆️ جاري الرفع إلى تليجرام...", message.chat.id, msg.message_id)
        
        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption="✅ تم التحميل بنجاح بدون استهلاك باقتك!")
            
        bot.delete_message(message.chat.id, msg.message_id)
        
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء التحميل أو أن الرابط غير مدعوم.", message.chat.id, msg.message_id)

print("Bot is running...")
bot.infinity_polling()

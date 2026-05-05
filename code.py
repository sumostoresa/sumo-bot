
import json
import os
import asyncio

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

FILE_NAME = "users.json"
COUNTER_FILE = "counter.json"

# 🔴 حط ID القروب هنا
GROUP_ID = -1003996815543  

# 🔴 حط التوكن هنا
TOKEN = "PUT_YOUR_TOKEN_HERE"

# تحميل المستخدمين
def load_users():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}

# حفظ المستخدمين
def save_users(users):
    with open(FILE_NAME, "w") as f:
        json.dump(users, f)

# تحميل العداد
def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            return json.load(f)["count"]
    return 1

# حفظ العداد
def save_counter(count):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)

users = load_users()
counter = load_counter()

# ✅ قائمة
def get_menu():
    return ReplyKeyboardMarkup(
        [
            ["📜 الشروط"],
            ["🔑 الحصول على كود"],
            ["🛒 المتجر"]
        ],
        resize_keyboard=True
    )

# ✅ start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 أهلاً {user.first_name}",
        reply_markup=get_menu()
    )

# ✅ الرسائل
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter

    text = update.message.text
    user = update.effective_user
    user_id = str(user.id)

    username = f"@{user.username}" if user.username else "بدون يوزر"

    # 📜 الشروط
    if text == "📜 الشروط":
        await update.message.reply_text(
            "📜 شروط الاستخدام\n\n✅ 4 طلبات = مجاني\n✅ مرة كل 30 يوم",
            reply_markup=ReplyKeyboardMarkup([["⬅️ رجوع"]], resize_keyboard=True)
        )

    # 🔑 كود
    elif text == "🔑 الحصول على كود":

        if user_id not in users:
            code = f"SUMO{counter}"
            users[user_id] = {"code": code}
            counter += 1
            save_users(users)
            save_counter(counter)
        else:
            code = users[user_id]["code"]

        # ✅ إشعار القروب (سريع بدون تأخير)
        asyncio.create_task(
            context.bot.send_message(
                chat_id=GROUP_ID,
                text=f"""
📥 طلب كود جديد

👤 الاسم: {user.first_name}
🆔 ID: {user_id}
📛 Username: {username}

🔑 الكود: {code}
"""
            )
        )

        await update.message.reply_text(
            f"""
🔑 كودك:

{code}

📢 شاركه الآن 🔥
""",
            reply_markup=ReplyKeyboardMarkup([["⬅️ رجوع"]], resize_keyboard=True)
        )

    # 🛒 المتجر
    elif text == "🛒 المتجر":
        await update.message.reply_text(
            "🛒 متجر سمو:\nhttps://sumo.twsaa.com/",
            reply_markup=ReplyKeyboardMarkup([["⬅️ رجوع"]], resize_keyboard=True)
        )

    # ⬅️ رجوع
    elif text == "⬅️ رجوع":
        await update.message.reply_text(
            "👑 القائمة الرئيسية",
            reply_markup=get_menu()
        )

# ✅ تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ BOT IS RUNNING")

app.run_polling(drop_pending_updates=True)

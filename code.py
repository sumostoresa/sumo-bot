
import json
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

FILE_NAME = "users.json"
COUNTER_FILE = "counter.json"

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

# القائمة الرئيسية
def get_main_menu():
    keyboard = [
        ["📜 الشروط"],
        ["🔑 الحصول على كود"],
        ["🛒 المتجر"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 أهلاً بك في SUMO\n\nاختر من القائمة 👇",
        reply_markup=get_main_menu()
    )

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter

    text = update.message.text
    user_id = str(update.effective_user.id)

    # 📜 الشروط
    if text == "📜 الشروط":
        keyboard = [["⬅️ رجوع"]]
        await update.message.reply_text("""
📜 الشروط – سمو

✅ 4 طلبات = اشتراك مجاني  
✅ مرة كل 30 يوم  
✅ الاشتراك لمدة شهر
""", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    # 🔑 الحصول على كود
    elif text == "🔑 الحصول على كود":

        if user_id not in users:
            code = f"SUMO{counter}"
            users[user_id] = {"code": code}
            counter += 1

            save_users(users)
            save_counter(counter)
        else:
            code = users[user_id]["code"]

        keyboard = [["⬅️ رجوع"]]

        await update.message.reply_text(f"""
🔑 كودك:

{code}

📢 شاركه وابدأ الآن 🔥
""", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    # 🛒 المتجر
    elif text == "🛒 المتجر":
        keyboard = [["⬅️ رجوع"]]
        await update.message.reply_text("""
🛒 متجر سمو

https://sumo.twsaa.com/
""", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    # ⬅️ رجوع
    elif text == "⬅️ رجوع":
        await update.message.reply_text(
            "👑 القائمة الرئيسية",
            reply_markup=get_main_menu()
        )

# تشغيل البوت
app = ApplicationBuilder().token("8787017989:AAEQqjUk7wximKGDVA96XvWg6sHAx6eyOy4").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ BOT IS RUNNING")

app.run_polling()

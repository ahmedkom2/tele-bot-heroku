
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ==== إعدادات البوت ====
BOT_TOKEN = os.environ.get("TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL")

# ==== رسالة الاشتراك ====
subscribe_message = (
    "❌ لا يمكنك استخدام البوت قبل الاشتراك في القناة الرسمية.\n"
    "📲 يرجى الاشتراك أولًا في القناة ثم اضغط على زر 'تحقق من الاشتراك'."
)

# ==== قائمة الخدمات ====
main_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📌 خدمات الرشق", callback_data="rashq")],
    [InlineKeyboardButton("🎮 حسابات ألعاب", callback_data="accounts")],
    [InlineKeyboardButton("💎 شحن ألعاب", callback_data="charge")],
    [InlineKeyboardButton("🛠️ الدعم", callback_data="support")],
])

# ==== تحقق من الاشتراك ====
async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ==== أمر /start ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await is_user_subscribed(user.id, context):
        await update.message.reply_text("مرحباً بك في بوت سلتي 👋\nاختر من القائمة:", reply_markup=main_menu_keyboard)
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📲 الاشتراك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")],
            [InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub")]
        ])
        await update.message.reply_text(subscribe_message, reply_markup=keyboard)

# ==== زر التحقق من الاشتراك ====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "check_sub":
        if await is_user_subscribed(user_id, context):
            await query.edit_message_text("✅ تم التحقق من الاشتراك! اختر من القائمة:", reply_markup=main_menu_keyboard)
        else:
            await query.edit_message_text(subscribe_message, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 الاشتراك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")],
                [InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub")]
            ]))
    elif query.data in ["rashq", "accounts", "charge", "support"]:
        message = f"🆕 طلب جديد من المستخدم: {query.from_user.full_name} (@{query.from_user.username})\n"
        if query.data == "rashq":
            message += "🟣 اختار: خدمات الرشق"
        elif query.data == "accounts":
            message += "🎮 اختار: حسابات ألعاب"
        elif query.data == "charge":
            message += "💎 اختار: شحن ألعاب"
        elif query.data == "support":
            message += "🛠️ طلب دعم"
        await query.edit_message_text("✅ تم إرسال طلبك! سيتم التواصل معك قريبًا.")
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=message)

# ==== تشغيل البوت ====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()

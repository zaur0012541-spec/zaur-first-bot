import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

SERVICES_TEXT = (
    "📚 *Услуги Zaur Academy*\n\n"
    "• Курсы программирования (Python, JavaScript)\n"
    "• Индивидуальные занятия с преподавателем\n"
    "• Подготовка к собеседованиям\n"
    "• Групповые онлайн-занятия\n"
    "• Проектная практика на реальных задачах"
)

PRICES_TEXT = (
    "💰 *Цены Zaur Academy*\n\n"
    "• Групповые занятия — от 5 000 ₽/мес\n"
    "• Индивидуальные занятия — от 2 500 ₽/час\n"
    "• Карьерный коучинг — от 3 000 ₽/сессия\n"
    "• Пробное занятие — *бесплатно*"
)

CONTACTS_TEXT = (
    "📞 *Контакты Zaur Academy*\n\n"
    "🌐 Сайт: zaur.academy\n"
    "📧 Email: info@zaur.academy\n"
    "📱 Telegram: @zaur_academy\n"
    "🕐 Мы на связи пн-пт с 9:00 до 20:00 МСК"
)

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Услуги", callback_data="services")],
        [InlineKeyboardButton("💰 Цены", callback_data="prices")],
        [InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome = (
        "👋 Добро пожаловать в *Zaur Academy*!\n\n"
        "Мы помогаем людям освоить программирование "
        "и построить карьеру в IT.\n\n"
        "Выберите раздел, чтобы узнать подробнее:"
    )
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "services":
        text = SERVICES_TEXT
    elif data == "prices":
        text = PRICES_TEXT
    elif data == "contacts":
        text = CONTACTS_TEXT
    else:
        return
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is not set")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Zaur Academy bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

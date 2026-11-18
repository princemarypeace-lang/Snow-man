import os
import json
import logging
import pathlib

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Forbidden, BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.environ.get("BOT_TOKEN")

# --- EDIT YOUR LINKS AND TEXT HERE ---
REDIRECT_URL = "https://your-shop-link.com"
REVERSE_URL = "https://your-support-link.com" # Change this to your second link

# The message for REDIRECT mode
REDIRECT_TEXT = (
    "Welcome to this bot!\n\n"
    "❄️🌿💊\n"
    "🍀💊🚕\n\n"
    "❄️🍁 jon 💊🍀\n\n"
    "💎❄️ Anni 🍁🌿\n\n"
    "❄️☃️  🌿🌳  🐴🚛  🍄🌈\n\n"
    "Click here to shop now."
)

# The message for REVERSE mode (Telegram ads will see this as a different function)
REVERSE_TEXT = (
    "Welcome to our Support Center!\n\n"
    "If you have any questions or need help with your order, "
    "please click the button below to contact our team."
)

STATE_FILE = pathlib.Path("bot_state.json")


def load_state():
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return data.get("mode", "REDIRECT"), set(data.get("chats", []))
        except Exception as exc:
            logging.warning("Could not read state file: %s", exc)
    return "REDIRECT", set()


def save_state(mode, chats):
    try:
        STATE_FILE.write_text(json.dumps({"mode": mode, "chats": list(chats)}))
    except Exception as exc:
        logging.warning("Could not save state file: %s", exc)


GLOBAL_BOT_MODE, user_chat_ids = load_state()


def set_mode(mode):
    global GLOBAL_BOT_MODE
    GLOBAL_BOT_MODE = mode
    save_state(mode, user_chat_ids)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    chat_id = update.effective_chat.id
    if chat_id not in user_chat_ids:
        user_chat_ids.add(chat_id)
        save_state(GLOBAL_BOT_MODE, user_chat_ids)

    # This is where the magic happens based on the mode
    if GLOBAL_BOT_MODE == "REDIRECT":
        text_to_send = REDIRECT_TEXT
        button_url = REDIRECT_URL
        button_text = "Shop Now 🛒"
    else:
        text_to_send = REVERSE_TEXT
        button_url = REVERSE_URL
        button_text = "Contact Support 💬"

    keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]

    await update.message.reply_text(
        text_to_send,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def change_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    command = update.message.text.strip().upper()

    if command == "REDIRECT":
        set_mode("REDIRECT")
        await update.message.reply_text(
            "✅ REDIRECT MODE ACTIVATED!\n\n"
            "Users will now see the Shop message."
        )
    elif command == "REVERSE":
        set_mode("REVERSE")
        await update.message.reply_text(
            "✅ REVERSE MODE ACTIVATED!\n\n"
            "Users will now see the Support message."
        )


async def redirect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REDIRECT")
    await update.message.reply_text("✅ REDIRECT MODE ACTIVATED!")


async def reverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REVERSE")
    await update.message.reply_text("✅ REVERSE MODE ACTIVATED!")


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    reminder_text = (
        "❄️🍁 jon 💊🍀\n\n\n\n"
        "Don't forget to shop with us today!"
    )

    for chat_id in list(user_chat_ids):
        try:
            await context.bot.send_message(chat_id=chat_id, text=reminder_text)
        except Forbidden:
            user_chat_ids.discard(chat_id)
            save_state(GLOBAL_BOT_MODE, user_chat_ids)
        except BadRequest as exc:
            logging.warning("Bad request for %s: %s", chat_id, exc)
        except Exception as exc:
            logging.error("Transient failure for %s: %s", chat_id, exc)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set!")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("redirect", redirect_command))
    application.add_handler(CommandHandler("reverse", reverse_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, change_mode)
    )

    if application.job_queue is None:
        raise RuntimeError(
            "job_queue is None — install with: pip install \"python-telegram-bot[job-queue]\""
        )

    application.job_queue.run_repeating(
        send_reminder,
        interval=3 * 60 * 60,
        first=10,
    )

    logging.info("Bot started in %s mode", GLOBAL_BOT_MODE)
    application.run_polling()


if __name__ == "__main__":
    main()import os
import json
import logging
import pathlib

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Forbidden, BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.environ.get("BOT_TOKEN")

# --- EDIT YOUR LINKS AND TEXT HERE ---
REDIRECT_URL = "https://your-shop-link.com"
REVERSE_URL = "https://your-support-link.com" # Change this to your second link

# The message for REDIRECT mode
REDIRECT_TEXT = (
    "Welcome to this bot!\n\n"
    "❄️🌿💊\n"
    "🍀💊🚕\n\n"
    "❄️🍁 jon 💊🍀\n\n"
    "💎❄️ Anni 🍁🌿\n\n"
    "❄️☃️  🌿🌳  🐴🚛  🍄🌈\n\n"
    "Click here to shop now."
)

# The message for REVERSE mode (Telegram ads will see this as a different function)
REVERSE_TEXT = (
    "Welcome to our Support Center!\n\n"
    "If you have any questions or need help with your order, "
    "please click the button below to contact our team."
)

STATE_FILE = pathlib.Path("bot_state.json")


def load_state():
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return data.get("mode", "REDIRECT"), set(data.get("chats", []))
        except Exception as exc:
            logging.warning("Could not read state file: %s", exc)
    return "REDIRECT", set()


def save_state(mode, chats):
    try:
        STATE_FILE.write_text(json.dumps({"mode": mode, "chats": list(chats)}))
    except Exception as exc:
        logging.warning("Could not save state file: %s", exc)


GLOBAL_BOT_MODE, user_chat_ids = load_state()


def set_mode(mode):
    global GLOBAL_BOT_MODE
    GLOBAL_BOT_MODE = mode
    save_state(mode, user_chat_ids)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    chat_id = update.effective_chat.id
    if chat_id not in user_chat_ids:
        user_chat_ids.add(chat_id)
        save_state(GLOBAL_BOT_MODE, user_chat_ids)

    # This is where the magic happens based on the mode
    if GLOBAL_BOT_MODE == "REDIRECT":
        text_to_send = REDIRECT_TEXT
        button_url = REDIRECT_URL
        button_text = "Shop Now 🛒"
    else:
        text_to_send = REVERSE_TEXT
        button_url = REVERSE_URL
        button_text = "Contact Support 💬"

    keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]

    await update.message.reply_text(
        text_to_send,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def change_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    command = update.message.text.strip().upper()

    if command == "REDIRECT":
        set_mode("REDIRECT")
        await update.message.reply_text(
            "✅ REDIRECT MODE ACTIVATED!\n\n"
            "Users will now see the Shop message."
        )
    elif command == "REVERSE":
        set_mode("REVERSE")
        await update.message.reply_text(
            "✅ REVERSE MODE ACTIVATED!\n\n"
            "Users will now see the Support message."
        )


async def redirect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REDIRECT")
    await update.message.reply_text("✅ REDIRECT MODE ACTIVATED!")


async def reverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REVERSE")
    await update.message.reply_text("✅ REVERSE MODE ACTIVATED!")


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    reminder_text = (
        "❄️🍁 jon 💊🍀\n\n\n\n"
        "Don't forget to shop with us today!"
    )

    for chat_id in list(user_chat_ids):
        try:
            await context.bot.send_message(chat_id=chat_id, text=reminder_text)
        except Forbidden:
            user_chat_ids.discard(chat_id)
            save_state(GLOBAL_BOT_MODE, user_chat_ids)
        except BadRequest as exc:
            logging.warning("Bad request for %s: %s", chat_id, exc)
        except Exception as exc:
            logging.error("Transient failure for %s: %s", chat_id, exc)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set!")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("redirect", redirect_command))
    application.add_handler(CommandHandler("reverse", reverse_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, change_mode)
    )

    if application.job_queue is None:
        raise RuntimeError(
            "job_queue is None — install with: pip install \"python-telegram-bot[job-queue]\""
        )

    application.job_queue.run_repeating(
        send_reminder,
        interval=3 * 60 * 60,
        first=10,
    )

    logging.info("Bot started in %s mode", GLOBAL_BOT_MODE)
    application.run_polling()


if __name__ == "__main__":
    main()import os
import json
import logging
import pathlib

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Forbidden, BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.environ.get("BOT_TOKEN")

# --- EDIT YOUR LINKS AND TEXT HERE ---
REDIRECT_URL = "https://your-shop-link.com"
REVERSE_URL = "https://your-support-link.com" # Change this to your second link

# The message for REDIRECT mode
REDIRECT_TEXT = (
    "Welcome to this bot!\n\n"
    "❄️🌿💊\n"
    "🍀💊🚕\n\n"
    "❄️🍁 jon 💊🍀\n\n"
    "💎❄️ Anni 🍁🌿\n\n"
    "❄️☃️  🌿🌳  🐴🚛  🍄🌈\n\n"
    "Click here to shop now."
)

# The message for REVERSE mode (Telegram ads will see this as a different function)
REVERSE_TEXT = (
    "Welcome to our Support Center!\n\n"
    "If you have any questions or need help with your order, "
    "please click the button below to contact our team."
)

STATE_FILE = pathlib.Path("bot_state.json")


def load_state():
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return data.get("mode", "REDIRECT"), set(data.get("chats", []))
        except Exception as exc:
            logging.warning("Could not read state file: %s", exc)
    return "REDIRECT", set()


def save_state(mode, chats):
    try:
        STATE_FILE.write_text(json.dumps({"mode": mode, "chats": list(chats)}))
    except Exception as exc:
        logging.warning("Could not save state file: %s", exc)


GLOBAL_BOT_MODE, user_chat_ids = load_state()


def set_mode(mode):
    global GLOBAL_BOT_MODE
    GLOBAL_BOT_MODE = mode
    save_state(mode, user_chat_ids)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    chat_id = update.effective_chat.id
    if chat_id not in user_chat_ids:
        user_chat_ids.add(chat_id)
        save_state(GLOBAL_BOT_MODE, user_chat_ids)

    # This is where the magic happens based on the mode
    if GLOBAL_BOT_MODE == "REDIRECT":
        text_to_send = REDIRECT_TEXT
        button_url = REDIRECT_URL
        button_text = "Shop Now 🛒"
    else:
        text_to_send = REVERSE_TEXT
        button_url = REVERSE_URL
        button_text = "Contact Support 💬"

    keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]

    await update.message.reply_text(
        text_to_send,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def change_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    command = update.message.text.strip().upper()

    if command == "REDIRECT":
        set_mode("REDIRECT")
        await update.message.reply_text(
            "✅ REDIRECT MODE ACTIVATED!\n\n"
            "Users will now see the Shop message."
        )
    elif command == "REVERSE":
        set_mode("REVERSE")
        await update.message.reply_text(
            "✅ REVERSE MODE ACTIVATED!\n\n"
            "Users will now see the Support message."
        )


async def redirect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REDIRECT")
    await update.message.reply_text("✅ REDIRECT MODE ACTIVATED!")


async def reverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REVERSE")
    await update.message.reply_text("✅ REVERSE MODE ACTIVATED!")


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    reminder_text = (
        "❄️🍁 jon 💊🍀\n\n\n\n"
        "Don't forget to shop with us today!"
    )

    for chat_id in list(user_chat_ids):
        try:
            await context.bot.send_message(chat_id=chat_id, text=reminder_text)
        except Forbidden:
            user_chat_ids.discard(chat_id)
            save_state(GLOBAL_BOT_MODE, user_chat_ids)
        except BadRequest as exc:
            logging.warning("Bad request for %s: %s", chat_id, exc)
        except Exception as exc:
            logging.error("Transient failure for %s: %s", chat_id, exc)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set!")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("redirect", redirect_command))
    application.add_handler(CommandHandler("reverse", reverse_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, change_mode)
    )

    if application.job_queue is None:
        raise RuntimeError(
            "job_queue is None — install with: pip install \"python-telegram-bot[job-queue]\""
        )

    application.job_queue.run_repeating(
        send_reminder,
        interval=3 * 60 * 60,
        first=10,
    )

    logging.info("Bot started in %s mode", GLOBAL_BOT_MODE)
    application.run_polling()


if __name__ == "__main__":
    main()import os
import json
import logging
import pathlib

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Forbidden, BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.environ.get("BOT_TOKEN")

# --- EDIT YOUR LINKS AND TEXT HERE ---
REDIRECT_URL = "https://your-shop-link.com"
REVERSE_URL = "https://your-support-link.com" # Change this to your second link

# The message for REDIRECT mode
REDIRECT_TEXT = (
    "Welcome to this bot!\n\n"
    "❄️🌿💊\n"
    "🍀💊🚕\n\n"
    "❄️🍁 jon 💊🍀\n\n"
    "💎❄️ Anni 🍁🌿\n\n"
    "❄️☃️  🌿🌳  🐴🚛  🍄🌈\n\n"
    "Click here to shop now."
)

# The message for REVERSE mode (Telegram ads will see this as a different function)
REVERSE_TEXT = (
    "Welcome to our Support Center!\n\n"
    "If you have any questions or need help with your order, "
    "please click the button below to contact our team."
)

STATE_FILE = pathlib.Path("bot_state.json")


def load_state():
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return data.get("mode", "REDIRECT"), set(data.get("chats", []))
        except Exception as exc:
            logging.warning("Could not read state file: %s", exc)
    return "REDIRECT", set()


def save_state(mode, chats):
    try:
        STATE_FILE.write_text(json.dumps({"mode": mode, "chats": list(chats)}))
    except Exception as exc:
        logging.warning("Could not save state file: %s", exc)


GLOBAL_BOT_MODE, user_chat_ids = load_state()


def set_mode(mode):
    global GLOBAL_BOT_MODE
    GLOBAL_BOT_MODE = mode
    save_state(mode, user_chat_ids)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    chat_id = update.effective_chat.id
    if chat_id not in user_chat_ids:
        user_chat_ids.add(chat_id)
        save_state(GLOBAL_BOT_MODE, user_chat_ids)

    # This is where the magic happens based on the mode
    if GLOBAL_BOT_MODE == "REDIRECT":
        text_to_send = REDIRECT_TEXT
        button_url = REDIRECT_URL
        button_text = "Shop Now 🛒"
    else:
        text_to_send = REVERSE_TEXT
        button_url = REVERSE_URL
        button_text = "Contact Support 💬"

    keyboard = [[InlineKeyboardButton(button_text, url=button_url)]]

    await update.message.reply_text(
        text_to_send,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def change_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    command = update.message.text.strip().upper()

    if command == "REDIRECT":
        set_mode("REDIRECT")
        await update.message.reply_text(
            "✅ REDIRECT MODE ACTIVATED!\n\n"
            "Users will now see the Shop message."
        )
    elif command == "REVERSE":
        set_mode("REVERSE")
        await update.message.reply_text(
            "✅ REVERSE MODE ACTIVATED!\n\n"
            "Users will now see the Support message."
        )


async def redirect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REDIRECT")
    await update.message.reply_text("✅ REDIRECT MODE ACTIVATED!")


async def reverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    set_mode("REVERSE")
    await update.message.reply_text("✅ REVERSE MODE ACTIVATED!")


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    reminder_text = (
        "❄️🍁 jon 💊🍀\n\n\n\n"
        "Don't forget to shop with us today!"
    )

    for chat_id in list(user_chat_ids):
        try:
            await context.bot.send_message(chat_id=chat_id, text=reminder_text)
        except Forbidden:
            user_chat_ids.discard(chat_id)
            save_state(GLOBAL_BOT_MODE, user_chat_ids)
        except BadRequest as exc:
            logging.warning("Bad request for %s: %s", chat_id, exc)
        except Exception as exc:
            logging.error("Transient failure for %s: %s", chat_id, exc)


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set!")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("redirect", redirect_command))
    application.add_handler(CommandHandler("reverse", reverse_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, change_mode)
    )

    if application.job_queue is None:
        raise RuntimeError(
            "job_queue is None — install with: pip install \"python-telegram-bot[job-queue]\""
        )

    application.job_queue.run_repeating(
        send_reminder,
        interval=3 * 60 * 60,
        first=10,
    )

    logging.info("Bot started in %s mode", GLOBAL_BOT_MODE)
    application.run_polling()


if __name__ == "__main__":
    main()

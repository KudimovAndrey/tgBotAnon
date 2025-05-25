from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from config import Config
import json
import logging
import re
from bots.repo.redis.client import RedisClient

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.text and update.message.text.startswith('/'):
            return

        redis = await RedisClient.get_client()
        msg = update.message


        if msg.text:
            sent_message = await context.bot.send_message(
                chat_id=Config.MODERATOR_CHAT_ID,
                text=msg.text,
            )
        else:
            sent_message = await context.bot.send_photo(
                chat_id=Config.MODERATOR_CHAT_ID,
                photo=msg.photo[-1].file_id,
                caption=msg.caption or "",
            )

        keyboard = [
            [
                InlineKeyboardButton("✅ Одобрить", callback_data=f"{sent_message.message_id}:approve"),
                InlineKeyboardButton("❌ Отклонить", callback_data=f"{sent_message.message_id}:reject")
            ]
        ]

        await sent_message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))

        content_data = {
            "type": "text" if msg.text else "photo",
            "content": msg.text if msg.text else None,
            "file_id": msg.photo[-1].file_id if msg.photo else None,
            "caption": msg.caption or "",
        }

        await redis.setex(
            f"submission:{sent_message.message_id}",
            Config.REDIS_TTL,
            json.dumps(content_data)
        )

        await msg.reply_text("✅ Контент отправлен на модерацию!")

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ Произошла ошибка!")


async def handle_moderation_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        redis = await RedisClient.get_client()
        msg_id, action = query.data.split(':', 1)
        content_key = f"submission:{msg_id}"
        
        data = await redis.get(content_key)
        
        if not data:
            await query.edit_message_text("⚠️ Время модерации истекло!")
            return

        try:
            content = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            await query.edit_message_text("❌ Ошибка данных")
            return

        await query.edit_message_reply_markup(reply_markup=None)

        if action == "approve":
            if content.get('type') == "photo":
                await context.bot.send_photo(
                    chat_id=Config.PUBLIC_CHANNEL_ID,
                    photo=content["file_id"],
                    caption=content.get("caption", "")
                )
            else:
                await context.bot.send_message(
                    chat_id=Config.PUBLIC_CHANNEL_ID,
                    text=content["content"]
                )
            await query.message.reply_text("✅ Контент опубликован")
            
        elif action == "reject":
            await query.message.reply_text("❌ Контент отклонен")

        await redis.delete(content_key)

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        await query.edit_message_text("❌ Ошибка при обработке")

def main():
    app = Application.builder().token(Config.TOKEN_MODERATION_BOT).build()
    app.add_handler(MessageHandler(
        (filters.TEXT | filters.PHOTO) & ~filters.COMMAND,
        handle_content
    ))
    app.add_handler(CallbackQueryHandler(handle_moderation_action))
    
    app.run_polling()
    app.add_handler(Application.shutdown(RedisClient.close()))

if __name__ == "__main__":
    main()
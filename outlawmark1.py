from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Document
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import tempfile
import os
import random
import logging
from io import BytesIO

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your token here
TOKEN = "6693711166:AAECSVVIBRJl0NQ2I7WdEDPqxuhWe3YROqQ"

def start(update: Update, context: CallbackContext) -> None:
    gif_urls = ['BQACAgUAAxkBAAIGnGZdzzUt6h9aU9og6SphNqPnvQ2yAAJDEAACdOrwVn0fLyi7fkowNQQ',
'BQACAgUAAxkBAAIGnWZdzzXYSZOX5fH0oxvo1gL5X9MEAAJFEAACdOrwVkI2QSxmI5SjNQQ',
'BQACAgUAAxkBAAIGnmZdzzX7bOjSTP6KfMaHoLATeUaMAAI9EAACdOrwVuyv06qMryZDNQQ',
'BQACAgUAAxkBAAIGn2ZdzzXTcU9BNt8PBeEwx83To1GFAAI-EAACdOrwVjgx0q6lEadqNQQ',
'BQACAgUAAxkBAAIGoGZdzzWdaNi9D14HYuwYsioe2POAAAI7EAACdOrwVmTQoun1iVs_NQQ',
'BQACAgUAAxkBAAIGoWZdzzUcxd1HMf5ziBQ9fkjkieo8AAI8EAACdOrwVhNLzJDpipTVNQQ',
'BQACAgUAAxkBAAIGomZdzzUh8i2LTmLa0ZV4WhbzK1RlAAJBEAACdOrwVgAB3bCjsKwFiDUE',
'BQACAgUAAxkBAAIGo2ZdzzWpI17n5wgckQQF6rK8XjJ9AAI_EAACdOrwVjNznfaQmOBVNQQ',
'BQACAgUAAxkBAAIGpGZdzzV5708SVIEBFWKgr0UWMUnRAAJAEAACdOrwVji1FneqWQEaNQQ',
'BQACAgUAAxkBAAIGpWZdzzWCwB1nMBB_uP9Vnc-eh8CYAAJGEAACdOrwVl-TGHOniU-3NQQ',
'BQACAgUAAxkBAAIGpmZdzzWZ00tfGSDDAAFGLraYof64ogACQhAAAnTq8FYGeo4GpcLN0jUE',
'BQACAgUAAxkBAAIGp2ZdzzX8z9nHQPEHSWUlQXgxxmxIAAJEEAACdOrwVsi5tPXisiiHNQQ']

    # Send GIF with description message
    hello_message="Send me a Document"
    update.message.reply_document(document=random.choice(gif_urls))
    update.message.reply_text(hello_message)

def concatenate_files_msg(context: CallbackContext) -> None:
    document = context.user_data.get('document')
    if not document:
        context.bot.send_message(chat_id=context.user_data.get('chat_id'), text="Please send me a supported document to concatenate.")
        return

    # Download the file to a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, document.file_name)
        document.get_file().download(file_path)

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            concatenated_content = f.read()

    # Split the content into chunks to avoid Telegram's message length limit
    chunk_size = 4096
    chunks = [concatenated_content[i:i+chunk_size] for i in range(0, len(concatenated_content), chunk_size)]

    # Send each chunk as a separate message
    for chunk in chunks:
        context.bot.send_message(chat_id=context.user_data.get('chat_id'), text=chunk)

def concatenate_files_txt(context: CallbackContext) -> None:
    document = context.user_data.get('document')
    if not document:
        context.bot.send_message(chat_id=context.user_data.get('chat_id'), text="Please send me a supported document to concatenate.")
        return

    # Extract the original filename without extension
    original_filename = os.path.splitext(document.file_name)[0]

    # Download the file to a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, document.file_name)
        document.get_file().download(file_path)

        # Read the content of the file
        with open(file_path, 'rb') as f:
            content = f.read()

    # Send the file content back to the user as a document with the new filename
    new_filename = f"{original_filename}.txt"
    context.bot.send_document(chat_id=context.user_data.get('chat_id'), document=BytesIO(content), filename=new_filename)

def callback_query_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    context.user_data['chat_id'] = query.message.chat_id

    if query.data == 'msg':
        concatenate_files_msg(context)
    elif query.data == 'txt':
        concatenate_files_txt(context)

def document_handler(update: Update, context: CallbackContext) -> None:
    context.user_data['document'] = update.message.document
    context.user_data['chat_id'] = update.message.chat_id

    gif_id = 'CgACAgUAAxkBAAIF6mZdvgMDm5h9tLn9PTvQRP1MnHr8AAIbEAACdOrwVpLcMK22vnwaNQQ'


    # Create inline keyboard with the "msg" and "txt" buttons
    keyboard = [
        [
        	InlineKeyboardButton("Message", callback_data='msg'),
        	InlineKeyboardButton("Text File", callback_data='txt'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send GIF with inline keyboard
    update.message.reply_document(document=gif_id, reply_markup=reply_markup)

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
    dispatcher.add_handler(MessageHandler(Filters.document, document_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

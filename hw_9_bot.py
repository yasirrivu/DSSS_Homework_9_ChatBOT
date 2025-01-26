import asyncio
import nest_asyncio
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes,Application
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from typing import Final
import google.generativeai as genai


TELEGRAM_BOT_TOKEN: Final ='7628743941:AAFRKRF_FOxfMtdRZLJ8k9FDwLR8EHB5WlE'
BOT_USERNAME: Final = '@DSSS_yasir_bot'
GEMINI_API_KEY = "AIzaSyBP5A9m3z5taquY6XoIEzAFew01v4x_t1g"


# Apply nest_asyncio for interactive environments
nest_asyncio.apply()


# Gemini API Configuration
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_LLM_MODEL = genai.GenerativeModel("gemini-1.5-flash")


# Function to query Gemini API to use Gemini LLM
def query_gemini(prompt: str) -> str:
    """
    Sends the user input (prompt) to the Gemini API and returns the response.
    """
    response = GEMINI_LLM_MODEL.generate_content(prompt,
                                                 generation_config = genai.GenerationConfig(
                                                     max_output_tokens=1000,
                                                     temperature=0.7)
                                                 ) 
    return response.text



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please types something so i can response.')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = query_gemini(new_text)
        else:
            return 
    else:
        response: str = query_gemini(text)

    print('Bot:', response)
    await update.message.reply_text(response)
    


if __name__ == "__main__":

    print('starting bot....')
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    #Errors
    app.add_error_handler(error)


    print("polling....")
    app.run_polling(poll_interval=3)
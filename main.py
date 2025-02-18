'''Homework 9 DSSS Creating a Telegram bot and implement a LLM'''
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import my_API
from langchain_ollama import OllamaLLM
import torch
# Set up llama3.2
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
model = OllamaLLM(model = 'llama3.2', device = device)

# Import API Key for privacy reasons
TOKEN: Final =  my_API.apiKey
BOT_USERNAME: Final = '@DSSS_HW9_Huber_bot'
# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ''' Response to /start command'''
    await update.message.reply_text('Hello, how can i help you?')
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Response to /help command'''
    await update.message.reply_text('Ask any question to the bot and he will reply')


# Response to User input
def handle_response(text: str) -> str:
    '''Process user messages'''
    processed: str = text.lower()
    # Testing response 
    
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you?' in processed:
        return 'I am good!'
    else:
    # process input with llama
        answer = model.invoke(input=processed)
        return answer

# Check for group or private message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Handle group or private messages'''
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)
# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Handle errors'''
    print(f'Update {update} caused error {context.error}')
# Run bot
if __name__ == '__main__':
    print('Starting bot...')
    # start the bot/app
    app = Application.builder().token(TOKEN).build() 
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # Errors
    app.add_error_handler(error)
    # Polling
    print('Polling...')
    app.run_polling(poll_interval=3)



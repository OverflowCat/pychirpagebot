import google.generativeai as genai
# import PIL
# from PIL import Image
import os
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from reg import get_context_text

generation_config = {
    "temperature": 0.88,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

chats = {}

genai.configure(api_key=os.environ["GEMINI_API_TOKEN"])

def new_gemini_convo():
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
    )
    chat = model.start_chat()
    return chat

async def gemini_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat_id not in chats:
        chats[message.chat_id] = new_gemini_convo()
    chat = chats[message.chat_id]
    text = get_context_text(message)
    if len(chat.history) > 8:
        chat.history = chat.history[2:]
    response = chat.send_message(text, stream=True)
    message = None
    accumulated_text = ""
    using_markdown = True
    for chunk in response:
        accumulated_text += chunk.text
        if message:
            if using_markdown:
                try:
                    await message.edit_text(accumulated_text, parse_mode="MarkdownV2")
                except:
                    using_markdown = False
                    await message.edit_text(accumulated_text)
            else:
                await message.edit_text(accumulated_text)
        else:
            try:
                message = await update.message.reply_markdown_v2(accumulated_text)
            except:
                using_markdown = False
                try:
                    message = await update.message.reply_text(accumulated_text)
                except:
                    return
        print(chunk.text)

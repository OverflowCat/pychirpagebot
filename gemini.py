import google.generativeai as genai
from google.generativeai.types import GenerationConfigType
from PIL import Image
import requests
from io import BytesIO
import os
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from reg import get_context_text

generation_config: GenerationConfigType = {
    "temperature": 0.88,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

chats = {}

genai.configure(api_key=os.environ["GEMINI_API_TOKEN"])


def new_gemini_convo(vision=False):
    model = genai.GenerativeModel(
        model_name="gemini-pro-vision" if vision else "gemini-pro",
        generation_config=generation_config,
    )
    chat = model.start_chat()
    return chat


async def gemini_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return
    if message.chat_id not in chats:
        chats[message.chat_id] = new_gemini_convo()
    chat = chats[message.chat_id]

    input = get_context_text(message)

    if message.photo:
        photo = message.photo[-1]
        photo_file = await photo.get_file()
        if not photo_file.file_path:
            return
        response = requests.get(photo_file.file_path)
        img = Image.open(BytesIO(response.content))
        if input == "":
            input = "Explain this image."
        input = [input, img]
        chat = new_gemini_convo(vision=True)

    if input == "":
        return

    if len(chat.history) > 8:
        chat.history = chat.history[2:]

    response = chat.send_message(input, stream=True)
    reply = None
    accumulated_text = ""
    using_markdown = True
    for chunk in response:
        accumulated_text += chunk.text
        if reply:
            if using_markdown:
                try:
                    await reply.edit_text(accumulated_text, parse_mode="MarkdownV2")
                except:
                    using_markdown = False
                    await reply.edit_text(accumulated_text)
            else:
                await reply.edit_text(accumulated_text)
        else:
            try:
                reply = await message.reply_markdown_v2(accumulated_text, quote=True)
            except:
                using_markdown = False
                try:
                    reply = await message.reply_text(accumulated_text, quote=True)
                except:
                    return
        print(chunk.text)

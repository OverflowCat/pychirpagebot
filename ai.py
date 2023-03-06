from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

import os
import openai

from reg import cutcmd

openai.api_key = os.getenv("OPENAI2")


async def ask_ai(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    prompt = cutcmd(update.message.text)
    print("Asking", prompt + "…")
    messages = [
        # {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "user", "content": "Who won the world series in 2020?"},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": prompt}
    ]

    quote = update.message.reply_to_message or None
    if quote:
        messages.insert(0, {"role": "assistant", "content": quote.text})

    resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    generated = resp["choices"][0]["message"]["content"]
    calc = f"{resp['usage']['prompt_tokens']} + {resp['usage']['completion_tokens']} = {resp['usage']['total_tokens']} tokens"
    try:
        await update.message.reply_markdown(
            generated + f"\n\n__{calc}__",
            quote=True,
        )
    except:  # Markdown 可能无法 parse
        await update.message.reply_text(
            generated + f"\n\n{calc}",
            quote=True,
        )


async def respond_to_ai(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    quote = update.message.reply_to_message or None
    if not (
        quote and quote.from_user.id == 827065789 and quote.text.endswith(" tokens")
    ):
        return False

    print("=== 会话 ===", {"q": quote.from_user.id, "t": quote.text})
    lines = quote.text.splitlines()
    del lines[-2:]
    prev_resp = "\n".join(lines)  # 删除上次回复最后的 token 数量统计

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": prev_resp},
            {"role": "user", "content": update.message.text},
        ],
    )
    print(resp["usage"])
    generated = resp["choices"][0]["message"]["content"]
    calc = f"{resp['usage']['prompt_tokens']} + {resp['usage']['completion_tokens']} = {resp['usage']['total_tokens']} tokens"
    try:
        await update.message.reply_markdown(
            generated + f"\n\n__{calc}__",
            quote=True,
        )
    except:  # Markdown 可能无法 parse
        await update.message.reply_text(
            generated + f"\n\n{calc}",
            quote=True,
        )
    return True

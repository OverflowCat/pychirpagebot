from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

import os
import re
import openai
from duckduckgo_search import ddg

from reg import cutcmd

openai.api_key = os.getenv("OPENAI2")


def limit_string(text):
    text = text.strip()  # Remove any trailing whitespace

    # Split the string into words
    words = re.findall(r"\b\w+\b", text)

    # Count the number of words and CJK characters
    word_count = len(words)
    cjk_count = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")

    if word_count <= 200 and cjk_count <= 100:
        return text
    else:
        # If the string is too long, truncate it and add an ellipsis
        if word_count > 201:
            words = words[:200]
        else:
            # If the string has too many CJK characters, remove the excess
            cjk_chars = []
            for char in text:
                if "\u4e00" <= char <= "\u9fff":
                    cjk_chars.append(char)
                    if len(cjk_chars) == 100:
                        break
            text = "".join(cjk_chars)

        return text + "…"


def search_results_to_text(result) -> str:
    # {'title': str,
    # 'href': str,
    # 'body': str,}
    return result["title"] + "\n" + limit_string(result["body"])


async def ask_ai(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await ctx.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
    )
    prompt = cutcmd(update.message.text)
    print("Asking", prompt + "…")

    if update.message.text.startswith("/net"):
        results = ddg(prompt, region="wt-wt", safesearch="Off", time="y")  # global
        if len(results) > 5:
            results = results[:5]
        print(results)
        messages = [
            {"role": "system", "content": "Analyze given search results and respond."},
            {
                "role": "assistant",
                "content": "\n\n".join(map(search_results_to_text, results)),
            },
            {
                "role": "user",
                "content": f"用中文解释 {prompt}"
                if update.message.text.startswith("/netzh")
                else f"Explain {prompt}",
            },
        ]
    else:
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
    quote = update.message and update.message.reply_to_message or None
    if not (
        quote and quote.from_user.id == 827065789 and quote.text.endswith(" tokens")
    ):
        return False

    await ctx.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
    )
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

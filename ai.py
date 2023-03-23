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


def join_search_results(results) -> str:
    # {'title': str,
    # 'href': str,
    # 'body': str,}
    return "\n\n".join(
        [
            f"""<{i}>: {result["title"]}\n{limit_string(result["body"])}"""
            for i, result in enumerate(results)
        ]
    )


async def ask_ai(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await ctx.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
    )
    prompt = cutcmd(update.message.text)
    print("Asking", prompt + "…")

    lang = "zh" if update.message.text.startswith("/netzh") else ""

    if update.message.text.startswith("/net"):
        messages = [
            {
                "role": "system",
                "content": "Act as a search assistant. Analyze user's query and reply with a search query that can be used in Google to find corresponding results. Reply plain text keywords separated by spaces only, DO NOT EXPLAIN or INSTRUCT.",
            },
            {
                "role": "user",
                "content": "@OverflowCat 是谁？他有啥开源项目？"
                if lang == "zh"
                else "Who's @OverflowCat on GitHub? What projects does he work on?",
            },
            {
                "role": "assistant",
                "content": """@OverflowCat site:github.com""",
            },
            {
                "role": "user",
                "content": "@OverflowCat 是谁？他有啥开源项目？"
                if lang == "zh"
                else "Who's @OverflowCat on GitHub? What projects does he work on?",
            },
            {
                "role": "assistant",
                "content": """@OverflowCat site:github.com""",
            },
            {
                "role": "user",
                "content": "韩剧黑暗荣耀好看吗",
            },
            {"role": "assistant", "content": "黑暗荣耀 韩剧 评价"},
            {
                "role": "user",
                "content": prompt,
            },
        ]
        search_query = prompt
        if False:
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages
                )
                search_query = resp["choices"][0]["message"]["content"]
                print(search_query)
                await update.message.reply_text(
                    f"""{"你好，这是鸭鸭走。现正在搜索" if lang=='zh' else "Hello, this is DuckDuckGo. Now searching"} {search_query}…"""
                )
            except:
                print("Failed to perfrom search query generation.")

        results = ddg(
            search_query, region="wt-wt", safesearch="Off", time="y"
        )  # global
        if results is None or results == [] or len(results) == 0:
            if search_query != prompt:
                results = ddg(prompt, region="wt-wt", safesearch="Off", time="y")
        if len(results) > 5:
            results = results[:5]
        if results is None or results == [] or len(results) == 0:
            await update.message.reply_text("Sorry, no results found on DuckDuckGo.")
            return
        print(results)
        messages = [
            {
                "role": "system",
                "content": "分析搜索结果并回答用户问题。用<1>content</1>等编号标记来源。"
                if lang == "zh"
                else "Analyze given search results and respond. Mark reference using indexes: <1>content</1> etc.",
            },
            {
                "role": "assistant",
                "content": join_search_results(results),
            },
            {
                "role": "user",
                "content": f"根据搜索结果解释回答「{prompt}」" if lang == "zh" else prompt,
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
    quote = update.message.reply_to_message or None
    if not (
        quote
        and quote.from_user.id in [827065789, 6158853909]
        and quote.text is not None
        and quote.text.endswith(" tokens")
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

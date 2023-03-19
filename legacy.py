"""
async def download_video(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    bot = ctx.bot
    sent_message = await update.message.reply_text("Now downloading video…")
    url = cutcmd(update.message.text)  # .lower() Bilibili 的 BV 号是区分大小写的！！
    storage.mkdir("/pan/annie/temp/")
    fid = reg.id_generator(4)
    storage.mkdir(f"/pan/annie/temp/{fid}/")
    command = f'/pan/annie/annie -o "/pan/annie/temp/{fid}/" "{url}"'
    print(command)
    os.system(command)
    # f'/pan/annie/annie -o "/pan/annie/temp/{fid}/" "{url}"'

    files = os.listdir(f"/pan/annie/temp/{fid}/")
    for f in files:
        location = f"/pan/annie/temp/{fid}/{f}"
        await sent_message.edit_text(f"Location: {location}")
        await bot.send_video(
            chat_id=update.message.chat_id,
            video=open(location, "rb"),
            supports_streaming=True,
        )
        # TODO: Files > 50 MB cannot be sent by bot directly!
        storage.rm(f"/pan/annie/temp/{fid}")
        return

async def pagesTweets(tweets, **pa):
  counter = 0
  outputTweets = []
  graves = []
  for t in tweets:
    counter += 1
    if counter%60 == 0:
      # New page!
      graves.append(await dealWithTweets(outputTweets, pa))
    else:
      outputTweets.append(t)
  return graves
"""
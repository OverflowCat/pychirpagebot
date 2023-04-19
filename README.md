# Chirpage Bot

## Instance

[`@pychirpagebot`](https://t.me/pychirpagebot)

## Development

Recommended Python virsion: `3.10`+

### Install dependencies

```py
poetry install
```

### Add tokens

```dotenv
T1=Twitter OAuth token 
T2=Twitter OAuth token
T3=Twitter access token
T4=Twitter access token
CHIRPAGE1=bot token 1
POETOKEN=see poe-api repo
OPENAI2=OpenAI SDK
CHIRPAGE_BOT_ADMIN_ID=405582582

# Optional
CHIRPAGE2=bot token 2 # Run different bot instances using args 1, 2, 3...
CHSHDB=https://sheetdb.io/api/v1/[数据删除]
PYCMYSQLHOST=[example].com
PYCMYSQLUSER=
PYCMYSQLPWD=

```

### Run

```py
poetry run python main.py 1
```

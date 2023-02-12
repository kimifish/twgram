import os
LANG = 'ru'
EMOTICONS_ENABLED = True
TAG_LIST_COLS = 3
PROJECT_LIST_COLS = 2
TZONE = 'Europe/Moscow'

# Telegram Bot
TG_API_ID = os.environ.get("TG_API_ID", "")
TG_API_HASH = os.environ.get("TG_API_HASH", "")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# TaskWarrior
# For the purpose of multiuser/multitasks
# Dict key must be your telegram username below
TW_CONFIG_FILE = {'kimifish': '/home/kimifish/.taskrc',
                  # 'some_user': '/home/somebody_else/.taskrc',
                  }
TW_BINARY = '/usr/local/bin/task'

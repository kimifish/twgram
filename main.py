import logging
from config import TG_BOT_TOKEN, TG_API_ID, TG_API_HASH
from tg.utils import TgClient

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


app = TgClient(name='twgram',
               bot_token=TG_BOT_TOKEN,
               api_id=TG_API_ID,
               api_hash=TG_API_HASH,
               workers=50,
               plugins=dict(root="tg/plugins")
               )

app.run()  # Automatically start() and idle()

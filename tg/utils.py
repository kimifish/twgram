import logging

from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

import tw

log = logging.getLogger(__name__)


class TgClient(Client):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.chats_dict: {str: int} = {}
        self.tw_clients_dict = {}
        self.msg_stack = {}


async def refresh_task(tg_client: TgClient,
                       q: CallbackQuery = None,
                       full_info: bool = False,
                       show_due: bool = False,
                       show_priority: bool = False,
                       show_status: bool = False,
                       show_tags: bool = False,
                       show_project: bool = False,
                       task_uuid: str = None,
                       use_alt_kbd: InlineKeyboardMarkup = None) -> bool:
    if q and not task_uuid:
        task_uuid = q.data.split('%')[1]
    description, keyboard = tw.format_task(client=tg_client.tw_clients_dict[q.from_user.username],
                                           task_uuid=task_uuid,
                                           full_info=full_info,
                                           show_due=show_due,
                                           show_status=show_status,
                                           show_priority=show_priority,
                                           show_tags=show_tags,
                                           show_project=show_project,
                                           ).values()
    if use_alt_kbd:
        keyboard = use_alt_kbd
    try:
        await q.message.edit_text(text=description)
        await q.message.edit_reply_markup(reply_markup=keyboard)
        return True
    except Exception as e:
        log.error(e)
        return False

import logging

from dateutil.tz import tz
from pyrogram import Client
from pyrogram.types import CallbackQuery

import tg.filters as bot_filters
import tg.keyboards as kbd
import tw
from config import TZONE
from tg.utils import refresh_task, TgClient
from utils.message_stack import clear_lists
from utils.simple_calendar import SimpleCalendar, calendar_callback
from utils.translations import k

log = logging.getLogger(__name__)


@Client.on_callback_query(bot_filters.tag_list_filter)
async def get_list_by_tag(client: TgClient, q: CallbackQuery):
    username = q.from_user.username
    tw_client = client.tw_clients_dict[username]
    await clear_lists(client, username, 'tags', except_first=True)
    tag = str(q.data).split('%')[1]
    task_list = tw.get_list_by_tag(tw_client, tag)
    reply = await q.message.reply(f'{k.Tasks_for_tag} "{tag}":')
    client.msg_stack[username]['tags'][str(q.message.id)].append(reply.id)
    for t in task_list:
        reply = await q.message.reply(**tw.format_task(client=tw_client, task=t))
        client.msg_stack[username]['tags'][str(q.message.id)].append(reply.id)
    await q.answer()


@Client.on_callback_query(bot_filters.project_list_filter)
async def get_list_by_project(client: TgClient, q: CallbackQuery):
    username = q.from_user.username
    tw_client = client.tw_clients_dict[username]
    await clear_lists(client, username, 'projects', except_first=True)
    project = str(q.data).split('%')[1]
    task_list = tw.get_list_by_project(tw_client, project)
    reply = await q.message.reply(f'{k.Tasks_in_project} "{project}":')
    client.msg_stack[username]['projects'][str(q.message.id)].append(reply.id)
    for t in task_list:
        reply = await q.message.reply(**tw.format_task(client=tw_client, task=t))
        client.msg_stack[username]['projects'][str(q.message.id)].append(reply.id)
    await q.answer()


@Client.on_callback_query(bot_filters.task_complete_filter)
async def task_complete(client: TgClient, q: CallbackQuery):
    log.debug(f'task_complete')
    task_uuid = q.data.split('%')[1]
    if tw.complete_task(client.tw_clients_dict[q.from_user.username], task_uuid):
        await q.answer(f'{k.Task_completed}.')
        await refresh_task(client, q, task_uuid=task_uuid)
    else:
        await q.answer(f'{k.Error_while_completing_task}.')


@Client.on_callback_query(bot_filters.task_complete_undo_filter)
async def task_complete_undo(client: TgClient, q: CallbackQuery):
    task_uuid = q.data.split('%')[1]
    if tw.set_task_pending(client.tw_clients_dict[q.from_user.username], task_uuid):
        await q.answer(f'{k.Completion_canceled}.')
        await refresh_task(client, q, task_uuid=task_uuid)
    else:
        await q.answer(f'{k.Error_while_canceling_previous_action}.')


@Client.on_callback_query(bot_filters.task_delete_filter)
async def task_delete(client: TgClient, q: CallbackQuery):
    task_uuid = q.data.split('%')[1]
    if tw.delete_task(client.tw_clients_dict[q.from_user.username], task_uuid):
        await q.answer(f'{k.Task_deleted}.')
        await refresh_task(client, q, task_uuid=task_uuid)
    else:
        await q.answer(f'{k.Error_while_deleting_task}.')


@Client.on_callback_query(bot_filters.task_delete_undo_filter)
async def task_delete_undo(client: TgClient, q: CallbackQuery):
    task_uuid = q.data.split('%')[1]
    if tw.set_task_pending(client.tw_clients_dict[q.from_user.username], task_uuid):
        await q.answer(f'{k.Deletion_canceled}.')
        await refresh_task(client, q, task_uuid=task_uuid)
    else:
        await q.answer(f'{k.Error_while_canceling_previous_action}.')


@Client.on_callback_query(bot_filters.task_info_filter)
async def task_info(client: TgClient, q: CallbackQuery):
    task_uuid = q.data.split('%')[1]
    await refresh_task(client, q, full_info=True, task_uuid=task_uuid,
                       use_alt_kbd=kbd.task_info_kbd(client.tw_clients_dict[q.from_user.username].get(task_uuid)))


@Client.on_callback_query(bot_filters.task_info_hide_filter)
async def task_info_hide(client: TgClient, q: CallbackQuery):
    log.info(f'task_info_hide')
    await refresh_task(client, q)


@Client.on_callback_query(bot_filters.task_modify_filter)
async def task_modify(client: TgClient, q: CallbackQuery):
    log.info(f'task_modify')
    task_uuid = q.data.split('%')[1]
    await refresh_task(client, q, task_uuid=task_uuid, use_alt_kbd=kbd.modify_task_kbd(task_uuid=task_uuid))


@Client.on_callback_query(bot_filters.task_modify_finish_filter)
async def task_modify_finish(client: TgClient, q: CallbackQuery):
    await refresh_task(client, q)


@Client.on_callback_query(bot_filters.task_modify_tags_filter)
async def task_modify_tags(client: TgClient, q: CallbackQuery):
    log.info(f'task_modify_tags: {q.data}')
    task_uuid = q.data.split('%')[1]
    alt_kbd = kbd.modify_tags_kbd(button_list=tw.tags_list(client.tw_clients_dict[q.from_user.username]),
                                  active_tags_list=client.tw_clients_dict[q.from_user.username].get(
                                      uuid=task_uuid).tags,
                                  task_uuid=task_uuid,
                                  )
    pass
    await refresh_task(client, q,
                       task_uuid=task_uuid,
                       use_alt_kbd=alt_kbd,
                       show_tags=True,
                       )


@Client.on_callback_query(bot_filters.task_modify_priority_filter)
async def task_modify_priority(client: TgClient, q: CallbackQuery):
    task_uuid = q.data.split('%')[1]
    await refresh_task(client, q,
                       task_uuid=task_uuid,
                       use_alt_kbd=kbd.modify_priority_kbd(task_uuid),
                       show_priority=True,
                       )


@Client.on_callback_query(bot_filters.task_modify_due_filter)
async def task_modify_due(client: TgClient, q: CallbackQuery):
    task_uuid = q.data.split('%')[1]
    reply_markup = await SimpleCalendar().start_calendar(task_uuid)
    await refresh_task(client, q,
                       task_uuid=task_uuid,
                       use_alt_kbd=reply_markup,
                       show_due=True,
                       )


@Client.on_callback_query(bot_filters.tag_switch_filter)
async def tag_switch(client: TgClient, q: CallbackQuery):
    username = q.from_user.username
    log.info(f'tag_switch')
    _, task_uuid, tag_pressed = q.data.split('%')
    if tw.switch_tag(client.tw_clients_dict[username], task_uuid=task_uuid, tag=tag_pressed):
        await refresh_task(client, q,
                           task_uuid=task_uuid,
                           use_alt_kbd=kbd.modify_tags_kbd(button_list=tw.tags_list(client.tw_clients_dict[username]),
                                                           active_tags_list=client.tw_clients_dict[username].get(
                                                               uuid=task_uuid).tags,
                                                           task_uuid=task_uuid,
                                                           ),
                           show_tags=True
                           )
    else:
        await q.answer(k.Error_while_changing_tag)


@Client.on_callback_query(bot_filters.priority_change_filter)
async def priority_change(client: TgClient, q: CallbackQuery):
    _, task_uuid, priority_pressed = q.data.split('%')
    if tw.change_priority(client.tw_clients_dict[q.from_user.username], task_uuid, priority=priority_pressed):
        await refresh_task(client, q, task_uuid=task_uuid, use_alt_kbd=kbd.modify_task_kbd(task_uuid=task_uuid))
    else:
        await q.answer(k.Error_while_changing_priority)


@Client.on_callback_query(bot_filters.simple_calendar_filter)
async def simple_calendar(client: TgClient, q: CallbackQuery):
    data = calendar_callback.parse(q.data)
    selected, date = await SimpleCalendar().process_selection(q, data)
    if selected:
        if tw.change_due(client.tw_clients_dict[q.from_user.username],
                         data['uuid'],
                         date.astimezone(tz=tz.gettz(TZONE))):
            await refresh_task(client, q, task_uuid=data['uuid'],
                               use_alt_kbd=kbd.modify_task_kbd(task_uuid=data['uuid']))

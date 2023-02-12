import datetime

from pyrogram import Client as Tg_Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove
from pytz import utc

import tg.filters as bot_filters
import tw
import tg.keyboards as kbd
from tg.utils import TgClient
from utils.message_stack import clear_lists
from utils.translations import k


@TgClient.on_message((filters.command(k.start, prefixes='') & filters.private) |
                     (filters.command('start')) & filters.private)
async def start(client: TgClient, message: Message):
    username = message.from_user.username
    client.chats_dict[username] = message.chat.id  # TODO: No multiuser for now
    client.tw_clients_dict[username] = tw.init(username)
    client.msg_stack[username] = {'tags': {}, 'projects': {}, 'today': {}, 'overdue': {}, }
    await message.reply(k.Hello, reply_markup=kbd.main_kbd)


@TgClient.on_message(filters.command(k.New_task, prefixes='') & filters.private)
async def new_task(client: Tg_Client, message: Message):
    await message.reply(f'{k.Enter_new_task_description}:', reply_markup=ReplyKeyboardRemove)


@TgClient.on_message(bot_filters.new_task_description_filter)
async def new_task_description(client: TgClient, message: Message):
    username = message.from_user.username
    tw_client = client.tw_clients_dict[username]
    task = tw.new_task(tw_client, message.text)
    text_markup = tw.format_task(tw_client, task=task, show_status=True)
    await message.reply(text=text_markup['text'], reply_markup=kbd.modify_task_kbd(task_uuid=task.uuid))


@TgClient.on_message(filters.command(k.Overdue, prefixes='') & filters.private)
async def overdue(client: TgClient, message: Message):
    username = message.from_user.username
    tw_client = client.tw_clients_dict[username]
    await clear_lists(client, username)
    overdue_list = tw.get_overdue_tasks(tw_client)
    if len(overdue_list) == 0:
        await message.reply(f'{k.No_overdue_tasks}.')
        return
    for t in overdue_list:
        if t.due and t.due < utc.localize(datetime.datetime.now()):
            reply = await message.reply(**tw.format_task(client=tw_client, task=t))
            client.msg_stack[username]['overdue'][str(reply.id)] = [reply.id]


@TgClient.on_message(filters.command(k.Today, prefixes='') & filters.private)
async def today_tasks(client: TgClient, message: Message):
    username = message.from_user.username
    tw_client = client.tw_clients_dict[username]
    await clear_lists(client, username)
    tasks = tw.get_today_tasks(tw_client)
    if len(tasks) == 0:
        reply = await message.reply(f'{k.No_tasks_today}.')
        client.msg_stack[username]['today'][str(reply.id)] = [reply.id]
        return
    for t in tasks:
        if t.due and t.due < utc.localize(datetime.datetime.now()):
            reply = await message.reply(**tw.format_task(tw_client, task=t))
            client.msg_stack[username]['today'][str(reply.id)] = [reply.id]


@TgClient.on_message(filters.command(k.Tags, prefixes='') & filters.private)
async def tags(client: TgClient, message: Message):
    username = message.from_user.username
    tw_client = client.tw_clients_dict[username]
    await clear_lists(client, username)
    reply = await message.reply(f'{k.Choose_tag}:',
                                reply_markup=kbd.tag_list_kbd(tw.tags_list(tw_client)))
    client.msg_stack[username]['tags'][str(reply.id)] = [reply.id]


@TgClient.on_message(filters.command(k.Projects, prefixes='') & filters.private)
async def projects(client: TgClient, message: Message):
    username = message.from_user.username
    tw_client = client.tw_clients_dict[username]
    await clear_lists(client, username)
    reply = await message.reply(f'{k.Choose_project}:', reply_markup=kbd.project_list_kbd(
        tw.projects_list(tw_client)))
    client.msg_stack[username]['projects'][str(reply.id)] = [reply.id]

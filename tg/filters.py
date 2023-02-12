from pyrogram import filters
from pyrogram.types import Message
from config import LANG
from utils.translations import translations
import logging

log = logging.getLogger(__name__)


async def filter_tag_query(_, __, query):
    return str(query.data).startswith('tag%')


async def filter_project_query(_, __, query):
    return str(query.data).startswith('project%')


async def filter_task_complete_query(_, __, query):
    return str(query.data).startswith('task_complete%')


async def filter_task_modify_query(_, __, query):
    return str(query.data).startswith('task_modify%')


async def filter_task_complete_undo_query(_, __, query):
    return str(query.data).startswith('task_complete_undo%')


async def filter_task_info_query(_, __, query):
    return str(query.data).startswith('task_info%')


async def filter_task_info_hide_query(_, __, query):
    return str(query.data).startswith('task_info_hide%')


async def filter_task_delete_query(_, __, query):
    return str(query.data).startswith('task_delete%')


async def filter_task_delete_undo_query(_, __, query):
    return str(query.data).startswith('task_delete_undo%')


async def filter_task_modify_tags_query(_, __, query):
    return str(query.data).startswith('mod_tags%')


async def filter_task_modify_project_query(_, __, query):
    return str(query.data).startswith('mod_project%')


async def filter_task_modify_priority_query(_, __, query):
    return str(query.data).startswith('mod_priority%')


async def filter_task_modify_due_query(_, __, query):
    return str(query.data).startswith('mod_due%')


async def filter_task_modify_finish_query(_, __, query):
    return str(query.data).startswith('mod_finish%')


async def filter_tag_switch_query(_, __, query):
    return str(query.data).startswith('tag_switch%')


async def filter_priority_change_query(_, __, query):
    return str(query.data).startswith('priority_change%')


async def filter_simple_calendar_query(_, __, query):
    return str(query.data).startswith('scl:')


async def filter_new_task_description(_, __, message: Message):
    return not message.text.lower() in translations[LANG].values()


tag_list_filter = filters.create(filter_tag_query)
project_list_filter = filters.create(filter_project_query)
task_info_filter = filters.create(filter_task_info_query)
task_info_hide_filter = filters.create(filter_task_info_hide_query)
task_complete_filter = filters.create(filter_task_complete_query)
task_complete_undo_filter = filters.create(filter_task_complete_undo_query)
task_delete_filter = filters.create(filter_task_delete_query)
task_delete_undo_filter = filters.create(filter_task_delete_undo_query)
new_task_description_filter = filters.create(filter_new_task_description)
task_modify_filter = filters.create(filter_task_modify_query)
task_modify_tags_filter = filters.create(filter_task_modify_tags_query)
task_modify_project_filter = filters.create(filter_task_modify_project_query)
task_modify_priority_filter = filters.create(filter_task_modify_priority_query)
task_modify_due_filter = filters.create(filter_task_modify_due_query)
task_modify_finish_filter = filters.create(filter_task_modify_finish_query)
tag_switch_filter = filters.create(filter_tag_switch_query)
priority_change_filter = filters.create(filter_priority_change_query)
simple_calendar_filter = filters.create(filter_simple_calendar_query)

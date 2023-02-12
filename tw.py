import datetime
import logging
from typing import List

from dateutil.tz import tz
from taskwarrior import Client, Task, Q

from config import TW_CONFIG_FILE, TW_BINARY, TZONE
from tg import keyboards as kbd
from utils.translations import k

log = logging.getLogger(__name__)


def init(username: str):
    client = Client(config_filename=TW_CONFIG_FILE[username],
                    task_bin=TW_BINARY,
                    )
    # global clients
    # clients[username] = client
    return client


def get_overdue_tasks(client):
    l = client.filter(Q(status='pending', due__before=datetime.datetime.now() + datetime.timedelta(days=1)))
    return l


def get_today_tasks(client):
    l = client.filter(Q(status='pending', due=datetime.datetime.now().date()))
    return l


def tags_list(client: Client):
    raw_tags_list = client._execute('tags')[0].split('\n')[2:]
    tags_list = []
    for e in raw_tags_list:
        if not e:
            continue
        tags_list.append(e.split())
    return tags_list


def projects_list(client: Client):
    raw_projects_list = client._execute('projects')[0].split('\n')[2:-2]
    projects_list = []
    for e in raw_projects_list:
        if not e:
            continue
        projects_list.append(e.split())
    return projects_list


def get_list_by_tag(client: Client, tag: str):
    l = client.filter(Q(tag__contains=tag) & Q(status='pending'))
    return l


def get_list_by_project(client: Client, project: str):
    l = client.filter(Q(project=project) & Q(status='pending'))
    return l


def complete_task(client: Client, task_uuid):
    task = client.get(uuid=task_uuid)
    task.status = 'completed'
    client.modify(task)
    task = client.get(uuid=task_uuid)
    return task.status == 'completed'


def delete_task(client: Client, task_uuid):
    task = client.get(uuid=task_uuid)
    client.delete(task)
    task = client.get(uuid=task_uuid)
    return task.status == 'deleted'


def set_task_pending(client: Client, task_uuid):
    task = client.get(uuid=task_uuid)
    task.status = 'pending'
    client.modify(task)
    task = client.get(uuid=task_uuid)
    return task.status == 'pending'


def new_task(client: Client, description):
    task = Task(description=description)
    task.status = 'pending'
    task.due = datetime.datetime.now(tz=tz.gettz(TZONE)) + datetime.timedelta(days=1)
    client.add(task)
    return task


def switch_tag(client: Client, task_uuid, tag):
    task = client.get(task_uuid)
    tags = task.tags
    if not tags:
        tags = []
        task.tags = []

    try:
        if tag in tags:
            task.tags.remove(tag)
        else:
            task.tags.append(tag)
        client.modify(task)
    except Exception as e:
        log.error(e)
        return False
    return True


def change_priority(client: Client, task_uuid, priority):
    task = client.get(task_uuid)
    try:
        old_priority = task.priority
    except AttributeError:
        old_priority = None
    if priority != old_priority:
        task.priority = priority
    client.modify(task)
    return True


def change_due(client: Client, task_uuid, due):
    task = client.get(task_uuid)
    try:
        old_due = task.due
    except AttributeError:
        old_due = None
    if due != old_due:
        task.due = due
    client.modify(task)
    return True


def format_task(client: Client,
                task: Task = None,
                task_uuid: str = None,
                full_info=False,
                show_due=False,
                show_priority=False,
                show_tags=False,
                show_status=False,
                show_project=False,
                ) -> dict:
    if not task:
        task = client.get(uuid=str(task_uuid))
    if task.id != 0:
        if full_info:
            text = f'[`{task.id}`] **{task.description}**\n'
        else:
            text = f'`•` **{task.description}**\n'
    else:
        if task.status == 'deleted':
            text = f'`X` <s>{task.description}</s>\n'
        elif task.status == 'completed':
            text = f'`V` {task.description}\n'
        else:
            text = None
    if full_info:
        text += '\n'
        if task.annotations:
            text += f'<i>{task.annotations}</i>'
        if task.urgency:
            text += f'{k.Urgency}: `{task.urgency}`\n'
    if show_status or full_info:
        text += f'{k.Status}: `{task.status}`\n'
    if show_priority or full_info:
        try:
            text += f'{k.Priority}: `{task.priority}`\n'
        except AttributeError:
            log.warning(f'No priority in task [{task.id}].')
    if show_project or full_info:
        if task.project:
            text += f'{k.Project}: `{task.project}`\n'
    if show_tags or full_info:
        if task.tags:
            text += f'{k.Tags}: `{", ".join(task.tags)}`\n'
    if show_due or full_info:
        if task.due:
            text += f'{k.Due}: `{task.due.astimezone(tz=tz.gettz(TZONE)).strftime("%d.%m.%y %H:%M")}`\n'
    if full_info:
        text += f'UUID: `{task.uuid}`\n'

        inline_kbd = kbd.task_info_kbd(task)
    else:
        inline_kbd = kbd.task_kbd(task)
    return {'text': text, 'reply_markup': inline_kbd}

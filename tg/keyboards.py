from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from utils.translations import k
from config import TAG_LIST_COLS, PROJECT_LIST_COLS
from taskwarrior import Task

main_kbd = ReplyKeyboardMarkup([
    [
        KeyboardButton(text=k.Overdue),
        KeyboardButton(text=k.Tags),
        KeyboardButton(text=k.Projects),
    ], [
        KeyboardButton(text=k.Today),
        KeyboardButton(text=k.New_task),

    ]
],
    is_persistent=True,
    resize_keyboard=True
)


def modify_task_kbd(task_uuid: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=k.Add_tags, callback_data=f'mod_tags%{task_uuid}'),
        ], [
            InlineKeyboardButton(text=k.Add_to_project, callback_data=f'mod_project%{task_uuid}'),
        ], [
            InlineKeyboardButton(text=k.Change_priority, callback_data=f'mod_priority%{task_uuid}'),
        ], [
            InlineKeyboardButton(text=k.Change_due_date, callback_data=f'mod_due%{task_uuid}'),
        ], [
            InlineKeyboardButton(text=k.Finish, callback_data=f'mod_finish%{task_uuid}'),
        ],
    ])


def task_kbd(task: Task) -> InlineKeyboardMarkup:
    if task.status == 'pending':
        kbd = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(k.Delete, callback_data=f'task_delete%{task.uuid}'),
                InlineKeyboardButton(k.Modify, callback_data=f'task_modify%{task.uuid}'),
                InlineKeyboardButton(k.Done, callback_data=f'task_complete%{task.uuid}'),
                InlineKeyboardButton(k.info, callback_data=f'task_info%{task.uuid}'),
            ],
        ])
    elif task.status == 'deleted':
        kbd = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(k.Undo, callback_data=f'task_delete_undo%{task.uuid}'),
                InlineKeyboardButton(k.Modify, callback_data=f'task_modify%{task.uuid}'),
                InlineKeyboardButton(k.info, callback_data=f'task_info%{task.uuid}'),
            ],
        ])
    elif task.status == 'completed':
        kbd = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(k.Undo, callback_data=f'task_delete_undo%{task.uuid}'),
                InlineKeyboardButton(k.Modify, callback_data=f'task_modify%{task.uuid}'),
                InlineKeyboardButton(k.info, callback_data=f'task_info%{task.uuid}'),
            ],
        ])
    else:
        kbd = None
    return kbd


def task_info_kbd(task: Task) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(k.Back, callback_data=f'task_info_hide%{task.uuid}')
    ]])


def tag_list_kbd(button_list: list):
    return InlineKeyboardMarkup(
        _format_buttons_from_lists(button_list,
                                   show_numbers=True,
                                   action_template='tag',
                                   cols=TAG_LIST_COLS,
                                   )
    )


def project_list_kbd(button_list: list):
    return InlineKeyboardMarkup(
        _format_buttons_from_lists(button_list,
                                   show_numbers=True,
                                   action_template='project',
                                   cols=PROJECT_LIST_COLS,
                                   )
    )


def modify_tags_kbd(button_list: list, active_tags_list: list, task_uuid: str):
    kbd = _format_buttons_from_lists(button_list=button_list,
                                     already_active_list=active_tags_list,
                                     action_template=f'tag_switch%{task_uuid}',
                                     cols=TAG_LIST_COLS
                                     )
    kbd.append(
        [InlineKeyboardButton(k.Complete,
                              callback_data=f'task_modify%{task_uuid}')])
    return InlineKeyboardMarkup(kbd)


def modify_priority_kbd(task_uuid: str):
    action = f'priority_change%{task_uuid}'
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(k.High, callback_data=f'{action}%H')],
         [InlineKeyboardButton(k.Medium, callback_data=f'{action}%M')],
         [InlineKeyboardButton(k.Low, callback_data=f'{action}%L')],
         ]
    )

def modify_due_kbd():
    pass


def _format_buttons_from_lists(button_list: list,
                               show_numbers=False,
                               already_active_list: list = None,
                               action_template: str = '',
                               cols=3):
    new_list = [[]]
    i = 0
    for l in button_list:
        tag_btn = l[0]
        if already_active_list and l[0] in already_active_list:
            tag_btn = f'【 {l[0]} 】'
        if show_numbers:
            tag_btn = f'{tag_btn} ({l[1]})'
        if len(new_list[i]) == cols:
            new_list.append([])
            i += 1
        new_list[i].append(InlineKeyboardButton(tag_btn, callback_data=f'{action_template}%{l[0]}'))
    return new_list

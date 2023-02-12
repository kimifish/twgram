from config import LANG, EMOTICONS_ENABLED

translations = {
    'ru': {
        'back': 'назад',
        'delete': 'удалить',
        'modify': 'изменить',
        'done': 'выполнить',
        'info': 'инфо',
        'undo': 'отменить',
        'hello': 'привет',
        'start': 'старт',
        'new_task': 'новая задача',
        'overdue': 'просрочка',
        'today': 'сегодня',
        'tags': 'тэги',
        'projects': 'проекты',
        'project': 'проект',
        'no_tasks': 'задач нет.',
        'status': 'cтатус',
        'due': 'срок',
        'urgency': 'срочность',
        'priority': 'приоритет',
        'enter_new_task_description': 'введите описание новой задачи',
        'choose_tag': 'выберите тэг',
        'choose_project': 'выберите проект',
        'tasks_for_tag': 'задачи с тэгом',
        'tasks_in_project': 'задачи проекта',
        'task_completed': 'задача выполнена',
        'error_while_completing_task': 'ошибка при изменении статуса задачи',
        'completion_canceled': 'завершение отменено',
        'task_deleted': 'задача удалена',
        'error_while_deleting_task': 'ошибка при удалении задачи',
        'deletion_canceled': 'удаление отменено',
        'error_while_canceling_previous_action': 'ошибка при отмене предыдущего действия',
        'no_tasks_today': 'на сегодня задач нет',
        'add_tags': 'изменить тэги',
        'add_to_project': 'добавить в проект',
        'change_priority': 'изменить приоритет',
        'change_due_date': 'изменить дату',
        'finish': 'закончить',
        'complete': 'завершить',
        'error_while_changing_tag': 'ошибка при изменении тэга',
        'error_while_changing_priority': 'ошибка при изменении приоритета',
        'high': 'высокий',
        'medium': 'средний',
        'low': 'низкий',
        'no_overdue_tasks': 'просроченных задач нет',
    },
    'en': {
        'back': 'back',
        'delete': 'delete',
        'modify': 'modify',
        'done': 'done',
        'info': 'info',
        'undo': 'undo',
        'hello': 'hello',
        'start': 'start',
        'new_task': 'new task',
        'overdue': 'overdue',
        'today': 'today',
        'tags': 'tags',
        'projects': 'projects',
        'project': 'project',
        'no_tasks': 'no tasks',
        'status': 'status',
        'due': 'due',
        'urgency': 'urgency',
        'priority': 'priority',
        'enter_new_task_description': 'enter new task description',
        'choose_tag': 'choose tag',
        'choose_project': 'choose project',
        'tasks_for_tag': 'tasks for tag',
        'tasks_in_project': 'tasks in project',
        'task_completed': 'task completed',
        'error_while_completing_task': 'error while completing task',
        'completion_canceled': 'completion canceled',
        'task_deleted': 'task deleted',
        'error_while_deleting_task': 'error while deleting task',
        'deletion_canceled': 'deletion canceled',
        'error_while_canceling_previous_action': 'error while canceling previous action',
        'no_tasks_today': 'no tasks today',
        'add_tags': 'add tags',
        'add_to_project': 'add to project',
        'change_priority': 'change priority',
        'change_due_date': 'change due date',
        'finish': 'finish',
        'complete': 'complete',
        'error_while_changing_tag': 'error while changing tag',
        'error_while_changing_priority': 'error while changing priority',
        'high': 'high',
        'medium': 'medium',
        'low': 'low',
        'no_overdue_tasks': 'no overdue tasks',
    },
}
emoticons = {
    0: {
        'delete': '❌',
        'modify': '✏',
        'done': '✔',
        'info': '📋',
        'undo': '↩',
    },
    1: {
        'done': '✓',
        'modify': '✎',
        'delete': '✗',
        'info': 'i',
        'undo': '↶',
    }

}


class Kwords:
    def __init__(self, lang, emoticons_enabled):
        for k, v in translations[lang].items():
            setattr(self, k, v)
            setattr(self, k.capitalize(), v.capitalize())
        if emoticons_enabled:
            for k, v in emoticons[1].items():
                setattr(self, k, v)
                setattr(self, k.capitalize(), v.capitalize())


k = Kwords(LANG, EMOTICONS_ENABLED)

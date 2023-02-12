from tg.utils import TgClient


async def clear_lists(tg_client: TgClient, user, list_id=None, except_first=False):
    if not list_id:
        for l_id in tg_client.msg_stack[user].keys():
            await _clear_list(tg_client, user, l_id, except_first)
    else:
        await _clear_list(tg_client, user, list_id, except_first)


async def _clear_list(tg_client: TgClient, user, list_id, except_first=False):
    stack = tg_client.msg_stack[user][list_id]
    if len(stack):
        for d in stack:
            if except_first:
                messages_list = stack[d][1:]
            else:
                messages_list = stack[d]
            await tg_client.delete_messages(tg_client.chats_dict[user], messages_list)


from config import REDIRECT_URI
from database_queries import get_all_id_tg, get_user_info, set_end_time, set_group_ids, set_status, set_user_ids
from requests_to_VK_API import get_account_info, get_info_about_groups, get_info_about_source, get_token, get_user_friends, get_user_groups
import datetime
import re


def add_group(id_tg, group_id, user_info):
    id_vk = user_info['id_vk']
    vk_token = user_info['vk_token']
    current_group_ids = user_info['group_ids']

    if current_group_ids and str(group_id) in current_group_ids.split(','):
        return 'repeat group'

    group_info = get_info_about_groups(group_id, vk_token)['response'][0]

    if group_info['is_closed'] and group_id not in get_user_groups(id_vk, vk_token)['response']['items']:
        return 'closed group'

    new_group_ids = f'{current_group_ids},{group_id}' if current_group_ids else str(group_id)
    set_group_ids(id_tg, new_group_ids)

    return 'group'


def add_source(id_tg, link_to_source):
    if not re.match('https://vk.com/', link_to_source) or len(link_to_source) < 20 or len(link_to_source) > 47:
        return None

    screen_name = link_to_source[15:]
    user_info = get_user_info(id_tg)
    data = get_info_about_source(screen_name, user_info['vk_token'])['response']

    try:
        info_about_source = {
            'type': data['type'],
            'id': data['object_id']
        }
    except TypeError:
        return None

    if not user_info['group_ids'] and not user_info['user_ids']:
        set_end_time(id_tg, get_current_unix_time())

    if info_about_source['type'] == 'group':
        return add_group(id_tg, info_about_source['id'], user_info)
    elif info_about_source['type'] == 'user':
        return add_user(id_tg, info_about_source['id'], user_info)
    else:
        return 'invalid source'


def add_user(id_tg, user_id, user_info):
    vk_token = user_info['vk_token']
    current_user_ids = user_info['user_ids']

    if current_user_ids and str(user_id) in current_user_ids.split(','):
        return 'repeat user'

    account_info = get_account_info(user_id, vk_token)['response'][0]

    if account_info['is_closed'] and user_id not in get_user_friends(vk_token)['response']['items']:
        return 'closed user'

    new_user_ids = f'{current_user_ids},{user_id}' if current_user_ids else str(user_id)
    set_user_ids(id_tg, new_user_ids)

    return 'user'


def delete_group(id_tg, group_numbers):
    if not len(group_numbers):
        return

    user_info = get_user_info(id_tg)
    current_group_ids = user_info['group_ids'].split(',')
    for group_number in sorted(group_numbers, reverse=True):
        current_group_ids.pop(group_number)

    new_group_ids = None if not len(current_group_ids) else ','.join(current_group_ids)
    set_group_ids(id_tg, new_group_ids)


def delete_source(id_tg, source_numbers):
    source_numbers = source_numbers.replace(' ', '').split(',')
    group_numbers, user_numbers = list(), list()
    user_info = get_user_info(id_tg)

    for source_number in source_numbers:
        if source_number[0] == '1':
            group_numbers.append(source_number[1:])
        elif source_number[0] == '2':
            user_numbers.append(source_number[1:])
        else:
            return 'incorrect list'

    try:
        group_numbers = sorted(map(int, group_numbers), reverse=True)
        user_numbers = sorted(map(int, user_numbers), reverse=True)
    except ValueError:
        return 'incorrect list'

    if len(group_numbers) and group_numbers[0] >= len(user_info['group_ids'].split(',')):
        return 'incorrect list'

    if len(user_numbers) and user_numbers[0] >= len(user_info['user_ids'].split(',')):
        return 'incorrect list'

    delete_group(id_tg, group_numbers)
    delete_user(id_tg, user_numbers)

    return 'delete'


def delete_user(id_tg, user_numbers):
    if not len(user_numbers):
        return

    user_info = get_user_info(id_tg)
    current_user_ids = user_info['user_ids'].split(',')
    for user_number in sorted(user_numbers, reverse=True):
        current_user_ids.pop(user_number)

    new_user_ids = None if not len(current_user_ids) else ','.join(current_user_ids)
    set_user_ids(id_tg, new_user_ids)


def get_current_unix_time():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))


def get_group_list(id_tg):
    user_info = get_user_info(id_tg)

    if not user_info['group_ids']:
        return None

    data = get_info_about_groups(user_info['group_ids'], user_info['vk_token'])['response']
    group_list = [group['name'] for group in data]

    return group_list


def get_id_and_token_vk(text_with_link_with_code):
    link_with_code = re.search(REDIRECT_URI + r'#code=[a-z\d]{18}', text_with_link_with_code)

    if not link_with_code:
        return 'invalid link'

    code = re.search(r'[a-z\d]{18}', link_with_code.group()).group()
    data = get_token(code)

    try:
        id_and_token = {
            'id': data['user_id'],
            'token': data['access_token']
        }
    except KeyError:
        return 'invalid code'

    return id_and_token


def get_info_about_current_account(id_tg):
    user_info = get_user_info(id_tg)
    id_vk = user_info['id_vk']
    vk_token = user_info['vk_token']
    data = get_account_info(id_vk, vk_token)['response'][0]

    try:
        info_about_current_account = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'screen_name': data['screen_name'],
            'url_of_photo': data['photo_max']
        }
    except KeyError:
        return None

    return info_about_current_account


def get_list_of_sources(id_tg):
    list_of_sources = {
        'group_list': get_group_list(id_tg),
        'user_list': get_user_list(id_tg)
    }

    return list_of_sources


def get_user_list(id_tg):
    user_info = get_user_info(id_tg)

    if not user_info['user_ids']:
        return None

    data = get_account_info(user_info['user_ids'], user_info['vk_token'])['response']
    user_list = [f"{user['first_name']} {user['last_name']}" for user in data]

    return user_list


def is_user_added(id_tg):
    return str(id_tg) in get_all_id_tg()


def is_vk_account_connected(id_tg):
    user_info = get_user_info(id_tg)
    return user_info['id_vk'] and user_info['vk_token']


def set_status_to_ON(id_tg):
    set_status(id_tg, 'ON')


def set_status_to_OFF(id_tg):
    set_status(id_tg, 'OFF')

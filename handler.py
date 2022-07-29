from config import REDIRECT_URI
from database_queries import get_all_id_tg, get_user_info, set_end_time, set_group_ids, set_status, set_user_ids
from requests_to_VK_API import get_account_info, get_info_about_source, get_token
import re


def add_source(id_tg, link_to_source):
    if not re.match('https://vk.com/', link_to_source) or len(link_to_source) < 20 or len(link_to_source) > 47:
        return None

    screen_name = link_to_source[15:]
    user_info = get_user_info(id_tg)
    vk_token = user_info['vk_token']
    data = get_info_about_source(screen_name, vk_token)['response']

    try:
        info_about_source = {
            'type': data['type'],
            'id': data['object_id']
        }
    except TypeError:
        return None

    if info_about_source['type'] not in ['group', 'user']:
        return None

    current_source_ids = user_info[f'{info_about_source["type"]}_ids']
    new_source_ids = current_source_ids + f',{info_about_source["id"]}' if current_source_ids is not None else info_about_source["id"]

    if info_about_source['type'] == 'group':
        set_group_ids(id_tg, new_source_ids)
    else:
        set_user_ids(id_tg, new_source_ids)

    return True


def get_id_and_token_vk(text_with_link_with_code):
    link_with_code = re.search(REDIRECT_URI + r'#code=[a-z\d]{18}', text_with_link_with_code)

    if not link_with_code:
        return None

    code = re.search(r'[a-z\d]{18}', link_with_code.group()).group()
    data = get_token(code)

    try:
        id_and_token = {
            'id': data['user_id'],
            'token': data['access_token']
        }
    except KeyError:
        return None

    return id_and_token


def get_info_about_current_account(id_tg):
    user_info = get_user_info(id_tg)
    vk_token = user_info['vk_token']
    data = get_account_info(vk_token)['response'][0]

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


def is_user_added(id_tg):
    return str(id_tg) in get_all_id_tg()


def is_vk_account_connected(id_tg):
    user_info = get_user_info(id_tg)
    return user_info['id_vk'] is not None and user_info['vk_token'] is not None


def set_status_to_ON(id_tg):
    set_status(id_tg, 'ON')


def set_status_to_OFF(id_tg):
    set_status(id_tg, 'OFF')

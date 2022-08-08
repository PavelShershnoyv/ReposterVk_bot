from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, VK_API_VERSION
import requests


def get_account_info(user_ids, vk_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_ids,
        'fields': 'photo_max,screen_name',
        'access_token': vk_token,
        'v': VK_API_VERSION
    }
    response = requests.get(url, params)

    return response.json()


def get_info_about_groups(group_ids, vk_token):
    url = 'https://api.vk.com/method/groups.getById'
    params = {
        'group_ids': group_ids,
        'access_token': vk_token,
        'v': VK_API_VERSION
    }
    response = requests.get(url, params)

    return response.json()


def get_info_about_source(screen_name, vk_token):
    url = 'https://api.vk.com/method/utils.resolveScreenName'
    params = {
        'screen_name': screen_name,
        'access_token': vk_token,
        'v': VK_API_VERSION
    }
    response = requests.get(url, params)

    return response.json()


def get_newsfeed(vk_token, start_time, source_ids):
    url = 'https://api.vk.com/method/newsfeed.get'
    params = {
        'filters': 'post',
        'return_banned': '1',
        'start_time': start_time,
        'max_photos': '10',
        'source_ids': source_ids,
        'count': '100',
        'fields': 'first_name,last_name,name',
        'access_token': vk_token,
        'v': VK_API_VERSION
    }
    response = requests.get(url, params)

    return response.json()


def get_token(code):
    url = 'https://oauth.vk.com/access_token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    response = requests.get(url, params)

    return response.json()


def get_user_friends(vk_token):
    url = 'https://api.vk.com/method/friends.get'
    params = {
        'access_token': vk_token,
        'v': VK_API_VERSION
    }
    response = requests.get(url, params)

    return response.json()


def get_user_groups(id_vk, vk_token):
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'user_id': id_vk,
        'access_token': vk_token,
        'v': VK_API_VERSION
    }
    response = requests.get(url, params)

    return response.json()


def get_video(vk_token, owner_id, videos, count):
    url = 'https://api.vk.com/method/video.get'
    params = {
        'owner_id': owner_id,
        'videos': videos,
        'count': count,
        'access_token': vk_token,
        'v': VK_API_VERSION
    }
    response = requests.get(url, params)

    return response.json()

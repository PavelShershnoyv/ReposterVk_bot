from config import REDIRECT_URI, VK_API_VERSION
import requests


def get_account_info(vk_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'fields': 'photo_max,screen_name',
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


def get_token(code):
    url = 'https://oauth.vk.com/access_token'
    params = {
        'client_id': '8221094',
        'client_secret': 'XmFdkB0LiBFyIZ1u4AaG',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    response = requests.get(url, params)

    return response.json()

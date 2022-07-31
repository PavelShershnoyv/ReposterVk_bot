# import multiprocessing
from database_queries import get_all_id_tg, get_user_info, set_end_time
from requests_to_VK_API import get_video, get_newsfeed
import time
import asyncio
from handler import get_current_unix_time


def get_info_from_posts(info, vk_token):
    id_name = {}
    groups = info['response']['groups']
    profiles = info['response']['profiles']
    if groups:
        for group in groups:
            id_name[group['id']] = group['name']
    if profiles:
        for profile in profiles:
            id_name[profile['id']] = f"{profile['first_name']} {profile['last_name']}"
    posts = info['response']['items']
    for post in posts:
        by = id_name[abs(post['owner_id'])]
        text = post['text']
        keys = post.keys()
        url_photo, url_video = [], []
        url_doc, url_link = {}, {}
        if 'attachments' in keys:
            for i in range(len(post['attachments'])):
                type_attachments = post['attachments'][i]['type']
                if type_attachments == 'photo':
                    for size in post['attachments'][i]['photo']['sizes']:
                        if size['type'] == 'r':
                            url_photo.append(size['url'])
                if type_attachments == 'doc':
                    url_doc[post['attachments'][i]['doc']['title']] = post['attachments'][i]['doc']['url']
                if type_attachments == 'link':
                    url_link[post['attachments'][i]['link']['title']] = post['attachments'][i]['link']['url']
                if type_attachments == 'video':
                    owner_id = post['attachments'][i]['video']['owner_id']
                    part_id = post['attachments'][i]['video']['id']
                    access_key = post['attachments'][i]['video']['access_key']
                    video = get_video(vk_token, owner_id, f'{owner_id}_{part_id}_{access_key}', 1)
                    url_video = [video['player'] for video in video['response']['items']]

        result = {
            'by': by,
            'text': text,
            'photo': url_photo,
            'link': url_link,
            'doc': url_doc,
            'video': url_video
        }
        print(result)
        # send_post(result)


async def get_post():
    while True:
        ids_tg = get_all_id_tg()
        for id in ids_tg:
            user = get_user_info(id)
            if user['status'] == 'OFF':
                continue
            posts = get_newsfeed(user['vk_token'], user['end_time'],
                                 ','.join([f'g{group_id}' for group_id in user['group_ids'].split(',')]), user['user_ids'])
            set_end_time(id, get_current_unix_time())
            get_info_from_posts(posts, user['vk_token'])
            await asyncio.sleep(1)


# if __name__ == '__main__':
#     p1 = multiprocessing.Process(target=get_posts)
#     p1.start()


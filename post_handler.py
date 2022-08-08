from aiogram import types
from create_bot import bot
from database_queries import get_all_id_tg, get_user_info, set_end_time
from requests_to_VK_API import get_newsfeed, get_video
import asyncio
import math


async def get_posts():
    while True:
        for id_tg in get_all_id_tg():
            user = get_user_info(id_tg)
            group_ids = user['group_ids']
            user_ids = user['user_ids']

            if user['status'] == 'OFF' or group_ids is None and user_ids is None:
                continue

            group_ids = list(map(lambda group_id: f'g{group_id}', group_ids.split(','))) if group_ids is not None else list()
            user_ids = user_ids.split(',') if user_ids is not None else list()
            source_ids = ','.join(group_ids + user_ids)
            posts = get_newsfeed(user['vk_token'], user['end_time'], source_ids)

            if posts['response']['items']:
                end_time = posts['response']['items'][0]['date'] + 1
                set_end_time(id_tg, end_time)

            await handle_posts(posts, user['vk_token'], id_tg)

        await asyncio.sleep(5)


async def handle_posts(posts, vk_token, id_tg):
    source_name = dict()
    groups = posts['response']['groups']
    profiles = posts['response']['profiles']

    for group in groups:
        source_name[-group['id']] = group['name']

    for profile in profiles:
        source_name[profile['id']] = f"{profile['first_name']} {profile['last_name']}"

    for post in posts['response']['items']:
        by = source_name[post['source_id']]
        text = post['text']
        url_doc, url_link, url_photo, url_video = dict(), dict(), list(), list()

        if 'attachments' in post.keys():
            for attachment in post['attachments']:
                attachment_type = attachment['type']

                if attachment_type == 'photo':
                    for size in attachment['photo']['sizes']:
                        if size['type'] == 'r':
                            url_photo.append(size['url'])

                if attachment_type == 'doc':
                    url_doc[attachment['doc']['title']] = attachment['doc']['url']

                if attachment_type == 'link':
                    url_link[attachment['link']['title']] = attachment['link']['url']

                if attachment_type == 'video':
                    owner_id = attachment['video']['owner_id']
                    video_id = attachment['video']['id']
                    access_key = attachment['video']['access_key']
                    video = get_video(vk_token, owner_id, f'{owner_id}_{video_id}_{access_key}', 1)
                    url_video += [video['player'] for video in video['response']['items']]

        result = {
            'by': by,
            'doc': url_doc,
            'link': url_link,
            'photo': url_photo,
            'text': text,
            'video': url_video
        }

        await send_post(id_tg, result)


async def send_post(id_tg, post):
    caption = f"<b>[VK] От: {post['by']}</b>"

    if post['text']:
        caption += f"\n\n{post['text']}"

    if post['video']:
        videos = 'Видео:'

        for i, url in enumerate(post['video']):
            videos += f'\n{i + 1}) {url}'

        caption += f'\n\n{videos}'

    if post['doc']:
        docs = 'Документы:'

        for key, value in post['doc'].items():
            docs += f'\n"{key}": {value}'

        caption += f'\n\n{docs}'

    if post['link']:
        links = 'Ссылки:'

        for i, url in enumerate(post['link'].values()):
            links += f'\n{i + 1}) {url}'

        caption += f'\n\n{links}'

    if post['photo']:
        media = types.MediaGroup()
        media.attach_photo(caption=caption[:1000], parse_mode='html', photo=post['photo'][0])

        for photo in post['photo'][1:]:
            media.attach_photo(photo=photo)

        await bot.send_media_group(chat_id=id_tg, media=media)
    else:
        await bot.send_message(chat_id=id_tg, parse_mode='html', text=caption[:4000])

    sent = 1000 if post['photo'] else 4000
    for i in range(math.ceil((len(caption) - sent) / 4000)):
        await bot.send_message(chat_id=id_tg, parse_mode='html', text=caption[sent + 4000 * i: sent + 4000 * (i + 1)])

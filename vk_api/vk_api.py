import time

import requests

with open('token.txt', 'r') as token_file:
    AUTH_TOKEN = token_file.read().strip()

GROUP = 'honkaistarrail_official'
USER_ID = 497723165
VERSION = 5.131


def get_posts(amount):
    offset = 0
    vk_resp = requests.get('https://api.vk.com/method/wall.get',
                           params={
                               'access_token': AUTH_TOKEN,
                               'v': VERSION,
                               'domain': GROUP,
                               'count': amount,
                               'offset': offset
                           })
    info = vk_resp.json()['response']['items']
    return info


def write_posts_to_file(posts):
    with open('posts.txt', 'w', encoding="utf-8") as file:
        for post in posts:
            text = post['text']
            file.write('date: ' +
                       str(time.ctime(post['date'])) + ' comments: ' + str(
                post['comments']['count']) + '\ntext:\n' + text + '\n\n')


def get_friends():
    count = 100
    order = 'name'
    response = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'access_token': AUTH_TOKEN,
                                'count': count,
                                'user_id': USER_ID,
                                'order': order,
                                'v': VERSION,
                                'fields': 'bdate'
                            })
    friends = response.json()['response']['items']
    return friends


def write_friends_to_file(friends):
    with open('friends.txt', 'w', encoding='utf-8') as file:
        for friend in friends:
            try:
                birth = friend['bdate']
            except:
                birth = 'idk'
            file.write(
                'birthday: ' + birth + '\nname: ' + friend['first_name'] + ' surname: ' + friend[
                    'last_name'] + '\n\n')


if __name__ == '__main__':
    posts = get_posts(10)
    write_posts_to_file(posts)
    friends = get_friends()
    write_friends_to_file(friends)

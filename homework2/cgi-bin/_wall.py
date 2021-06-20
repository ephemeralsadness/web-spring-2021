#!/usr/bin/env python3

import json
import random
import time

from typing import Dict, List


class Wall:
    USERS = 'cgi-bin/users.json'
    WALL = 'cgi-bin/wall.json'
    COOKIES = 'cgi-bin/cookies.json'

    def __init__(self):
        """Создаём начальные файлы, если они не созданы"""
        try:
            with open(self.USERS, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.USERS, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        try:
            with open(self.WALL, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.WALL, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        try:
            with open(self.COOKIES, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.COOKIES, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def register(self, user, password):
        """Регистриует пользователя. Возвращает True при успешной регистрации"""
        if self.find(user):
            return False  # Такой пользователь существует
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        users[user] = [password, "gold"]
        with open(self.USERS, 'w', encoding='utf-8') as f:
            json.dump(users, f)
        return True

    def set_cookie(self, user):
        """Записывает куку в файл. Возвращает созданную куку."""
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        cookie = str(time.time()) + str(random.randrange(10**14))  # Генерируем уникальную куку для пользователя
        cookies[cookie] = user
        with open(self.COOKIES, 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
        return cookie

    def find_cookie(self, cookie):
        """По куке находит имя пользователя"""
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        return cookies.get(cookie)

    def remove_cookie(self, cookie):
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        if cookie in cookies:
            cookies.pop(cookie)
        with open(self.COOKIES, 'w', encoding='utf-8') as f:
            json.dump(cookies, f)

    def find(self, user, password=None):
        """Ищет пользователя по имени или по имени и паролю"""
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        if user in users and (password is None or password == users[user][0]):
            return True
        return False

    def ava(self, user):
        """Ищет цвет аватарок пользователей"""
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        for u, p in users.items():
            if user == u:
                return p[1]
        return "gray"

    def change_ava(self, user, color):
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)

        users[user][1] = color

        with open(self.USERS, 'w', encoding='utf-8') as f:
            json.dump(users, f)

    def publish(self, user, text):
        if len(text) != 0 and text[0] == '/':
            self.change_ava(user, text[1:])
            return
        """Публикует текст"""
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        wall.append({'user': user, 'text': text})
        with open(self.WALL, 'w', encoding='utf-8') as f:
            json.dump(wall, f)

    def html_list(self):
        """Список постов для отображения на странице"""
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        posts = []
        for post in wall:
            content = f"""
                    <div class="post">
                        <div class="post-ava" style="background-color: {self.ava(post['user'])}"></div>
                        <div class="post-username">{post['user']}</div>
                        <div class="post-text">{post['text']}</div>
                    </div>
            """
            posts.append(content)
        return '\n'.join(posts[::-1])

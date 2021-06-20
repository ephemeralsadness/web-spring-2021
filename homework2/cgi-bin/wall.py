#!/usr/bin/env python3

import cgi
import html
import http.cookies
import os
import sys
from _wall import Wall

wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")

if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке

form = cgi.FieldStorage()
action = form.getfirst("action", "")


if action == "Войти":
    login = html.escape(form.getfirst("login", ""))
    password = html.escape(form.getfirst("password", ""))
    if wall.find(login, password):
        cookie = wall.set_cookie(login)
        user = cookie
        print('Set-cookie: session={}'.format(cookie))
elif action == "Зарегистрироваться":
    login = html.escape(form.getfirst("login", ""))
    password = html.escape(form.getfirst("password", ""))
    if not wall.find(login):
        wall.register(login, password)
        cookie = wall.set_cookie(login)
        user = cookie
        print('Set-cookie: session={}'.format(cookie))
elif action == "Выйти":
    wall.remove_cookie(cookie.get("session").value)
    cookie.clear()
    user = None
elif action == "Отправить":
    text = form.getfirst("text", "")
    text = html.escape(text)
    if text is not None and user is not None:
        wall.publish(user, text)


# pattern == common html file
# pub == mainpage
# reg == login

print('Content-type: text/html\n')

if user is None:
    # Не в системе
    with open("cgi-bin/src/login.html", "r") as html_file, open("cgi-bin/src/login.css", "r") as css_file:
        html_code = '\n'.join(html_file.readlines())
        css_code = '\n'.join(css_file.readlines())
        html_code = html_code.replace("<!-- STYLE -->", css_code)
        print(html_code)
else:
    # В системе
    with open("cgi-bin/src/mainpage.html", "r") as html_file, open("cgi-bin/src/mainpage.css", "r") as css_file:
        html_code = '\n'.join(html_file.readlines())
        css_code = '\n'.join(css_file.readlines())
        html_code = html_code.replace("<!-- STYLE -->", css_code)

        ava = wall.ava(wall.find_cookie(user))
        html_code = html_code.replace("<!-- AVA -->", ava)

        posts = wall.html_list()
        html_code = html_code.replace("<!-- POSTS -->", posts)
        print(html_code)

from flask import request

def clear_cookies(response):

    from app import app

    session_cookie_name = app.config.get('SESSION_COOKIE_NAME', 'session')

    cookies = request.cookies

    for cookie in cookies:

        if cookie != session_cookie_name:

            response.delete_cookie(cookie)

    return response

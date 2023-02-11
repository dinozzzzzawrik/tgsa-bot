import os
import json

from aiohttp import web
from aiohttp_jinja2 import setup, template
from aiohttp_session import setup, get_session

from models.models import WhiteList, Accounts


@template('login.html')
async def login(request):
    if request.method == 'POST':
        data = await request.post()
        username = data.get('username')
        password = data.get('password')

        if username == os.getenv('LOGIN') and password == os.getenv('PASSWORD'):
            session = await get_session(request)
            session['user'] = username
            raise web.HTTPFound('/admin')
        else:
            raise web.HTTPUnauthorized()


@template('admin.html')
async def admin(request):
    session = await get_session(request)
    user = session.get('user')

    whitelist = WhiteList.select()
    accounts = Accounts.select()

    if user is None:
        raise web.HTTPFound('/')
    return {'whitelist': whitelist, 'accounts': accounts}


async def logout(request):
    session = await get_session(request)
    session.clear()
    raise web.HTTPFound('/')


async def add_user(request):
    # retrieve data from the form using request.post()
    session = await get_session(request)
    auser = session.get('user')
    if auser is None:
        raise web.HTTPFound('/')

    try:
        data = await request.post()
        name = data.get('name')
        tg_id = int(data.get('tg_id'))
    except (Exception,):
        return web.Response(text='Please fill out all fields.', status=400)

    # add the data to the database using your preferred database library
    # for example, using SQLAlchemy:
    user = WhiteList(name=name, tg_id=tg_id)
    user.save()

    # redirect the user back to the admin page
    raise web.HTTPFound('/admin')


async def delete_user(request):
    # Get the user ID from the request URL
    session = await get_session(request)
    auser = session.get('user')
    if auser is None:
        raise web.HTTPFound('/')

    user_id = request.query.get('id')

    user = WhiteList.get(WhiteList.id == user_id)
    user.delete_instance()

    # Return a JSON response indicating success or failure
    raise web.HTTPFound('/admin')


async def add_acc(request):
    # retrieve data from the form using request.post()
    session = await get_session(request)
    auser = session.get('user')
    if auser is None:
        raise web.HTTPFound('/')

    try:
        data = await request.post()
        name = data.get('acc_name')
        key = data.get('key')
    except (Exception,):
        return web.Response(text='Please fill out all fields.', status=400)

    # add the data to the database using your preferred database library
    # for example, using SQLAlchemy:
    acc = Accounts(name=name, key=key)
    acc.save()

    # redirect the user back to the admin page
    raise web.HTTPFound('/admin')


async def delete_acc(request):
    # Get the user ID from the request URL
    session = await get_session(request)
    auser = session.get('user')
    if auser is None:
        raise web.HTTPFound('/')

    acc_id = request.query.get('id')

    acc = Accounts.get(Accounts.id == acc_id)
    acc.delete_instance()

    # Return a JSON response indicating success or failure
    raise web.HTTPFound('/admin')


@template('help.html')
async def help(request):
    if request.method == 'POST':
        data = await request.post()
        file = data['file'].file
        filename = data['file'].filename

        with open(filename, 'wb') as f:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                key = data['shared_secret']
                login = data['account_name']
        except (Exception,):
            return web.Response(text='Please check your file', status=400)

        os.remove(filename)

        return {'login': login, 'key': key}

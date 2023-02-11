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

        if username == 'admin' and password == 'admin':
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
    accounts = Accounts.select().get()

    if user is None:
        raise web.HTTPFound('/')
    return {'whitelist': whitelist}


async def logout(request):
    session = await get_session(request)
    session.clear()
    raise web.HTTPFound('/')


async def add(request):
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


async def delete(request):
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

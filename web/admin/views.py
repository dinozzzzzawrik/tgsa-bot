from aiohttp import web
from aiohttp_jinja2 import setup, template
from aiohttp_session import setup, get_session


@template('login.html')
async def login(request):
    if request.method == 'POST':
        data = await request.post()
        username = data.get('username')
        password = data.get('password')

        if username == 'admin' and password == 'admin':
            session = await get_session(request)
            session['user'] = username
            return web.HTTPFound('/admin')
        else:
            return web.HTTPUnauthorized()


@template('admin.html')
async def admin(request):
    session = await get_session(request)
    user = session.get('user')
    if user is None:
        return web.HTTPFound('/')


async def logout(request):
    session = await get_session(request)
    session.clear()
    raise web.HTTPFound('/')


async def add_user(request):
    # retrieve data from the form using request.post()
    username = request.post['username']
    email = request.post['email']

    # validate the data and return an error response if needed
    if not username or not email:
        return web.Response(text='Please fill out all fields.', status=400)

    # add the data to the database using your preferred database library
    # for example, using SQLAlchemy:
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    # redirect the user back to the admin page
    raise web.HTTPFound('/admin')

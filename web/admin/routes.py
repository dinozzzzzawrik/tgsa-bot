from web.admin import views
from aiohttp import web


def setup_routes(app: web.Application) -> None:
    app.router.add_get('', views.login)
    app.router.add_post('', views.login)

    app.router.add_get('/admin', views.admin)

    app.router.add_get('/logout', views.logout)

    app.router.add_post('/add_user', views.add_user)

from web.admin import views
from aiohttp import web


def setup_routes(app: web.Application) -> None:
    app.router.add_get('', views.login)
    app.router.add_post('', views.login)

    app.router.add_get('/admin', views.admin)

    app.router.add_get('/logout', views.logout)

    app.router.add_post('/add_user', views.add_user)
    app.router.add_get('/delete_user', views.delete_user)

    app.router.add_post('/add_acc', views.add_acc)
    app.router.add_get('/delete_acc', views.delete_acc)

    app.router.add_get('/help', views.help)
    app.router.add_post('/help', views.help)

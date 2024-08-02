from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("portfolio/add", views.add_stock, name="add_stock"),
    path("portfolio/remove", views.remove_stock, name="remove_stock"),
    path("stocks", views.stocks, name="stocks"),
    path("stocks/new", views.new_stock, name="new_stock"),
    path("stocks/edit", views.edit_stock, name="edit_stock"),
    path("stocks/delete", views.delete_stock, name="delete_stock"),
    path("events", views.events, name="events"),
    path("events/new", views.new_event, name="new_event"),
    path("events/edit", views.edit_event, name="edit_event"),
    path("events/delete", views.delete_event, name="delete_event"),
    path("simulator", views.simulator, name="simulator"),
    path("simulation", views.simulation, name="simulation"),
]

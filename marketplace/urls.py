from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("category/<int:category_id>", views.category_listings, name="category_listings"),
    path("listing/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("edit_listing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("profile", views.profile, name="profile"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("my_purchases", views.my_purchases, name="my_purchases"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
]

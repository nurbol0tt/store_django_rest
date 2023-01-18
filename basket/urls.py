from django.urls import path

from . import views


# Check
urlpatterns = [
    path("add_to_cart/<int:pro_id>/", views.AddToCartView.as_view()),
    path("update_cart/<int:pro_id>/", views.UpdateCartItemView.as_view()),
    path("cart/", views.CartListView.as_view()),
    path("cart_change/<int:pro_id>/", views.ManageCartView.as_view()),
]


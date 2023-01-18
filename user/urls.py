from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('update_password/', views.UpdatePassword.as_view()),
    path('user_list/', views.UserListView.as_view()),
    path('user/<int:pk>/detail/', views.UserDetailView.as_view()),
    path('rating_user/', views.AddStarRatingUserView.as_view()),
    path('email_verify/', views.EmailVerify.as_view(), name='email_verify'),
    path('wishlist/add_to_wishlist/<int:pk>/', views.WishlistCreateView.as_view()),
    path('my_wishlist/', views.MyWishlistView.as_view())
]


from django.urls import path

from . import views

urlpatterns = [
    path("checkout/<int:pk>/", views.CheckoutView.as_view()),
    path("webhook/", views.MyWebhookView.as_view()),
    path("success/", views.SuccessView.as_view()),
]


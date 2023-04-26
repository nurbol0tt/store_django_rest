from django.urls import path

from product.views import views
from product.views import views_product
from product.views import views_category
from product.views import views_comment


urlpatterns = [
    # Product
    path('products/', views_product.ProductListView.as_view(), name='products'),
    path('product/create/', views_product.ProductCreateView.as_view()),
    path('product/<int:pk>/detail/', views_product.ProductDetailView.as_view()),
    path('product/<int:pk>/update/', views_product.ProductUpdateView.as_view()),
    path('product/<int:pk>/delete/', views_product.ProductDeleteView.as_view()),

    # Category
    path('categories/', views_category.CategoryListView.as_view()),
    path('category/create/', views_category.CategoryCreateView.as_view()),
    path('category/<int:pk>/detail/', views_category.CategoryDetailView.as_view()),
    path('category/<int:pk>/update/', views_category.CategoryUpdateView.as_view()),
    path('category/<int:pk>/delete/', views_category.CategoryDeleteView.as_view()),

    # Comment
    path('comment/', views_comment.CommentCreateView.as_view()),
    path('comment/<int:pk>/delete/', views_comment.CommentDeleteView.as_view()),
    path('comment/<int:pk>/update/', views_comment.CommentUpdateView.as_view()),


    # Single
    path('rating_product/', views.AddStarRatingView.as_view()),
    path('most_popular/', views.ProductMostPopular.as_view()),
    path('most_viewed/', views.ProductMostViewed.as_view()),
    path('most_liked/', views.MostLikeView.as_view()),
    path('like/<int:pk>/', views.LikeView.as_view()),
    path('search/', views.SearchView.as_view()),
    path('filter/', views.FilterDataView.as_view()),
]

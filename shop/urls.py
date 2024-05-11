from django.urls import path
from .views import *


urlpatterns=[
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<slug:category_slug>/", ProductListView.as_view(), name="product_list_by_category"),
    path('product/<int:pk>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]


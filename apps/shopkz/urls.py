from django.urls import path

from .views import CategoryView, ProductView

urlpatterns = (
    path('category/<int:category_id>', CategoryView.as_view()),
    path('product/<int:product_id>', ProductView.as_view()),
)

from django.urls import path

from .views import ProductImportView

urlpatterns = (
    path('product/import/', ProductImportView.as_view()),
)

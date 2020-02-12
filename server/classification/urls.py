from django.urls import path
from . import views

urlpatterns = [
    path('classify/', views.ClassificationView.as_view(), name= 'classification_result'),
]

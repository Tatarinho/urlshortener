from django.urls import path
from apps.shortener.views import EncodeURLView, DecodeURLView

urlpatterns = [
    path('encode/', EncodeURLView.as_view(), name='encode'),
    path('decode/<str:short_code>/', DecodeURLView.as_view(), name='decode'),
]

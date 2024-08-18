from apps.shortener.views import EncodeURLView, DecodeURLView, RedirectView, IndexView, ProcessURLView
from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('process/', ProcessURLView.as_view(), name='process'),
    path('encode/', EncodeURLView.as_view(), name='encode'),
    path('decode/<str:short_code>/', DecodeURLView.as_view(), name='decode'),
    path('<str:short_code>/', RedirectView.as_view(), name='redirect'),
]

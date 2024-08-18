from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ShortURL
from .utils import encode_url, decode_url, build_full_url, is_internal_link


class URLMixin:
    def encode_and_build_url(self, request: HttpRequest, url: str):
        short_url, created = encode_url(url)
        full_url = build_full_url(request, short_url.short_code)
        return full_url, created


class EncodeURLView(APIView, URLMixin):
    def post(self, request, *args, **kwargs):
        url = request.data.get('url', '')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        validator = URLValidator()
        try:
            validator(url)
        except ValidationError:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

        full_url, created = self.encode_and_build_url(request, url)
        return Response({'url': full_url}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class DecodeURLView(APIView):
    def get(self, request, short_code, *args, **kwargs):
        try:
            short_url = decode_url(short_code)
            return Response({'url': short_url.url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RedirectView(APIView):
    def get(self, request, short_code, *args, **kwargs):
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        return redirect(short_url.url)


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class ProcessURLView(APIView, URLMixin):
    def get(self, request, *args, **kwargs):
        input_value = request.query_params.get('url')
        if not input_value:
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        if is_internal_link(request, input_value):
            short_code = input_value.rstrip('/').split('/')[-1]  # Extract short code from the URL
            try:
                url = decode_url(short_code)
                return Response({'url': url.url}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            full_url, _ = self.encode_and_build_url(request, input_value)
            return Response({'url': full_url}, status=status.HTTP_201_CREATED)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.shortener.models import ShortURL
from django.shortcuts import get_object_or_404


class EncodeURLView(APIView):
    def post(self, request, *args, **kwargs):
        url = request.data.get('url', '')
        if url:
            short_url, created = ShortURL.objects.get_or_create(url=url)
            short_code = short_url.short_code

            full_url = request.build_absolute_uri(f'/{short_code}')
            return Response({'url': full_url}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)


class DecodeURLView(APIView):
    def get(self, request, short_code, *args, **kwargs):
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        return Response({'url': short_url.url}, status=status.HTTP_200_OK)

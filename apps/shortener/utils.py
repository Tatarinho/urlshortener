from urllib.parse import urlparse

from django.shortcuts import get_object_or_404
from .models import ShortURL


def encode_url(url):
    """
    Encode the given URL by creating or retrieving the corresponding short URL.

    Args:
        url (str): The URL to encode.

    Returns:
        tuple: A tuple containing the short URL object and a boolean indicating
               whether the object was created or retrieved from the database.
    """
    short_url, created = ShortURL.objects.get_or_create(url=url)
    return short_url, created


def decode_url(short_code):
    """
    Decode the given short code by retrieving the corresponding full URL.

    Args:
        short_code (str): The short code to decode.

    Returns:
        ShortURL: The ShortURL object associated with the given short code.
    """
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    return short_url


def build_full_url(request, short_code):
    """
    Build the full URL given a request and a short code.

    Args:
        request: The HTTP request object.
        short_code (str): The short code for which to build the full URL.

    Returns:
        str: The full URL.
    """
    full_url = request.build_absolute_uri(f'/{short_code}')
    return full_url


def is_internal_link(request, url):
    """
    Checks if the given URL is an internal link (within the application).

    Args:
        request: HTTP request object.
        url (str): URL to check.

    Returns:
        bool: True if the URL is an internal link to the application.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc == request.get_host()

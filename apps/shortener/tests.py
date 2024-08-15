import pytest
from django.urls import reverse
from apps.shortener.models import ShortURL


@pytest.mark.django_db
class TestShortURLModel:
    @pytest.fixture
    def short_url(self):
        return ShortURL.objects.create(url="https://www.example.com")

    def test_short_code_generation(self, short_url):
        """Test that the short code is generated correctly."""
        assert short_url.short_code is not None
        assert len(short_url.short_code) == 8

    def test_short_code_uniqueness(self):
        """Test that the short code is unique."""
        url1 = "https://www.example1.com"
        url2 = "https://www.example2.com"
        short_url1 = ShortURL.objects.create(url=url1)
        short_url2 = ShortURL.objects.create(url=url2)
        assert short_url1.short_code != short_url2.short_code

    def test_string_representation(self, short_url):
        """Test the string representation of the model."""
        expected_representation = f"ShortURL(short_code='{short_url.short_code}', url='{short_url.url}')"
        assert str(short_url) == expected_representation

    def test_save_does_not_overwrite_short_code(self, short_url):
        """Test that saving the object does not overwrite the short code."""
        original_short_code = short_url.short_code
        short_url.save()
        assert short_url.short_code == original_short_code

    def test_encode_existing_url(self, client):
        """Test that the same full URL is returned for the same original URL."""
        url = 'https://www.example.com'

        response1 = client.post(reverse('encode'), {'url': url})
        assert response1.status_code == 201
        full_url1 = response1.json()['url']

        response2 = client.post(reverse('encode'), {'url': url})
        assert response2.status_code == 200
        full_url2 = response2.json()['url']

        assert full_url1 == full_url2

    def test_decode(self, client):
        """Test the /decode endpoint."""
        url = 'https://www.example.com'

        response = client.post(reverse('encode'), {'url': url})
        assert response.status_code == 201
        short_code = response.json()['url'].split('/')[-1]  # Pobierz short_code z pełnego URL-a

        decode_response = client.get(reverse('decode', args=[short_code]))
        assert decode_response.status_code == 200
        data = decode_response.json()
        assert 'url' in data
        assert data['url'] == url

from django.db import models
import zlib


class ShortURL(models.Model):
    url: models.URLField = models.URLField(max_length=2048)
    short_code: models.CharField = models.CharField(max_length=8, unique=True, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)

    def generate_short_code(self) -> str:
        crc32_value = zlib.crc32(self.url.encode('utf-8'))
        short_code = format(crc32_value & 0xFFFFFFFF, '08x')

        while ShortURL.objects.filter(short_code=short_code).exists():
            crc32_value += 1
            short_code = format(crc32_value & 0xFFFFFFFF, '08x')

        return short_code

    def __str__(self) -> str:
        return f"ShortURL(short_code='{self.short_code}', url='{self.url}')"

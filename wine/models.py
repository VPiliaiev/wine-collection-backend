from django.db import models
import pathlib
from django.utils.text import slugify
import uuid


class WineType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Mood(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


def wine_image_path(instance: "Wine", filename: str) -> pathlib.Path:
    filename = (
            f"{slugify(instance.name)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/wine") / pathlib.Path(filename)


class Wine(models.Model):
    name = models.CharField(max_length=255, unique=True)
    volume = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Volume in liters"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    country = models.ForeignKey(
        "Country", on_delete=models.PROTECT, related_name="wines"
    )
    wine_type = models.ForeignKey(
        "WineType", on_delete=models.PROTECT, related_name="wines"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, related_name="wines"
    )
    moods = models.ManyToManyField("Mood", related_name="wines", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to=wine_image_path, blank=True)
    stock = models.PositiveIntegerField(default=0)
    purpose = models.ForeignKey("Purpose", on_delete=models.PROTECT, related_name="wines")

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name

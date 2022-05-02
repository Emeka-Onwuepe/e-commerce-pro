from django.db import models

# Create your models here.
class Location(models.Model):
    """Model definition for Location."""
    location = models.CharField(verbose_name="location", max_length=150)
    price = models.IntegerField(verbose_name="price")

    class Meta:
        """Meta definition for Location."""

        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        """Unicode representation of Location."""
        return f"{self.location} - {str(self.price)}"
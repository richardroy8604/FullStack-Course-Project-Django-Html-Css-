from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year_of_publication = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_pages = models.IntegerField()

    def __str__(self):
        return f"{self.name} by {self.author}"

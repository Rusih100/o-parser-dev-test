from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=300)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    rating = models.FloatField()
    comments_amount = models.IntegerField()
    delivery_date = models.CharField(max_length=30)
    tag = models.CharField(max_length=150)
    url = models.TextField(max_length=1000)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name})"

    __str__ = __repr__

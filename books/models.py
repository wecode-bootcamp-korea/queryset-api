from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'publishers'

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book)

    class Meta:
        db_table = 'stores'

    def __str__(self):
        return self.name

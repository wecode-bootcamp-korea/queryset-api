from django.db import models
#
#class Yest24QuerySet(models.QuerySet):
#    def get_best_store(self):
#        return self.first()
#
#class Yes24Manager(models.Manager):
#    def get_queryset(self):
#        return Yest24QuerySet(self.model, using=self._db).filter(type='yes24')
#
#    def get_best_store(self):
#        return self.get_queryset().get_best_store()
#
#    yes24_stores = Store.yes24_objects.all()
#    yes24_objects = Yes24Manager()
#    kybo_objects  = KyoboMnager()



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

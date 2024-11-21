from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=100)
    abv_name = models.CharField(max_length=15)
    email = models.CharField(max_length=60)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    number_managers = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name
    
class Cooperative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trade_license = models.FileField(upload_to='specs')
    number_of_members = models.IntegerField()
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    started_date = models.DateField()

class stock_management(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    quality = models.ForeignKey()
    quantity = models.IntegerField()
    date = models.DateTimeField()
    expired_date = models.DateTimeField()
    total_quantity_quality = models.IntegerField()
    

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

class Quality(models.Model):
    name = models.CharField(max_length=50) #adding choices of type
    std_temperature = models.DecimalField()
    std_humidity = models.DecimalField()
    seasons = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

class Stock_management(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    quality = models.ForeignKey(Quality, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField()
    expired_date = models.DateTimeField()
    total_quantity_quality = models.IntegerField()

class Fail_type(models.Model):
    name = models.CharField(max_length=100)
    error_detail = models.TextField(max_length=300)
    equipment = models.CharField(max_length=50)
    level = models.CharField()#choice add
    effect = models.CharField(max_length=20)

class System(models.Model):
    cooperative = models.OneToOneField(Cooperative, on_delete=models.CASCADE)
    fail_type = models.ManyToManyField(Fail_type)
    status = models.CharField(max_length=20) #add choices
    temperature_change = models.DecimalField()
    humidity_change = models.DecimalField()
    last_update = models.DateTimeField()
    failed = models.BooleanField()

class Notification(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    status = models.CharField(max_length=100)

class Message(models.Model):
    email = models.CharField(max_length=100)
    comment = models.TextField(max_length=500)
    reply = models.TextField(max_length=500)

class Geolocation(models.Model):
    cooperative = models.OneToOneField(Cooperative, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.CharField(max_length=200)
    
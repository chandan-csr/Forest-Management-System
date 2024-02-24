from django.db import models

# Create your models here.

class Forest(models.Model):
    f_name = models.CharField(max_length=30)
    f_type = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.f_name
    
class Product(models.Model):
    p_name = models.CharField(max_length=20)
    p_description = models.CharField(max_length=100)
    p_type = models.CharField(max_length=30)
    p_price = models.CharField(max_length=4)
    image = models.ImageField(upload_to='hello/media')
    gives = models.ManyToManyField(Forest)
    def __str__(self):
        return self.p_name

class Haulier(models.Model):
    h_name = models.CharField(max_length=20)
    h_address = models.CharField(max_length=40)
    city = models.CharField(max_length=30)
    phone = models.BigIntegerField()
    email = models.EmailField()
    transports = models.ManyToManyField(Product)
    def __str__(self):
        return self.h_name

class customer(models.Model):
    cust_name = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    email = models.EmailField()
    orders = models.ManyToManyField(Product)
    def __str__(self):
        return self.cust_name

class Visitors_pass(models.Model):
    date_of_visit = models.CharField(max_length=10)
    price = models.CharField(max_length=4)
    vpass = models.ForeignKey(customer, on_delete=models.CASCADE)
    def __str__(self):
        return self.date_of_visit
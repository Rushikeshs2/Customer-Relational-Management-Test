from django.db import models
from django.contrib.auth.models import User
from django import forms
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# Create your models here.
class Customers(models.Model):
    user = models.OneToOneField(User,null= True, on_delete =models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Out door','Out door'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null = True)
    category = models.CharField(max_length=200, null=True, choices = CATEGORY)
    description = models.CharField(max_length=200, null=True, blank = True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customers, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices = STATUS)
    note = models.CharField(max_length=1000, null=True, choices = STATUS)
    def __str__(self):
        return self.product.name

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'message from  ' + self.name + '   -' + self.email
class Newsletter(models.Model):
    email = models.CharField(max_length=100,default=False)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Subscribed for your newsletter  ' + self.email
class Score(models.Model):
    result = models.PositiveIntegerField()

    def __str__(self):
        return str(self.result)

class Barcode(models.Model):
    name = models.CharField(max_length=200)
    barcode = models.ImageField(upload_to='image/',blank=True)
    country_id = models.CharField(max_length=1,null=True)
    manufacturer_id = models.CharField(max_length=6,null=True)
    number_id = models.CharField(max_length=5,null=True)
    
    def __str__(self):
        return str(self.name)

    def save(self,*args,**kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f'{self.country_id}{self.manufacturer_id}{self.number_id}',writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save('barcode.png',File(buffer), save=False)
        return super().save(*args, **kwargs)
from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=30)
    category = models.CharField(max_length=30, default="")
    subcategory = models.CharField(max_length=30, default="")
    price = models.IntegerField(default=200)
    
    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

class Replacement(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    order_id=models.IntegerField(default="1111")
    product_name=models.CharField(max_length=30,default="")
    product_email=models.CharField(max_length=70,default="")
    password=models.CharField(max_length=70,default="")
    desc = models.CharField(max_length=500, default="")
    oid=models.CharField(max_length=100,default="")


    def __str__(self):
        return self.name

class Reset(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    order_id=models.IntegerField(default="1111") 
    product_name=models.CharField(max_length=30,default="")
    product_email=models.CharField(max_length=70,default="")
    password=models.CharField(max_length=70,default="")
    desc = models.CharField(max_length=500, default="")
    oid=models.CharField(max_length=100,default="")


    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    oid=models.CharField(max_length=100,default="")
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField( default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    phone = models.CharField(max_length=10, default="")
    code = models.CharField(max_length=15,default="")

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    oid=models.CharField(max_length=100,default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
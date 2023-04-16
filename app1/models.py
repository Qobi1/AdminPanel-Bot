from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    ctg = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField()
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class User(models.Model):
    state = models.IntegerField(null=True)
    user_id = models.BigIntegerField()
    language = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=256, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    log = models.JSONField()

    def __str__(self):
        return self.user_id


class Orders(models.Model):
    user_id = models.BigIntegerField()
    phone_number = models.CharField(max_length=50)
    quantity = models.IntegerField()
    image = models.ImageField()
    product = models.CharField(max_length=256)
    ctg = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


class Messages(models.Model):
    image = models.ImageField(null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at
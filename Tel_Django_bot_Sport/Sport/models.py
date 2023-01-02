from django.db import models

class Clients(models.Model):
    clients_id = models.IntegerField()
    password = models.CharField(max_length=50)
    time_autorization = models.FloatField(default=0.0)
    cash_account = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.clients_id}"


class Treiner_warker(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Schedule_treiner(models.Model):
    weekday = models.CharField(max_length=20)
    treiner_name = models.ForeignKey(Treiner_warker, on_delete=models.CASCADE)
    time_training = models.CharField(max_length=20)
    clients = models.ForeignKey(Clients, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.weekday}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}, {self.price}"


class User_product(models.Model):
    clients = models.ForeignKey(Clients, on_delete=models.CASCADE)
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}, {self.price}"
from django.db import models
from products.models import Product

from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # Payment method is implicitly Cash on Delivery as per requirements

    def __str__(self):
        return f"Order #{self.id} by {self.full_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

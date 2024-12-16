from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]  # Use Decimal for validation
    )
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.title} - {self.amount}"
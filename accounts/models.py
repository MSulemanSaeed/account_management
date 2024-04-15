from django.db import models
from django.core.exceptions import ValidationError

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def total_amount(self):
        return self.balance

class Transaction(models.Model):
    DEBIT = 'd'
    CREDIT = 'c'
    TRANSACTION_TYPES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, null=True)  
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.transaction_type == self.DEBIT and self.amount > 100000:
            raise ValidationError("Can't Debit more than 100,000 Rs")
        elif self.transaction_type == self.CREDIT:
            if self.amount > self.account.total_amount:
                raise ValidationError("Credit amount must not exceed total amount")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.transaction_type == self.DEBIT:
            self.account.balance += self.amount
        elif self.transaction_type == self.CREDIT:
            self.account.balance -= self.amount
        self.account.save()

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"
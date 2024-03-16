from django.db import models

from jwtAuth.models import User


# Create your models here.

class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY '),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE-HUSTLES', 'SIDE-HUSTLES'),
        ('OTHERS', 'OTHERS')
    ]

    source = models.CharField(max_length=255, choices=SOURCE_OPTIONS)
    amount = models.DecimalField(max_length=255, max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    # Ordering the incomes by date
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner) + 's income'

from django.db import models
from .production import Production

class ProdOperation(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    plan = models.PositiveIntegerField()
    actual = models.PositiveIntegerField()
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='operations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
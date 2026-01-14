from django.db import models
from mecs.apps.master.models import RejectCategory

from .prod_operation import ProdOperation

class ProdReject(models.Model):
    quantity = models.PositiveIntegerField()
    reject_photo = models.ImageField(upload_to='reject_photos/', null=True, blank=True)
    reject_category = models.ForeignKey(RejectCategory, on_delete=models.CASCADE)
    prod_operation = models.ForeignKey(ProdOperation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
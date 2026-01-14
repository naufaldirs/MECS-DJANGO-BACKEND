from django.db import models
from mecs.apps.master.models import ProblemCategory
from .prod_operation import ProdOperation
class ProdProblem(models.Model):
    duration = models.DurationField()
    action = models.TextField()
    problem_category = models.ForeignKey(ProblemCategory, on_delete=models.CASCADE)
    prod_operation = models.ForeignKey(ProdOperation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

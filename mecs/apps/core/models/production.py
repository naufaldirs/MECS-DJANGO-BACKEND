from django.db import models
from mecs.apps.accounts.models import User,Operator
from mecs.apps.master.models import Machine, ProductionParameter
from .schedule import Schedule
class Production(models.Model):
    total_shoots = models.PositiveIntegerField()
    preheat = models.PositiveIntegerField()
    target_pcs = models.PositiveIntegerField()
    work_time = models.FloatField(help_text='Work time in hours')
    actual_total = models.PositiveIntegerField()
    reject_total = models.PositiveIntegerField()
    downtime_total = models.FloatField(help_text='Downtime in hours')
    status_process = models.CharField(
        max_length=20,
        choices=[
            ('planned', 'Planned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        default='planned'
    )
    mode_status = models.CharField(
        max_length=20,
        choices=[
            ('normal', 'Normal'),
            ('overtime', 'Overtime'),
            ('dandory', 'Dandory')
        ],
        default='normal'
    )
     
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True, blank=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prod_parameter = models.ForeignKey(ProductionParameter, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
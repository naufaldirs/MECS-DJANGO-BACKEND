from django.db import models
class DailyProduction(models.Model):
    production_date = models.DateField(unique=True)

    target_output = models.PositiveIntegerField()
    worktime_output = models.PositiveIntegerField()
    actual_output = models.PositiveIntegerField()
    reject_output = models.PositiveIntegerField()
    downtime_output = models.FloatField(help_text='Downtime in hours')

    status = models.CharField(
        max_length=20,
        choices=[('open', 'Open'), ('approved', 'Approved')],
        default='open'
    )

    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_reports'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

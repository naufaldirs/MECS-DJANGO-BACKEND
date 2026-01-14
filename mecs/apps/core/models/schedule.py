from django.db import models
from .daily_production import DailyProduction

class Schedule(models.Model):
    SHIFT_1 = 1
    SHIFT_2 = 2
    SHIFT_3 = 3

    SHIFT_CHOICES = (
        (SHIFT_1, 'Shift 1'),
        (SHIFT_2, 'Shift 2'),
        (SHIFT_3, 'Shift 3'),
    )

    scheduled_time = models.DateTimeField()
    shift = models.PositiveSmallIntegerField(choices=SHIFT_CHOICES)
    daily_production = models.ForeignKey(DailyProduction, on_delete=models.CASCADE, related_name='schedules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('scheduled_time', 'shift')
        ordering = ['scheduled_time', 'shift']

    def __str__(self):
        return f"{self.scheduled_time} | Shift {self.shift}"

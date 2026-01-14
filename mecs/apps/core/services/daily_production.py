from django.db  import models
from django.utils import timezone
from datetime import time

from mecs.apps.core.models import DailyProduction, Schedule
from mecs.apps.master.models import Shift

from django.db import transaction
from django.utils import timezone
from datetime import datetime

from mecs.apps.core.models import DailyProduction, Schedule
from mecs.apps.core.constants.shift import SHIFT_TIMES


@transaction.atomic
def create_daily_production(production_date, status='open'):
    if DailyProduction.objects.filter(production_date=production_date).exists():
        raise ValueError('Daily production for this date already exists')

    daily = DailyProduction.objects.create(
        production_date=production_date,
        status=status,
    )

    for shift, shift_time in SHIFT_TIMES.items():
        prod_time = timezone.make_aware(
            datetime.combine(production_date, shift_time)
        )

        Schedule.objects.create(
            daily_production_id=daily,
            shift=shift,
            scheduled_time=prod_time,
        )

    return daily

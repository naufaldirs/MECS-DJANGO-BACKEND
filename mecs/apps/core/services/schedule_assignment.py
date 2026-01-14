from django.db import transaction
from django.utils import timezone
from datetime import datetime

from mecs.apps.core.models import Schedule, Production, ProdOperation


TARGET_TIME_MAP = {
    6: 5.5,
    7: 6.5,
    8: 7.5,
}

@transaction.atomic
def assign_production_to_schedule(
    schedule_id,
    *,
    machine,
    prod_parameter,
    target_time,
    target_pcs,
    status,
    details,
):
    schedule = Schedule.objects.select_for_update().get(id=schedule_id)

    work_time = TARGET_TIME_MAP.get(target_time, target_time)

    production, _ = Production.objects.get_or_create(
        schedule=schedule,
        machine=machine,
    )

    production.prod_parameter = prod_parameter
    production.work_time = work_time
    production.target_pcs = target_pcs
    production.mode_status = status
    production.save()

    # Hapus operation lama
    production.prod_operation.all().delete()

    # Create operation baru
    for item in details:
        start_time = timezone.make_aware(
            datetime.fromisoformat(item['start_time'].strip())
        )
        end_time = timezone.make_aware(
            datetime.fromisoformat(item['end_time'].strip())
        )

        ProdOperation.objects.create(
            production=production,
            start_time=start_time,
            end_time=end_time,
            plan=item['plan'],
            actual=item.get('actual', 0),
        )

    return production

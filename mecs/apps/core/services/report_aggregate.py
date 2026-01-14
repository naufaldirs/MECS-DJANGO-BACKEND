import mecs.apps.core.models.daily_production as DailyProduction

def build_published_reports():
    reports = DailyProduction.objects.prefetch_related(
        'schedules__productions__prod_parameter'
    ).filter(
        schedules__status='open'
    ).distinct()

    result = []

    for report in reports:
        total_ascast = 0
        total_scrub = 0

        for schedule in report.schedules.all():
            for prod in schedule.productions.all():
                param = prod.prod_parameter
                if param:
                    total_ascast += param.ascast or 0
                    total_scrub += param.runner or 0

        result.append({
            'daily_production_id': report.id,
            'production_date': report.production_date,
            'total_ascast': total_ascast,
            'total_scrub': total_scrub,
            'total_ingot': total_ascast + total_scrub,
        })

    return result

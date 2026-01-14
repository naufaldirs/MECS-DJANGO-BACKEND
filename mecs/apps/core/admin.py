from django.contrib import admin

from mecs.apps.core.models import (
    DailyProduction,
    Schedule,
    Production,
    ProdOperation,
    ProdProblem,
    ProdReject,
)

@admin.register(DailyProduction)
class DailyProductionAdmin(admin.ModelAdmin):
    list_display = (
        'production_date',
        'status',
        'approved_at',
        'approved_by',
    )

    list_filter = (
        'status',
        'production_date',
    )

    search_fields = ('production_date',)
    ordering = ('-production_date',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'scheduled_time',
        'shift_label',
        'created_at',
    )

    list_filter = (
        'shift',
        'scheduled_time',
    )

    ordering = ('scheduled_time',)

    def shift_label(self, obj):
        return obj.get_shift_display()

    shift_label.short_description = 'Shift'

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'machine',
        'schedule',
        'status_process',
        'mode_status',
        'target_pcs',
        'actual_total',
        'reject_total',
    )

    list_filter = (
        'status_process',
        'mode_status',
        'machine',
    )

    search_fields = (
        'machine__name',
    )

    readonly_fields = (
        'actual_total',
        'reject_total',
        'downtime_total',
        'total_shoots',
        'created_at',
        'updated_at',
    )

@admin.register(ProdOperation)
class ProdOperationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'production',
        'start_time',
        'end_time',
        'plan',
        'actual',
    )

    list_filter = (
        'start_time',
    )

    ordering = ('-start_time',)

@admin.register(ProdProblem)
class ProdProblemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'problem_category',
        'prod_operation',
        'duration',
        'created_at',
    )

    list_filter = (
        'problem_category',
    )

    search_fields = (
        'action',
    )

@admin.register(ProdReject)
class ProdRejectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reject_category',
        'prod_operation',
        'quantity',
        'created_at',
    )

    list_filter = (
        'reject_category',
    )

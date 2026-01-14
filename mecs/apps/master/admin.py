from django.contrib import admin
from .models import Customer, Machine, Part, ProductionParameter, Shift, ProductionCapacity
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'name', 'address')
    search_fields = ('customer_code', 'name')

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'line_address', 'status')
    list_filter = ('status',)

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'part_name', 'model', 'customer')
    search_fields = ('part_number', 'part_name')
    list_filter = ('customer',)

@admin.register(ProductionParameter)
class ProductionParameterAdmin(admin.ModelAdmin):
    list_display = ('part', 'cavity', 'runner', 'shot_weight', 'ascast', 'cycle_time')
    search_fields = ('part__part_number', 'part__part_name')

@admin.register(ProductionCapacity)
class ProductionCapacityAdmin(admin.ModelAdmin):
    list_display = ('prod_parameter', 'normal_kg', 'overtime_kg', 'dandory_kg', 'one_hour_pcs', 'six_hour_pcs', 'seven_hour_pcs', 'eight_hour_pcs')
    search_fields = ('prod_parameter__part__part_number', 'prod_parameter__part__part_name')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')
    search_fields = ('name',)
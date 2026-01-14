from django.db import models
class Customer(models.Model):
    customer_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)

class Machine(models.Model):
    name = models.CharField(max_length=100)
    line_address = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20,
                            choices=[('active', 'Active'), ('inactive', 'Inactive')],
                            default='active')
    def __str__(self):
        return self.name
    
class Part(models.Model):
    part_number = models.CharField(max_length=50, unique=True)
    part_name = models.CharField(max_length=150)
    model = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='parts/', blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return f"{self.part_number} - {self.part_name}"

class ProductionParameter(models.Model):
    type = models.CharField(max_length=100, blank=True)
    cavity = models.PositiveIntegerField()
    runner = models.FloatField(help_text='Runner weight (kg)')
    shot_weight = models.FloatField(help_text='Shot weight (kg)')
    ascast = models.FloatField(help_text='As-cast weight (kg)')
    cycle_time = models.FloatField(help_text='Cycle time (seconds)', null=True, blank=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Parameters for {self.part.part_number}"

class ProductionCapacity(models.Model):
    normal_kg = models.FloatField(help_text='Normal production capacity (kg/hour)')
    overtime_kg = models.FloatField(help_text='Overtime production capacity (kg/hour)')
    dandory_kg = models.FloatField(help_text='Dandory production capacity (kg/hour)')
    one_hour_pcs = models.PositiveIntegerField(help_text='One hour production capacity (pieces/hour)')
    six_hour_pcs = models.PositiveIntegerField(help_text='Six hour production capacity (pieces/6 hours)')
    seven_hour_pcs = models.PositiveIntegerField(help_text='Seven hour production capacity (pieces/7 hours)')
    eight_hour_pcs = models.PositiveIntegerField(help_text='Eight hour production capacity (pieces/8 hours)')
    prod_parameter = models.OneToOneField(ProductionParameter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Capacity for {self.prod_parameter.part.part_number}"
    
class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name

class ProblemCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    solution = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RejectCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sample_photo = models.ImageField(upload_to='rejects/', blank=True, null=True)
    def __str__(self):
        return self.name
    

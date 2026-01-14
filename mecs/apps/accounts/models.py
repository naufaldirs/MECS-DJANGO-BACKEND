from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10,
        choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')],
        blank=True
    )
    phone_number = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='employee/', blank=True, null=True)

    def __str__(self):
        return f"{self.nip} - {self.full_name}"
    
class User(AbstractUser):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username
    
class Operator(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    group = models.CharField(max_length=50)

    def __str__(self):
        return f"Operator: {self.employee.full_name} - Group: {self.group}"
    

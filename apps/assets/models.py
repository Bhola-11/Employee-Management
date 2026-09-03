from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class AssetCategory(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='asset_categories')
    name = models.CharField(max_length=100) # Laptops & MacBooks, Monitors, Mobile Devices, Access Keycards, Office Desks
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Asset(TimeStampedModel):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available in Inventory'),
        ('ALLOCATED', 'Allocated to Employee'),
        ('UNDER_MAINTENANCE', 'Under Maintenance / Repair'),
        ('RETIRED', 'Retired / Disposed'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='assets')
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='assets')
    asset_tag = models.CharField(max_length=50, unique=True) # e.g. AST-MBP-9021
    name = models.CharField(max_length=200) # e.g. Apple MacBook Pro 16" M3 Max
    serial_number = models.CharField(max_length=100, unique=True)
    model_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    warranty_expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='AVAILABLE')
    assigned_to = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_assets')
    assigned_date = models.DateField(null=True, blank=True)
    specifications = models.TextField(blank=True)

    class Meta:
        ordering = ['asset_tag']

    def __str__(self):
        return f"[{self.asset_tag}] {self.name} ({self.status})"

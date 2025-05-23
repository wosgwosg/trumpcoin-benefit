from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import uuid

# User Profile Model
class UserProfile(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20)
    address = models.TextField()
    dob = models.DateField()
    country = models.CharField(max_length=100)
    ssn_or_id = models.CharField(max_length=20)
    verification_status = models.CharField(
        max_length=10, 
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# Bank Details Model
class BankDetails(models.Model):
    ACTIVATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    AMOUNT_CHOICES = [
        (1000, '$1,000'),
        (5000, '$5,000'),
        (10000, '$10,000'),
        (25000, '$25,000'),
        (50000, '$50,000'),
    ]
    
    bank_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=30)
    routing_number = models.CharField(max_length=20)
    amount_to_apply = models.IntegerField(choices=AMOUNT_CHOICES, default=1000)
    activation_deposit_status = models.CharField(
        max_length=10,
        choices=ACTIVATION_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Bank Details"

# Application Model
class Application(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    ]
    
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='application')
    unique_tracking_code = models.CharField(max_length=20, unique=True, blank=True)
    application_status = models.CharField(
        max_length=10,
        choices=APPLICATION_STATUS_CHOICES,
        default='pending'
    )
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activation_deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.unique_tracking_code:
            # Generate a unique tracking code in the format TRUMP-PR-XXXXX
            random_part = get_random_string(5, '0123456789')
            self.unique_tracking_code = f"TRUMP-PR-{random_part}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}'s Application ({self.unique_tracking_code})"

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('activation', 'Activation Deposit'),
        ('admin_credit', 'Admin Credit'),
        ('disbursement', 'Disbursement'),
    ]
    
    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=15,
        choices=TRANSACTION_TYPE_CHOICES
    )
    transaction_status = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s {self.get_transaction_type_display()} - {self.amount}"

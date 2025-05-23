from django.contrib import admin
from .models import UserProfile, BankDetails, Application, Transaction

# Register models with customized admin views
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'country', 'verification_status', 'created_at')
    list_filter = ('verification_status', 'country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'ssn_or_id')
    readonly_fields = ('created_at',)

@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'amount_to_apply', 'activation_deposit_status', 'created_at')
    list_filter = ('activation_deposit_status', 'amount_to_apply', 'created_at')
    search_fields = ('user__username', 'user__email', 'bank_name', 'account_number')
    readonly_fields = ('bank_id', 'created_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'unique_tracking_code', 'application_status', 'approved_amount', 'created_at', 'updated_at')
    list_filter = ('application_status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'unique_tracking_code')
    readonly_fields = ('application_id', 'unique_tracking_code', 'created_at', 'updated_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'transaction_status', 'created_at')
    list_filter = ('transaction_type', 'transaction_status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('transaction_id', 'created_at')

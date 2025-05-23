from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from .models import UserProfile, BankDetails, Application, Transaction

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

# Admin Dashboard Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view"""
    # Get counts for different application statuses
    pending_count = Application.objects.filter(application_status='pending').count()
    approved_count = Application.objects.filter(application_status='approved').count()
    rejected_count = Application.objects.filter(application_status='rejected').count()
    disbursed_count = Application.objects.filter(application_status='disbursed').count()
    
    # Get recent applications
    recent_applications = Application.objects.all().order_by('-created_at')[:10]
    
    context = {
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'disbursed_count': disbursed_count,
        'recent_applications': recent_applications
    }
    
    return render(request, 'benefit/admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def applicant_list(request):
    """List of all applicants with filtering"""
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    applications = Application.objects.all()
    
    # Apply status filter if provided
    if status_filter:
        applications = applications.filter(application_status=status_filter)
    
    # Apply search filter if provided
    if search_query:
        applications = applications.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(unique_tracking_code__icontains=search_query)
        )
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'search_query': search_query
    }
    
    return render(request, 'benefit/admin/applicant_list.html', context)

@login_required
@user_passes_test(is_admin)
def applicant_detail(request, tracking_code):
    """Detailed view of an applicant"""
    application = get_object_or_404(Application, unique_tracking_code=tracking_code)
    user = application.user
    profile = UserProfile.objects.get(user=user)
    bank_details = BankDetails.objects.get(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'application': application,
        'user': user,
        'profile': profile,
        'bank_details': bank_details,
        'transactions': transactions
    }
    
    return render(request, 'benefit/admin/applicant_detail.html', context)

@login_required
@user_passes_test(is_admin)
def update_application_status(request, tracking_code):
    """Update application status"""
    if request.method == 'POST':
        application = get_object_or_404(Application, unique_tracking_code=tracking_code)
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        
        if new_status in ['pending', 'approved', 'rejected', 'disbursed']:
            application.application_status = new_status
            application.admin_notes = admin_notes
            application.save()
            
            # Send email notification to user
            subject = f'TrumpCoin Benefit Application Update: {new_status.capitalize()}'
            message = f'Dear {application.user.first_name},\n\nYour TrumpCoin Benefit application ({tracking_code}) has been updated to: {new_status.capitalize()}.\n\n'
            
            if admin_notes:
                message += f'Admin Notes: {admin_notes}\n\n'
            
            message += 'Thank you for your application.\n\nTrumpCoin Benefit Team'
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [application.user.email],
                fail_silently=False,
            )
            
            messages.success(request, f'Application status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('applicant_detail', tracking_code=tracking_code)

@login_required
@user_passes_test(is_admin)
def add_transaction(request, tracking_code):
    """Add a transaction to user account"""
    if request.method == 'POST':
        application = get_object_or_404(Application, unique_tracking_code=tracking_code)
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
                
            if transaction_type in ['activation', 'admin_credit', 'disbursement']:
                # Create transaction
                transaction = Transaction.objects.create(
                    user=application.user,
                    amount=amount,
                    transaction_type=transaction_type,
                    transaction_status='completed'
                )
                
                # If this is an activation deposit, update bank details
                if transaction_type == 'activation':
                    bank_details = BankDetails.objects.get(user=application.user)
                    bank_details.activation_deposit_status = 'completed'
                    bank_details.save()
                
                # Send email notification to user
                subject = f'TrumpCoin Benefit: New Transaction'
                message = f'Dear {application.user.first_name},\n\nA new transaction has been added to your account:\n\n'
                message += f'Amount: ${amount}\n'
                message += f'Type: {transaction.get_transaction_type_display()}\n'
                message += f'Status: Completed\n\n'
                message += 'Thank you for your application.\n\nTrumpCoin Benefit Team'
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [application.user.email],
                    fail_silently=False,
                )
                
                messages.success(request, f'Transaction of ${amount} added successfully.')
            else:
                messages.error(request, 'Invalid transaction type.')
        except ValueError:
            messages.error(request, 'Invalid amount. Please enter a positive number.')
    
    return redirect('applicant_detail', tracking_code=tracking_code)

@login_required
@user_passes_test(is_admin)
def delete_applicant(request, tracking_code):
    """Delete an applicant and all associated data"""
    if request.method == 'POST':
        application = get_object_or_404(Application, unique_tracking_code=tracking_code)
        user = application.user
        
        # Send notification email before deletion
        subject = 'TrumpCoin Benefit: Account Deleted'
        message = f'Dear {user.first_name},\n\nYour TrumpCoin Benefit application and account have been deleted.\n\n'
        message += 'If you believe this is an error, please contact our support team.\n\nTrumpCoin Benefit Team'
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except:
            # Continue with deletion even if email fails
            pass
        
        # Delete the user (this will cascade delete all related objects)
        user.delete()
        
        messages.success(request, 'Applicant and all associated data deleted successfully.')
        return redirect('applicant_list')
    
    return redirect('applicant_detail', tracking_code=tracking_code)

@login_required
@user_passes_test(is_admin)
def send_message(request, tracking_code):
    """Send a custom message to a user"""
    if request.method == 'POST':
        application = get_object_or_404(Application, unique_tracking_code=tracking_code)
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')
        
        if subject and message_body:
            # Send email
            full_message = f'Dear {application.user.first_name},\n\n{message_body}\n\nTrumpCoin Benefit Team'
            
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [application.user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Message sent successfully.')
        else:
            messages.error(request, 'Subject and message are required.')
    
    return redirect('applicant_detail', tracking_code=tracking_code)

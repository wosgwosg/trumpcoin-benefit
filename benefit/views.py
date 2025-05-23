from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum

from .forms import UserRegistrationForm, UserProfileForm, BankDetailsForm, ContactForm
from .models import UserProfile, BankDetails, Application, Transaction

# Public Pages
def home(request):
    """Home page view"""
    return render(request, 'benefit/home.html')

def overview(request):
    """Overview page with program details"""
    return render(request, 'benefit/overview.html')

def faq(request):
    """FAQ page"""
    return render(request, 'benefit/faq.html')

def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email (in production, this would send an actual email)
            send_mail(
                f'Contact Form: {subject}',
                f'From: {name} ({email})\n\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'benefit/contact.html', {'form': form})

# Authentication Views
def register_step1(request):
    """Step 1 of registration: Personal details"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save user data to session for step 2
            request.session['user_data'] = user_form.cleaned_data
            request.session['profile_data'] = profile_form.cleaned_data
            
            # Convert date object to string for session storage
            request.session['profile_data']['dob'] = request.session['profile_data']['dob'].strftime('%Y-%m-%d')
            
            return redirect('register_step2')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'benefit/register_step1.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def register_step2(request):
    """Step 2 of registration: Bank details"""
    # Check if step 1 was completed
    if 'user_data' not in request.session or 'profile_data' not in request.session:
        messages.error(request, 'Please complete step 1 first.')
        return redirect('register_step1')
    
    if request.method == 'POST':
        bank_form = BankDetailsForm(request.POST)
        
        if bank_form.is_valid():
            # Create user
            user_data = request.session['user_data']
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password1'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            # Create profile
            profile_data = request.session['profile_data']
            profile = UserProfile.objects.create(
                user=user,
                phone=profile_data['phone'],
                address=profile_data['address'],
                dob=profile_data['dob'],
                country=profile_data['country'],
                ssn_or_id=profile_data['ssn_or_id']
            )
            
            # Create bank details
            bank_details = bank_form.save(commit=False)
            bank_details.user = user
            bank_details.save()
            
            # Create application
            application = Application.objects.create(
                user=user,
                activation_deposit_amount=bank_details.amount_to_apply * 0.1  # 10% of requested amount
            )
            
            # Clean up session
            del request.session['user_data']
            del request.session['profile_data']
            
            # Log the user in
            login(request, user)
            
            messages.success(request, 'Registration successful! Your application has been submitted.')
            return redirect('dashboard')
    else:
        bank_form = BankDetailsForm()
    
    return render(request, 'benefit/register_step2.html', {'bank_form': bank_form})

# User Dashboard Views
@login_required
def dashboard(request):
    """User dashboard view"""
    try:
        application = Application.objects.get(user=request.user)
        bank_details = BankDetails.objects.get(user=request.user)
        
        # Get total balance from completed transactions
        balance = Transaction.objects.filter(
            user=request.user,
            transaction_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        context = {
            'application': application,
            'bank_details': bank_details,
            'balance': balance
        }
        
        return render(request, 'benefit/dashboard.html', context)
    except (Application.DoesNotExist, BankDetails.DoesNotExist):
        messages.error(request, 'Your application is incomplete. Please contact support.')
        return redirect('home')

@login_required
def application_status(request):
    """Application status tracking view"""
    try:
        application = Application.objects.get(user=request.user)
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
        
        context = {
            'application': application,
            'transactions': transactions
        }
        
        return render(request, 'benefit/application_status.html', context)
    except Application.DoesNotExist:
        messages.error(request, 'No application found.')
        return redirect('dashboard')

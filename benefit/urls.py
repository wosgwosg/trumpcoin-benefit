from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import admin_views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('overview/', views.overview, name='overview'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register_step1, name='register_step1'),
    path('register/step2/', views.register_step2, name='register_step2'),
    path('login/', auth_views.LoginView.as_view(template_name='benefit/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='benefit/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='benefit/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='benefit/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='benefit/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('application-status/', views.application_status, name='application_status'),
    
    # Admin dashboard
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/applicants/', admin_views.applicant_list, name='applicant_list'),
    path('admin-dashboard/applicant/<str:tracking_code>/', admin_views.applicant_detail, name='applicant_detail'),
    path('admin-dashboard/applicant/<str:tracking_code>/update-status/', admin_views.update_application_status, name='update_application_status'),
    path('admin-dashboard/applicant/<str:tracking_code>/add-transaction/', admin_views.add_transaction, name='add_transaction'),
    path('admin-dashboard/applicant/<str:tracking_code>/delete/', admin_views.delete_applicant, name='delete_applicant'),
    path('admin-dashboard/applicant/<str:tracking_code>/send-message/', admin_views.send_message, name='send_message'),
]

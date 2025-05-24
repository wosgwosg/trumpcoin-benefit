// TrumpCoin Benefit Program Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Password strength meter
    var passwordInput = document.getElementById('id_password1');
    if (passwordInput) {
        var strengthMeter = document.createElement('div');
        strengthMeter.className = 'progress mt-2';
        strengthMeter.innerHTML = '<div class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>';
        passwordInput.parentNode.appendChild(strengthMeter);
        
        var progressBar = strengthMeter.querySelector('.progress-bar');
        
        passwordInput.addEventListener('input', function() {
            var strength = 0;
            var password = this.value;
            
            if (password.length >= 8) strength += 25;
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 25;
            if (password.match(/\d/)) strength += 25;
            if (password.match(/[^a-zA-Z\d]/)) strength += 25;
            
            progressBar.style.width = strength + '%';
            progressBar.setAttribute('aria-valuenow', strength);
            
            if (strength < 50) {
                progressBar.className = 'progress-bar bg-danger';
            } else if (strength < 75) {
                progressBar.className = 'progress-bar bg-warning';
            } else {
                progressBar.className = 'progress-bar bg-success';
            }
        });
    }
    
    // Copy tracking code to clipboard
    var trackingCodeElement = document.querySelector('.tracking-code');
    if (trackingCodeElement) {
        trackingCodeElement.addEventListener('click', function() {
            var code = this.textContent;
            navigator.clipboard.writeText(code).then(function() {
                var tooltip = bootstrap.Tooltip.getInstance(trackingCodeElement);
                if (tooltip) {
                    tooltip.dispose();
                }
                trackingCodeElement.setAttribute('data-bs-original-title', 'Copied!');
                var newTooltip = new bootstrap.Tooltip(trackingCodeElement);
                newTooltip.show();
                
                setTimeout(function() {
                    trackingCodeElement.setAttribute('data-bs-original-title', 'Click to copy');
                }, 2000);
            });
        });
    }
    
    // Admin dashboard charts (if Chart.js is included)
    if (typeof Chart !== 'undefined') {
        // Applications by status chart
        var statusChartCanvas = document.getElementById('statusChart');
        if (statusChartCanvas) {
            var pendingCount = parseInt(statusChartCanvas.getAttribute('data-pending') || 0);
            var approvedCount = parseInt(statusChartCanvas.getAttribute('data-approved') || 0);
            var rejectedCount = parseInt(statusChartCanvas.getAttribute('data-rejected') || 0);
            var disbursedCount = parseInt(statusChartCanvas.getAttribute('data-disbursed') || 0);
            
            new Chart(statusChartCanvas, {
                type: 'doughnut',
                data: {
                    labels: ['Pending', 'Approved', 'Rejected', 'Disbursed'],
                    datasets: [{
                        data: [pendingCount, approvedCount, rejectedCount, disbursedCount],
                        backgroundColor: ['#ffc107', '#28a745', '#dc3545', '#17a2b8'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        position: 'bottom'
                    }
                }
            });
        }
    }
});

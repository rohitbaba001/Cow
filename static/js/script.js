// Auto-hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.alert');
    
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(function(button) {
        if (!button.classList.contains('no-confirm')) {
            button.addEventListener('click', function(e) {
                const confirmed = confirm('Are you sure you want to proceed?');
                if (!confirmed) {
                    e.preventDefault();
                }
            });
        }
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = 'var(--danger-color)';
                } else {
                    field.style.borderColor = 'var(--border-color)';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Highlight overdue tasks
    const today = new Date();
    const taskRows = document.querySelectorAll('.data-table tbody tr');
    
    taskRows.forEach(function(row) {
        const deadlineCell = row.querySelector('td:nth-child(3)');
        if (deadlineCell) {
            const deadlineText = deadlineCell.textContent.trim();
            // Simple check - you might need to adjust based on your date format
            if (deadlineText) {
                const statusCell = row.querySelector('.badge');
                if (statusCell && !statusCell.classList.contains('badge-completed')) {
                    // Add visual indicator for overdue items
                    const deadline = new Date(deadlineText);
                    if (deadline < today) {
                        row.classList.add('overdue-row');
                    }
                }
            }
        }
    });
});

// Language switcher
function changeLanguage(lang) {
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
}

// Image preview for file uploads
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create preview if it doesn't exist
                    let preview = input.parentElement.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview';
                        preview.style.maxWidth = '200px';
                        preview.style.marginTop = '10px';
                        preview.style.borderRadius = '4px';
                        input.parentElement.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Mobile menu toggle (if needed)
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

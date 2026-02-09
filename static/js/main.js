// StyleAI Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize file upload functionality
    initializeFileUpload();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize tooltips
    initializeTooltips();
});

// File Upload Handling
function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            const fileNameDisplay = this.parentElement.querySelector('.file-name');
            
            if (fileName) {
                fileNameDisplay.textContent = `Selected: ${fileName}`;
                fileNameDisplay.style.color = '#28a745';
            } else {
                fileNameDisplay.textContent = '';
            }
            
            // Preview image if it's an image file
            if (this.files && this.files[0] && this.files[0].type.startsWith('image/')) {
                previewImage(this);
            }
        });
    });
}

function previewImage(input) {
    const file = input.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        // Create or update preview
        let preview = input.parentElement.querySelector('.image-preview');
        if (!preview) {
            preview = document.createElement('div');
            preview.className = 'image-preview';
            input.parentElement.appendChild(preview);
        }
        
        preview.innerHTML = `
            <img src="${e.target.result}" alt="Preview" style="max-width: 200px; max-height: 200px; border-radius: 8px; margin-top: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        `;
    };
    
    if (file) {
        reader.readAsDataURL(file);
    }
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            showLoadingState(form);
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showError(field, 'This field is required');
            isValid = false;
        } else {
            clearError(field);
        }
        
        // Specific validation for file inputs
        if (field.type === 'file' && field.files.length === 0) {
            showError(field, 'Please select a file');
            isValid = false;
        }
        
        // File type validation
        if (field.type === 'file' && field.files.length > 0) {
            const file = field.files[0];
            const maxSize = 16 * 1024 * 1024; // 16MB
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
            
            if (file.size > maxSize) {
                showError(field, 'File size must be less than 16MB');
                isValid = false;
            }
            
            if (!allowedTypes.includes(file.type)) {
                showError(field, 'Please upload a valid image file (JPG, PNG, GIF)');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

function showError(field, message) {
    clearError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '5px';
    
    field.parentNode.appendChild(errorDiv);
    field.style.borderColor = '#dc3545';
}

function clearError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.style.borderColor = '#e9ecef';
}

function showLoadingState(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitButton.disabled = true;
        
        // Store original text for later restoration
        submitButton.dataset.originalText = originalText;
    }
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

function showTooltip(element) {
    const tooltipText = element.getAttribute('data-tooltip');
    if (!tooltipText) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = tooltipText;
    tooltip.style.cssText = `
        position: absolute;
        background: #333;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.875rem;
        z-index: 1000;
        pointer-events: none;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
    
    element.tooltipElement = tooltip;
}

function hideTooltip(element) {
    if (element.tooltipElement) {
        element.tooltipElement.remove();
        delete element.tooltipElement;
    }
}

// Color Palette Visualization
function visualizeColorPalette() {
    const swatchColors = {
        'navy blue': '#000080',
        'emerald green': '#50C878',
        'burgundy': '#800020',
        'charcoal': '#36454F',
        'soft pink': '#FFB6C1',
        'lavender': '#E6E6FA',
        'mint green': '#98FF98',
        'peach': '#FFE5B4',
        'gold': '#FFD700',
        'coral': '#FF7F50',
        'turquoise': '#40E0D0',
        'neon yellow': '#FFFF33',
        'orange': '#FFA500',
        'beige': '#F5F5DC',
        'royal blue': '#4169E1',
        'crimson': '#DC143C',
        'forest green': '#228B22',
        'plum': '#8E4585',
        'teal': '#008080',
        'lemon yellow': '#FFF44F',
        'magenta': '#FF00FF',
        'silver': '#C0C0C0',
        'bronze': '#CD7F32',
        'fuchsia': '#FF00FF',
        'brown': '#A52A2A',
        'muted olive': '#808000',
        'cream': '#FFFDD0',
        'rust': '#B7410E',
        'deep purple': '#301934',
        'terracotta': '#E2725B',
        'dusty rose': '#BC5C73',
        'khaki': '#F0E68C',
        'copper': '#B87333',
        'pure white': '#FFFFFF',
        'bright orange': '#FFA500',
        'hot pink': '#FF69B4',
        'electric blue': '#7DF9FF',
        'lime green': '#32CD32',
        'red': '#FF0000',
        'yellow': '#FFFF00',
        'cobalt': '#0047AB',
        'neon shades': '#39FF14'
    };
    
    const swatches = document.querySelectorAll('.swatch-color');
    
    swatches.forEach(swatch => {
        const colorName = swatch.nextElementSibling?.textContent.toLowerCase();
        if (swatchColors[colorName]) {
            swatch.style.backgroundColor = swatchColors[colorName];
        }
    });
}

// Initialize color visualization when DOM is ready
document.addEventListener('DOMContentLoaded', visualizeColorPalette);

// Print functionality enhancement
window.addEventListener('beforeprint', function() {
    // Add print-specific styles
    const printStyle = document.createElement('style');
    printStyle.textContent = `
        @media print {
            .header-actions, .results-actions, .footer {
                display: none !important;
            }
            .container {
                max-width: 100% !important;
                padding: 0 !important;
            }
            body {
                background: white !important;
            }
            .results-content, .main-content {
                box-shadow: none !important;
                border: 1px solid #ccc !important;
            }
        }
    `;
    document.head.appendChild(printStyle);
});

// Accessibility improvements
function improveAccessibility() {
    // Add ARIA labels to form elements
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        const label = group.querySelector('label');
        const input = group.querySelector('input, select, textarea');
        
        if (label && input) {
            const id = input.id || `field-${index}`;
            input.id = id;
            label.setAttribute('for', id);
            
            // Add descriptive labels for screen readers
            if (input.type === 'file') {
                input.setAttribute('aria-describedby', 'file-help');
            }
        }
    });
    
    // Add skip link for keyboard navigation
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: #000;
        color: #fff;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1000;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', improveAccessibility);

// Performance monitoring
function monitorPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.fetchStart, 'ms');
            }, 0);
        });
    }
}

// Initialize performance monitoring
document.addEventListener('DOMContentLoaded', monitorPerformance);
// PropertyHub App JavaScript

// Format peso amounts
function formatPeso(amount) {
    return new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Peso formatter for templates
function peso(n) {
    return '₱' + (n || 0).toLocaleString('en-PH');
}

// UTM parameter handling
function captureUTMParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const utmSource = urlParams.get('utm_source');
    const utmCampaign = urlParams.get('utm_campaign');
    
    if (utmSource && !getCookie('utm_source')) {
        setCookie('utm_source', utmSource, 30);
    }
    if (utmCampaign && !getCookie('utm_campaign')) {
        setCookie('utm_campaign', utmCampaign, 30);
    }
}

function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = name + '=' + value + ';expires=' + expires.toUTCString() + ';path=/';
}

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

// Shortlist functionality
function addToShortlist(propertyId) {
    let shortlist = JSON.parse(localStorage.getItem('property_shortlist') || '[]');
    if (!shortlist.includes(propertyId)) {
        shortlist.push(propertyId);
        localStorage.setItem('property_shortlist', JSON.stringify(shortlist));
        updateShortlistUI();
        showNotification('Added to shortlist!');
    } else {
        showNotification('Already in shortlist!');
    }
}

function removeFromShortlist(propertyId) {
    let shortlist = JSON.parse(localStorage.getItem('property_shortlist') || '[]');
    shortlist = shortlist.filter(id => id !== propertyId);
    localStorage.setItem('property_shortlist', JSON.stringify(shortlist));
    updateShortlistUI();
    showNotification('Removed from shortlist!');
}

function updateShortlistUI() {
    const shortlist = JSON.parse(localStorage.getItem('property_shortlist') || '[]');
    const savedChip = document.querySelector('.saved-chip');
    if (savedChip) {
        savedChip.textContent = `Saved (${shortlist.length})`;
    }
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 transition-all duration-300';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Search debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Capture UTM params
    captureUTMParams();
    
    // Update shortlist UI
    updateShortlistUI();
    
    // Add CSRF token to HTMX requests
    document.body.addEventListener('htmx:configRequest', function(evt) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            evt.detail.headers['X-CSRFToken'] = csrfToken.value;
        }
    });
    
    // Handle lead form interest IDs
    const leadForm = document.querySelector('form[hx-post*="lead_submit"]');
    if (leadForm) {
        const interestIdsInput = leadForm.querySelector('#interest-ids');
        if (interestIdsInput) {
            // Get current property ID from URL or other source
            const currentPropertyId = window.location.pathname.includes('/property/') 
                ? window.location.pathname.split('/property/')[1].split('/')[0] 
                : '';
            if (currentPropertyId) {
                interestIdsInput.value = currentPropertyId;
            }
        }
    }

    // Chat composer event listener
    const chatComposer = document.querySelector('form[hx-post*="property_chat"]');
    if (chatComposer) {
        chatComposer.addEventListener('submit', function(e) {
            const messageInput = this.querySelector('input[name="message"]');
            const message = messageInput.value.trim();
            
            if (message) {
                // Add user message immediately for instant UX
                const chatStream = document.getElementById('chat-stream');
                if (chatStream) {
                    const userBubble = document.createElement('div');
                    userBubble.className = 'flex justify-end';
                    userBubble.innerHTML = `
                        <div class="bg-orange-600 text-white rounded-2xl rounded-tr-sm p-3 max-w-xs">
                            <p class="text-sm">${message}</p>
                            <p class="text-xs text-orange-100 mt-1">now</p>
                        </div>
                    `;
                    chatStream.appendChild(userBubble);
                    
                    // Scroll to bottom
                    chatStream.scrollTop = chatStream.scrollHeight;
                }
            }
        });
    }
});

// Export functions for global use
window.formatPeso = formatPeso;
window.addToShortlist = addToShortlist;
window.removeFromShortlist = removeFromShortlist;
window.updateShortlistUI = updateShortlistUI;

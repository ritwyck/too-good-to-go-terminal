// Theme functionality
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    if (body.getAttribute('data-theme') === 'light') {
        body.removeAttribute('data-theme');
        themeIcon.textContent = '☀️';
        themeText.textContent = 'LIGHT MODE';
        localStorage.setItem('theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        themeIcon.textContent = '🌙';
        themeText.textContent = 'DARK MODE';
        localStorage.setItem('theme', 'light');
    }
}

// Load saved theme on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    if (savedTheme === 'light') {
        document.body.setAttribute('data-theme', 'light');
        themeIcon.textContent = '🌙';
        themeText.textContent = 'DARK MODE';
    }
});


// Signup form handler
document.getElementById('signupForm').onsubmit = function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    const output = document.getElementById('signupOutput');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'AUTHENTICATING...';
    output.style.display = 'block';
    
    fetch('/start_auth', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const messageClass = data.success ? 'success' : 'error';
        const icon = data.success ? '✓' : '✗';
        
        document.getElementById('signupMessage').innerHTML = `
            <div class="output">
                <div class="line">
                    <span class="${messageClass}">[${icon}]</span> <span class="highlight">SYSTEM_RESPONSE:</span> ${data.message}
                </div>
            </div>
        `;
        
        if (data.success) this.reset();
        
        submitBtn.disabled = false;
        submitBtn.textContent = 'EXECUTE REGISTRATION';
    })
    .catch(error => {
        document.getElementById('signupMessage').innerHTML = `
            <div class="output">
                <div class="line">
                    <span class="error">[✗]</span> <span class="highlight">SYSTEM_ERROR:</span> ${error.message}
                </div>
            </div>
        `;
        
        submitBtn.disabled = false;
        submitBtn.textContent = 'EXECUTE REGISTRATION';
    });
};

// Deregister form handler
document.getElementById('deregisterForm').onsubmit = function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    
    if (confirm('⚠️  CONFIRM DELETION: Remove monitoring and purge all data? [y/N]')) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'PURGING DATA...';
        
        fetch('/deregister', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const messageClass = data.success ? 'success' : 'error';
            const icon = data.success ? '✓' : '✗';
            
            document.getElementById('deregisterMessage').innerHTML = `
                <div class="output">
                    <div class="line">
                        <span class="${messageClass}">[${icon}]</span> <span class="highlight">SYSTEM_RESPONSE:</span> ${data.message}
                    </div>
                </div>
            `;
            
            if (data.success) this.reset();
            
            submitBtn.disabled = false;
            submitBtn.textContent = 'EXECUTE REMOVAL';
        })
        .catch(error => {
            document.getElementById('deregisterMessage').innerHTML = `
                <div class="output">
                    <div class="line">
                        <span class="error">[✗]</span> <span class="highlight">SYSTEM_ERROR:</span> ${error.message}
                    </div>
                </div>
            `;
            
            submitBtn.disabled = false;
            submitBtn.textContent = 'EXECUTE REMOVAL';
        });
    }
};
// Handle unsubscribe form submission
document.addEventListener('DOMContentLoaded', function() {
    const deregisterForm = document.getElementById('deregisterForm');
    const deregisterMessage = document.getElementById('deregisterMessage');
    
    if (deregisterForm) {
        deregisterForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // Prevent default form submission
            
            const emailInput = document.getElementById('deregister_email');
            const email = emailInput.value.trim();
            const submitButton = this.querySelector('button[type="submit"]');
            
            if (!email) {
                showMessage('Please enter your email address', 'error');
                return;
            }
            
            // Disable button and show loading
            submitButton.disabled = true;
            submitButton.textContent = 'REMOVING...';
            showMessage('Processing removal request...', 'info');
            
            try {
                const response = await fetch('/unsubscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        email: email
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage(result.message, 'success');
                    deregisterForm.reset(); // Clear the form
                } else {
                    showMessage(result.message, 'error');
                }
                
            } catch (error) {
                console.error('Error:', error);
                showMessage('Network error. Please try again.', 'error');
            } finally {
                // Re-enable button
                submitButton.disabled = false;
                submitButton.textContent = 'EXECUTE REMOVAL';
            }
        });
    }
    
    function showMessage(message, type) {
        deregisterMessage.innerHTML = '';
        
        const line = document.createElement('div');
        line.className = 'line';
        
        let icon = '';
        let className = '';
        
        switch(type) {
            case 'success':
                icon = '✓';
                className = 'success';
                break;
            case 'error':
                icon = '✗';
                className = 'error';
                break;
            case 'info':
                icon = 'ℹ';
                className = 'warning';
                break;
            default:
                icon = '•';
                className = 'comment';
        }
        
        line.innerHTML = `<span class="${className}">[${icon}]</span> <span class="comment">SYSTEM_${type.toUpperCase()}: ${message}</span>`;
        deregisterMessage.appendChild(line);
        
        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                deregisterMessage.innerHTML = '';
            }, 5000);
        }
    }
});

// Theme functionality
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    if (body.getAttribute('data-theme') === 'light') {
        body.removeAttribute('data-theme');
        themeIcon.textContent = '🌙';
        themeText.textContent = 'LIGHT MODE';
        localStorage.setItem('theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        themeIcon.textContent = '☀️';
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
        themeIcon.textContent = '☀️';
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

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        
        event.preventDefault();
        
        const email = form.querySelector('input[name="email"]').value;
        const password = form.querySelector('input[name="password"]').value;
    
        
        fetch('http://127.0.0.1:8000/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Signin successful:', data);
            if (data.authenticated) { // Check the value of data.authenticated
                alert("Login successful redirecting ")
                window.location.href = '/'; // Redirect to index.html if signin is successful
            } else {
                alert("username or password is wrong")
                console.error('Signin failed:', data.error);
            }
        })
        .catch(error => {
            console.error('Error signing in:', error);
        });
    });
});

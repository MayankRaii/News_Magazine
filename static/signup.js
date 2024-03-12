document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        
        event.preventDefault();
        
        const username = form.querySelector('input[name="email"]').value;
        const password = form.querySelector('input[name="password"]').value;
        
        fetch('http://127.0.0.1:8000/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert("Signup successfull redirecting to signin.html");
            window.location.href = '/sign_page';
            console.log('Signup successful:', data);
            // You can perform actions here after successful signup, like redirecting to another page
        })
        .catch(error => {
            console.error('Error signing up:', error);
            // Handle errors here, like showing an error message to the user
        });
    });
});

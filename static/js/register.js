function validateForm() {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm_password').value;
    var errorMessage = document.getElementById('errorMessage');

    var passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$/;

    if (!passwordPattern.test(password)) {
        errorMessage.innerText = 'Password must be at least 8 characters, contain at least one uppercase letter, one lowercase letter, one number, and have no spaces.';
        errorMessage.classList.remove('hidden');
        return false; 
    }

    if (password !== confirmPassword) {
        errorMessage.innerText = 'Passwords do not match.';
        errorMessage.classList.remove('hidden');
        return false; 
    }

    errorMessage.classList.add('hidden');
    return true;
}
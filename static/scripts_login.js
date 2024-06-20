document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginMessage = document.getElementById('loginMessage');
    const signupMessage = document.getElementById('signupMessage');
    const showSignupFormButton = document.getElementById('showSignupForm');
    const togglePasswordButton = document.getElementById('togglePassword');
    const csrfTokenElement = document.querySelector('input[name="csrf_token"]');
    const sessionLifetimeMinutes = 15;
    const refreshInterval = 60 * 1000;
    let remainingSessionTime = sessionLifetimeMinutes * 60;
    let inactivityTimer;

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        loginMessage.innerText = 'Connexion en cours...';

        let formData = {
            username: loginForm.username.value,
            password: loginForm.password.value
        };

        if (!csrfTokenElement) {
            loginMessage.innerText = 'Erreur CSRF. Veuillez réessayer.';
            console.error('CSRF token not found');
            return;
        }
        let csrfToken = csrfTokenElement.value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.access_token) {
                    localStorage.setItem('access_token', data.access_token);
                    window.location.href = '/';
                } else {
                    loginMessage.innerText = data.error;
                }
            })
            .catch(error => {
                loginMessage.innerText = 'Erreur de connexion. Veuillez réessayer.';
                console.error('Error:', error);
            });
    });

    showSignupFormButton.addEventListener('click', function () {
        signupForm.style.display = 'block';
    });

    signupForm.addEventListener('submit', function (event) {
        event.preventDefault();
        signupMessage.innerText = 'Création de compte en cours...';

        let formData = {
            username: signupForm.signupUsername.value,
            password: signupForm.signupPassword.value,
            role: signupForm.signupRole.value
        };

        fetch('/signup', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfTokenElement.value,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    signupMessage.innerText = data.message;
                    signupForm.reset();
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                } else {
                    signupMessage.innerText = data.error;
                }
            })
            .catch(error => {
                signupMessage.innerText = 'Erreur de création de compte. Veuillez réessayer.';
                console.error('Error:', error);
            });
    });

    function startInactivityTimer() {
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(() => {
            document.getElementById("alertMessage").style.display = "block";
        }, sessionLifetimeMinutes * 60 * 1000);
    }

    function updateLastRefresh() {
        const lastRefreshElement = document.getElementById('last-refresh');
        if (lastRefreshElement) {
            const currentDate = new Date();
            lastRefreshElement.textContent = `Dernier rafraîchissement : ${currentDate.toLocaleString()}`;
        }
    }

    function updateSessionCountdown() {
        const sessionCountdownElement = document.getElementById('sessionCountdown');
        let minutes = Math.floor(remainingSessionTime / 60);
        let seconds = remainingSessionTime % 60;
        sessionCountdownElement.textContent = `Temps restant de session : ${minutes} minutes et ${seconds} secondes`;
    }

    function decrementSessionTime() {
        remainingSessionTime--;
        updateSessionCountdown();

        if (remainingSessionTime <= 0) {
            clearTimeout(inactivityTimer);
            document.getElementById("alertMessage").style.display = "block";
            return;
        }
    }

    updateLastRefresh();
    updateSessionCountdown();
    setInterval(updateLastRefresh, refreshInterval);
    startInactivityTimer();

    document.addEventListener("mousemove", startInactivityTimer);
    document.addEventListener("keydown", startInactivityTimer);

    setInterval(decrementSessionTime, 1000);

    togglePasswordButton.addEventListener('click', function () {
        const passwordField = document.getElementById('password');
        const passwordFieldType = passwordField.getAttribute('type');
        if (passwordFieldType === 'password') {
            passwordField.setAttribute('type', 'text');
            this.textContent = 'Cacher';
        } else {
            passwordField.setAttribute('type', 'password');
            this.textContent = 'Afficher';
        }
    });
});

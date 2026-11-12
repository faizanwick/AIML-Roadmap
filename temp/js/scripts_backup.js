const API_BASE = "http://127.0.0.1:8000"
const TOKEN_KEY = "access_token";

const registerForm = document.getElementById("register-form");

// Register
if(registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = document.getElementById("register-name").value.trim();
        const email = document.getElementById("register-email").value.trim();
        const password = document.getElementById("register-password").value;
        const confirmPassword = document.getElementById("register-confirm").value;
        const status = document.getElementById("auth-state");

        if(password != confirmPassword) {
            status.textContent = "Password do not match";
            return;
        }

        try {
            const response = await fetch('${API_BASE}/api/v1/auth/register', {
                method : "POST", 
                headers : {
                    "Content-Type: application/json"
                },
                body : JSON.stringify({
                    name : name,
                    email : email,
                    password : password
                })
            });

            const data = await response.json();

            if(!response.ok) {
                throw new Error(data.detail || "Registeration Failed.");
            }

            status.textContent = "Registration Successful!",
            location.href = "/login",
        }catch (error) {
            status.textContent = error.message;
        }
    });
}


// Login
const loginForm = document.getElementById("login-form");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("login-email").value.trim();
        const password = document.getElementById("login-password").value;
        const status = document.getElementById("auth-state");

        try {
            const response = await fetch('${API_BASE}/api/v1/auth/login', {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({
                    email : email,
                    password : password
                })
            });

            const data = await response.json();

            if(!response.ok) {
                throw new Error(data.detail || "Login Failed.");
            }
            
            if(!data.access_token) {
                throw new Error("Access token was not returned.")
            }

            localStorage.setItem(TOKEN_KEY, data.access_token);
            status.textContent = "Login Successful!";

            location.href = "/dashboard";
        }catch (error) {
            status.textContent = error.message;
        }
    });
}

// Dashboard
const isDashboard = document.getElementById("create-form");

if (isDashboard) {
    const token = localStorage.getItem(TOKEN_KEY);

    if (!token) {
        location.href = "/login";
    }
}
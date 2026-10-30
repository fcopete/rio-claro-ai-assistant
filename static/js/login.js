console.log(
    "LOGIN JS CARGADO"
);

/* ==========================================
   INIT
========================================== */

document.addEventListener(
    "DOMContentLoaded",
    initializeLogin
);

function initializeLogin() {

    checkExistingSession();

    const loginButton =
        document.getElementById(
            "loginButton"
        );

    const usernameInput =
        document.getElementById(
            "username"
        );

    const passwordInput =
        document.getElementById(
            "password"
        );

    if (loginButton) {

        loginButton.addEventListener(
            "click",
            login
        );
    }

    if (usernameInput) {

        usernameInput.addEventListener(
            "keydown",
            handleEnter
        );
    }

    if (passwordInput) {

        passwordInput.addEventListener(
            "keydown",
            handleEnter
        );
    }
}

/* ==========================================
   ENTER KEY
========================================== */

function handleEnter(
    event
) {

    if (
        event.key === "Enter"
    ) {

        event.preventDefault();

        login();
    }
}

/* ==========================================
   LOGIN
========================================== */

async function login() {

    const username =
        document
            .getElementById(
                "username"
            )
            ?.value
            .trim()
            .toUpperCase();

    const password =
        document
            .getElementById(
                "password"
            )
            ?.value
            .trim();

    hideLoginError();

    if (!username) {

        showLoginError(
            "Debe capturar un usuario."
        );

        return;
    }

    if (!password) {

        showLoginError(
            "Debe capturar una contraseña."
        );

        return;
    }

    try {

        const response =
            await fetch(
                "/api/auth/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            username,

                            password
                        })
                }
            );

        let data;

        try {

            data =
                await response.json();

        } catch {

            throw new Error(
                "La respuesta del servidor no es válida."
            );
        }

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Credenciales inválidas."
            );
        }

        localStorage.setItem(
            "authenticated",
            "true"
        );

        localStorage.setItem(
            "user",
            data.user
        );

        localStorage.setItem(
            "role",
            data.role
        );

        window.location.href =
            "/";

    } catch (error) {

        console.error(
            "LOGIN ERROR:",
            error
        );

        showLoginError(
            error.message
        );
    }
}

/* ==========================================
   VERIFY ACTIVE SESSION
========================================== */

async function checkExistingSession() {

    try {

        const response =
            await fetch(
                "/api/auth/me"
            );

        if (!response.ok) {

            return;
        }

        const data =
            await response.json();

        if (
            data.authenticated &&
            data.role
        ) {

            localStorage.setItem(
                "authenticated",
                "true"
            );

            localStorage.setItem(
                "user",
                data.user
            );

            localStorage.setItem(
                "role",
                data.role
            );

            window.location.href =
                "/";
        }

    } catch (error) {

        console.error(
            "SESSION CHECK ERROR:",
            error
        );
    }
}

/* ==========================================
   LOGOUT
========================================== */

async function logout() {

    try {

        await fetch(
            "/api/auth/logout",
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            error
        );
    }

    localStorage.removeItem(
        "authenticated"
    );

    localStorage.removeItem(
        "user"
    );

    localStorage.removeItem(
        "role"
    );

    window.location.href =
        "/login";
}

/* ==========================================
   UI
========================================== */

function showLoginError(
    message
) {

    const container =
        document.getElementById(
            "loginMessage"
        );

    if (!container) {
        return;
    }

    container.textContent =
        message;

    container.classList.remove(
        "d-none"
    );
}

function hideLoginError() {

    const container =
        document.getElementById(
            "loginMessage"
        );

    if (!container) {
        return;
    }

    container.textContent = "";

    container.classList.add(
        "d-none"
    );
}
console.log(
    "login.js cargado"
);

/* ==========================================
   INIT
========================================== */

document.addEventListener(
    "DOMContentLoaded",
    initializeLogin
);

function initializeLogin() {

    console.log(
        "Inicializando Login"
    );

    checkExistingSession();

    const loginButton =
        document.getElementById(
            "loginButton"
        );

    const username =
        document.getElementById(
            "username"
        );

    const password =
        document.getElementById(
            "password"
        );

    if (loginButton) {

        loginButton.addEventListener(
            "click",
            login
        );
    }

    if (username) {

        username.addEventListener(
            "keydown",
            handleEnter
        );
    }

    if (password) {

        password.addEventListener(
            "keydown",
            handleEnter
        );
    }
}

/* ==========================================
   ENTER
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
            "Debe ingresar un usuario."
        );

        return;
    }

    if (!password) {

        showLoginError(
            "Debe ingresar una contraseña."
        );

        return;
    }

    showLoader(true);

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
                "El servidor devolvió una respuesta inválida."
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

    } finally {

        showLoader(false);
    }
}

/* ==========================================
   EXISTING SESSION
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
            "SESSION ERROR:",
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

    localStorage.clear();

    window.location.href =
        "/login";
}

/* ==========================================
   UI
========================================== */

function showLoader(
    visible
) {

    const loader =
        document.getElementById(
            "loginLoader"
        );

    if (!loader) {
        return;
    }

    loader.classList.toggle(
        "hidden",
        !visible
    );
}

function showLoginError(
    message
) {

    const box =
        document.getElementById(
            "loginMessage"
        );

    if (!box) {
        return;
    }

    box.textContent =
        message;

    box.classList.remove(
        "d-none"
    );
}

function hideLoginError() {

    const box =
        document.getElementById(
            "loginMessage"
        );

    if (!box) {
        return;
    }

    box.textContent = "";

    box.classList.add(
        "d-none"
    );
}
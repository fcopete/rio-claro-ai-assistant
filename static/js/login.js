document.addEventListener(
    "DOMContentLoaded",
    initializeLogin
);

function initializeLogin() {

    checkExistingSession();

    document
        .getElementById(
            "loginButton"
        )
        ?.addEventListener(
            "click",
            login
        );

    document
        .getElementById(
            "password"
        )
        ?.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Enter"
                ) {

                    login();
                }
            }
        );
}

async function login() {

    const username =
        document
            .getElementById(
                "username"
            )
            .value
            .trim();

    const password =
        document
            .getElementById(
                "password"
            )
            .value
            .trim();

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

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Credenciales inválidas"
            );
        }

        localStorage.setItem(
            "user",
            username
        );

        localStorage.setItem(
            "role",
            data.role
        );

        localStorage.setItem(
            "authenticated",
            "true"
        );

        window.location.href =
            "/";
    }

    catch (error) {

        console.error(
            error
        );

        showLoginError(
            error.message
        );
    }
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
            data.role
        ) {

            localStorage.setItem(
                "role",
                data.role
            );

            localStorage.setItem(
                "user",
                data.user
            );

            localStorage.setItem(
                "authenticated",
                "true"
            );

            window.location.href =
                "/";
        }
    }

    catch {

        // no hacer nada
    }
}

async function logout() {

    try {

        await fetch(
            "/api/auth/logout",
            {
                method: "POST"
            }
        );

    } catch {

        // ignorar errores
    }

    localStorage.removeItem(
        "role"
    );

    localStorage.removeItem(
        "user"
    );

    localStorage.removeItem(
        "authenticated"
    );

    window.location.href =
        "/login";
}
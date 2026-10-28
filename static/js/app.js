const API = {
    HEALTH: "/health",
    CHAT: "/api/chat/ask",
    INVOICE: "/api/invoice/upload"
};

let chatCounter = 0;
let invoiceCounter = 0;

document.addEventListener(
    "DOMContentLoaded",
    initialize
);

function initialize() {

    bindEvents();

    checkHealth();
}

function bindEvents() {

    const chatButton =
        document.getElementById(
            "chatButton"
        );

    const uploadButton =
        document.getElementById(
            "uploadButton"
        );

    const question =
        document.getElementById(
            "question"
        );

    if (chatButton) {

        chatButton.addEventListener(
            "click",
            sendQuestion
        );
    }

    if (uploadButton) {

        uploadButton.addEventListener(
            "click",
            uploadInvoice
        );
    }

    if (question) {

        question.addEventListener(
            "keydown",
            handleEnter
        );
    }
}

function handleEnter(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendQuestion();
    }
}

async function checkHealth() {

    try {

        const response =
            await fetch(
                API.HEALTH
            );

        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        updateStatus(
            data.status === "healthy"
        );

    } catch (error) {

        console.error(
            "Health Check Error:",
            error
        );

        updateStatus(false);
    }
}

function updateStatus(
    healthy
) {

    const system =
        document.getElementById(
            "systemStatus"
        );

    const openAI =
        document.getElementById(
            "openAIStatus"
        );

    const documentAI =
        document.getElementById(
            "docStatus"
        );

    const metric =
        document.getElementById(
            "statusMetric"
        );

    if (healthy) {

        if (system) {
            system.textContent =
                "🟢 Operativa";
        }

        if (openAI) {
            openAI.textContent =
                "🟢 Disponible";
        }

        if (documentAI) {
            documentAI.textContent =
                "🟢 Disponible";
        }

        if (metric) {
            metric.textContent =
                "🟢 Operativo";
        }

    } else {

        if (system) {
            system.textContent =
                "🔴 Error";
        }

        if (openAI) {
            openAI.textContent =
                "🔴 Error";
        }

        if (documentAI) {
            documentAI.textContent =
                "🔴 Error";
        }

        if (metric) {
            metric.textContent =
                "🔴 Error";
        }
    }
}

async function sendQuestion() {

    const textarea =
        document.getElementById(
            "question"
        );

    if (!textarea) {
        return;
    }

    const question =
        textarea.value.trim();

    if (!question) {

        showMessage(
            "Ingrese una pregunta.",
            "error"
        );

        return;
    }

    appendMessage(
        question,
        "user"
    );

    textarea.value = "";

    toggleLoader(
        "chatLoader",
        true
    );

    try {

        const response =
            await fetch(
                API.CHAT,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            question
                        })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Error del servidor"
            );
        }

        appendMessage(
            data.answer ||
            "Sin respuesta.",
            "assistant"
        );

        chatCounter++;

        const counter =
            document.getElementById(
                "chatCounter"
            );

        if (counter) {

            counter.textContent =
                chatCounter;
        }

    } catch (error) {

        console.error(
            "Chat Error:",
            error
        );

        appendMessage(
            error.message ||
            "Error al conectar con el asistente.",
            "assistant"
        );

        showMessage(
            error.message ||
            "Error al conectar.",
            "error"
        );

    } finally {

        toggleLoader(
            "chatLoader",
            false
        );
    }
}

async function uploadInvoice() {

    const fileInput =
        document.getElementById(
            "invoiceFile"
        );

    if (
        !fileInput ||
        !fileInput.files.length
    ) {

        showMessage(
            "Seleccione una factura.",
            "error"
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    toggleLoader(
        "invoiceLoader",
        true
    );

    try {

        const response =
            await fetch(
                API.INVOICE,
                {
                    method: "POST",
                    body: formData
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Error procesando factura"
            );
        }

        const output =
            document.getElementById(
                "invoiceResult"
            );

        if (output) {

            output.textContent =
                JSON.stringify(
                    data.data,
                    null,
                    2
                );
        }

        invoiceCounter++;

        const counter =
            document.getElementById(
                "invoiceCounter"
            );

        if (counter) {

            counter.textContent =
                invoiceCounter;
        }

        showMessage(
            "Factura procesada correctamente.",
            "success"
        );

    } catch (error) {

        console.error(
            "Invoice Error:",
            error
        );

        const output =
            document.getElementById(
                "invoiceResult"
            );

        if (output) {

            output.textContent =
                error.message;
        }

        showMessage(
            error.message ||
            "Error procesando factura.",
            "error"
        );

    } finally {

        toggleLoader(
            "invoiceLoader",
            false
        );
    }
}

function appendMessage(
    text,
    type
) {

    const container =
        document.getElementById(
            "chatContainer"
        );

    if (!container) {
        return;
    }

    const item =
        document.createElement(
            "div"
        );

    item.className =
        type === "user"
            ? "user-message"
            : "ai-message";

    item.textContent =
        text;

    container.appendChild(
        item
    );

    container.scrollTop =
        container.scrollHeight;
}

function toggleLoader(
    id,
    visible
) {

    const loader =
        document.getElementById(
            id
        );

    if (!loader) {
        return;
    }

    loader.classList.toggle(
        "hidden",
        !visible
    );
}

function showMessage(
    message,
    type = "error"
) {

    const box =
        document.getElementById(
            "messageBox"
        );

    if (!box) {
        return;
    }

    box.className = type;

    box.textContent =
        message;

    box.classList.remove(
        "hidden"
    );

    setTimeout(
        () => {

            box.classList.add(
                "hidden"
            );

        },
        5000
    );
}
const RioClaroApp = {

    API: {

        HEALTH:
            "/health",

        CHAT:
            "/api/chat/ask",

        INVOICE:
            "/api/invoice/upload",

        INVOICE_ANALYZE:
            "/api/invoice/analyze",

        EXECUTIVE_SUMMARY:
            "/api/executive/sales-summary",

        CUSTOMER_PENDING:
            "/api/customer/pending",

        ADMIN_STATUS:
            "/api/admin/status",

        SAMPLE_ALL:
            "/api/sample/all",

        SAMPLE_DASHBOARD:
            "/api/sample/dashboard",

        SAMPLE_SALES:
            "/api/sample/sales",

        SAMPLE_CUSTOMERS:
            "/api/sample/customers",

        SAMPLE_WAREHOUSE:
            "/api/sample/warehouse",

        SAMPLE_INVOICES:
            "/api/sample/invoices",

        SAMPLE_ADMIN:
            "/api/sample/admin"
    },

    MAX_HISTORY: 20,

    MAX_FILE_SIZE:
        10 * 1024 * 1024,

    chatCounter: 0,

    invoiceCounter: 0,

    conversationHistory: [],

    initialize() {

        if (
            !this.checkAuthentication()
        ) {

            return;
        }

        this.bindEvents();

        this.checkHealth();

        this.loadDashboardData();

        this.loadExecutiveSummary();

        this.loadCustomerMetrics();

        this.loadWarehouseData();

        this.loadAdminStatus();

        this.applyRole();
    },

    checkAuthentication() {

        const authenticated =
            localStorage.getItem(
                "authenticated"
            );

        if (
            authenticated !== "true"
        ) {

            if (
                window.location.pathname !==
                "/login"
            ) {

                window.location.href =
                    "/login";
            }

            return false;
        }

        return true;
    },

    logout() {

        localStorage.clear();

        window.location.href =
            "/login";
    },

    applyRole() {

        const role =
            localStorage.getItem(
                "role"
            );

        if (!role) {
            return;
        }

        document
            .querySelectorAll(
                "[data-role]"
            )
            .forEach(el => {

                el.style.display =
                    "none";
            });

        document
            .querySelectorAll(
                `[data-role="${role}"]`
            )
            .forEach(el => {

                el.style.display =
                    "block";
            });
    },

    bindEvents() {

        document
            .getElementById(
                "chatButton"
            )
            ?.addEventListener(
                "click",
                () =>
                    this.sendQuestion()
            );

        document
            .getElementById(
                "uploadButton"
            )
            ?.addEventListener(
                "click",
                () =>
                    this.uploadInvoice()
            );

        document
            .getElementById(
                "speechButton"
            )
            ?.addEventListener(
                "click",
                () =>
                    this.startSpeech()
            );

        document
            .getElementById(
                "question"
            )
            ?.addEventListener(
                "keydown",
                event => {

                    if (

                        event.key ===
                            "Enter" &&

                        !event.shiftKey

                    ) {

                        event.preventDefault();

                        this.sendQuestion();
                    }
                }
            );
    },

    async checkHealth() {

        try {

            const response =
                await fetch(
                    this.API.HEALTH
                );

            const data =
                await response.json();

            this.updateStatus(

                response.ok &&

                data.status ===
                    "healthy"
            );

        } catch {

            this.updateStatus(
                false
            );
        }
    },

    updateStatus(ok) {

        const value =
            ok
                ? "🟢 Disponible"
                : "🔴 Error";

        this.setText(
            "openAIStatus",
            value
        );

        this.setText(
            "openAIStatusLabel",
            value
        );

        this.setText(
            "docStatus",
            value
        );

        this.setText(
            "systemStatus",
            ok
                ? "🟢 Operativa"
                : "🔴 Error"
        );

        this.setText(
            "statusMetric",
            ok
                ? "🟢 Operativo"
                : "🔴 Error"
        );
    },

    async sendQuestion() {

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

            this.showMessage(
                "Ingrese una pregunta.",
                "error"
            );

            return;
        }

        this.appendMessage(
            question,
            "user"
        );

        this.conversationHistory.push({

            role:
                "user",

            content:
                question
        });

        textarea.value = "";

        this.toggleLoader(
            "chatLoader",
            true
        );

        try {

            const response =
                await fetch(
                    this.API.CHAT,
                    {
                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                question,

                                history:
                                    this.conversationHistory
                            })
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.message ||
                    "Error IA"
                );
            }

            this.appendMessage(

                data.answer ||
                "Sin respuesta.",

                "assistant"
            );

            this.conversationHistory.push({

                role:
                    "assistant",

                content:
                    data.answer
            });

            this.trimHistory();

            this.chatCounter++;

            this.setText(
                "chatCounter",
                this.chatCounter
            );

        } catch (error) {

            this.showMessage(
                error.message,
                "error"
            );

        } finally {

            this.toggleLoader(
                "chatLoader",
                false
            );
        }
    },

    trimHistory() {

        if (

            this.conversationHistory.length >

            this.MAX_HISTORY

        ) {

            this.conversationHistory =
                this.conversationHistory.slice(
                    -this.MAX_HISTORY
                );
        }
    },

    async uploadInvoice() {

        const input =
            document.getElementById(
                "invoiceFile"
            );

        if (
            !input ||
            !input.files.length
        ) {

            this.showMessage(
                "Seleccione una factura.",
                "error"
            );

            return;
        }

        const file =
            input.files[0];

        if (
            file.size >
            this.MAX_FILE_SIZE
        ) {

            this.showMessage(
                "Archivo superior a 10 MB.",
                "error"
            );

            return;
        }

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        this.toggleLoader(
            "invoiceLoader",
            true
        );

        try {

            const response =
                await fetch(
                    this.API.INVOICE,
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const data =
                await response.json();

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

            await this.analyzeInvoiceWithAI(
                data.data
            );

        } catch (error) {

            this.showMessage(
                error.message,
                "error"
            );

        } finally {

            this.toggleLoader(
                "invoiceLoader",
                false
            );
        }
    },

    async analyzeInvoiceWithAI(
        invoiceData
    ) {

        try {

            const response =
                await fetch(
                    this.API
                        .INVOICE_ANALYZE,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                invoice:
                                    invoiceData,

                                history:
                                    this.conversationHistory
                            })
                    }
                );

            const data =
                await response.json();

            this.renderInvoiceAnalysis(
                data.analysis ||
                "Sin análisis"
            );

        } catch (error) {

            console.error(
                error
            );
        }
    },

    renderInvoiceAnalysis(
        text
    ) {

        const analysis =
            document.getElementById(
                "invoiceAnalysis"
            );

        if (!analysis) {
            return;
        }

        analysis.innerHTML = `

            <div class="analysis-title">

                Informe IA

            </div>

            <div class="analysis-section">

                ${String(text)
                    .replace(
                        /\n/g,
                        "<br>"
                    )}

            </div>
        `;
    },

    async loadDashboardData() {

        try {

            const response =
                await fetch(
                    this.API
                        .SAMPLE_DASHBOARD
                );

            const data =
                await response.json();

            this.setText(

                "invoiceCounter",

                data.facturas_procesadas || 0
            );

            this.setText(

                "chatCounter",

                data.consultas_ia || 0
            );

        } catch {}
    },

    async loadExecutiveSummary() {

        try {

            const response =
                await fetch(
                    this.API
                        .SAMPLE_SALES
                );

            const data =
                await response.json();

            const value =
                "$" +
                Number(
                    data.total_sales || 0
                ).toLocaleString();

            this.setText(
                "salesMetric",
                value
            );

            this.setText(
                "salesMetricReport",
                value
            );

        } catch {}
    },

    async loadCustomerMetrics() {

        try {

            const response =
                await fetch(
                    this.API
                        .SAMPLE_CUSTOMERS
                );

            const data =
                await response.json();

            this.setText(
                "pendingCustomers",
                data.pending_cases || 0
            );

        } catch {}
    },

    async loadWarehouseData() {

        try {

            const response =
                await fetch(
                    this.API
                        .SAMPLE_WAREHOUSE
                );

            const data =
                await response.json();

            console.log(
                "Warehouse",
                data
            );

        } catch {}
    },

    async loadAdminStatus() {

        try {

            const response =
                await fetch(
                    this.API
                        .SAMPLE_ADMIN
                );

            const data =
                await response.json();

            console.log(
                data
            );

        } catch {}
    },

    startSpeech() {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (
            !SpeechRecognition
        ) {

            this.showMessage(
                "Reconocimiento de voz no soportado.",
                "error"
            );

            return;
        }

        const recognition =
            new SpeechRecognition();

        recognition.lang =
            "es-MX";

        recognition.start();

        recognition.onresult =
            event => {

                document
                    .getElementById(
                        "question"
                    )
                    .value =
                        event.results[0][0]
                        .transcript;
            };
    },

    appendMessage(
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

        const div =
            document.createElement(
                "div"
            );

        div.className =
            type === "user"
                ? "user-message"
                : "ai-message";

        div.innerHTML =
            String(text)
                .replace(
                    /\n/g,
                    "<br>"
                );

        container.appendChild(
            div );

        container.scrollTop =
            container.scrollHeight;
    },

    toggleLoader(
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
    },

    showMessage(
        message,
        type
    ) {

        const box =
            document.getElementById(
                "messageBox"
            );

        if (!box) {
            return;
        }

        box.className =
            `toast-message ${type}`;

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
    },

    setText(
        id,
        value
    ) {

        const element =
            document.getElementById(
                id
            );

        if (element) {

            element.textContent =
                value;
        }
    }
};

document.addEventListener(
    "DOMContentLoaded",
    () =>
        RioClaroApp.initialize()
);
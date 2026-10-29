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

        console.log(
            "Rio Claro AI Assistant iniciado"
        );

        this.bindEvents();

        this.checkHealth();

        this.loadDashboardData();

        this.loadExecutiveSummary();

        this.loadCustomerMetrics();

        this.loadWarehouseData();

        this.loadAdminStatus();
    },

    bindEvents() {

        document
            .getElementById(
                "chatButton"
            )
            ?.addEventListener(
                "click",
                () => this.sendQuestion()
            );

        document
            .getElementById(
                "uploadButton"
            )
            ?.addEventListener(
                "click",
                () => this.uploadInvoice()
            );

        document
            .getElementById(
                "speechButton"
            )
            ?.addEventListener(
                "click",
                () => this.startSpeech()
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

        this.activateMenu();
    },

    activateMenu() {

        document
            .querySelectorAll(
                ".sidebar a"
            )
            .forEach(link => {

                link.addEventListener(
                    "click",

                    function () {

                        document
                            .querySelectorAll(
                                ".sidebar a"
                            )
                            .forEach(item =>
                                item.classList.remove(
                                    "active"
                                )
                            );

                        this.classList.add(
                            "active"
                        );
                    }
                );
            });
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

    updateStatus(
        healthy
    ) {

        const state =
            healthy
                ? "🟢 Disponible"
                : "🔴 Error";

        this.setText(
            "openAIStatus",
            state
        );

        this.setText(
            "openAIStatusLabel",
            state
        );

        this.setText(
            "docStatus",
            state
        );

        this.setText(
            "systemStatus",
            healthy
                ? "🟢 Operativa"
                : "🔴 Error"
        );

        this.setText(
            "statusMetric",
            healthy
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

            role: "user",

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
                    "Error del servidor."
                );
            }

            const answer =
                data.answer ||
                "Sin respuesta.";

            this.appendMessage(
                answer,
                "assistant"
            );

            this.conversationHistory.push({

                role:
                    "assistant",

                content:
                    answer
            });

            this.trimHistory();

            this.chatCounter++;

            this.setText(
                "chatCounter",
                this.chatCounter
            );

        } catch (error) {

            console.error(
                error
            );

            this.appendMessage(
                error.message,
                "assistant"
            );

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

            if (!response.ok) {

                throw new Error(
                    data.message ||
                    "Error procesando factura."
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

            this.invoiceCounter++;

            this.setText(
                "invoiceCounter",
                this.invoiceCounter
            );

            await this.analyzeInvoiceWithAI(
                data.data
            );

            this.showMessage(
                "Factura procesada correctamente.",
                "success"
            );

        } catch (error) {

            console.error(
                error
            );

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

        const analysis =
            document.getElementById(
                "invoiceAnalysis"
            );

        try {

            if (analysis) {

                analysis.innerHTML = `
                    <div class="loader"></div>
                    <div class="analysis-section">
                        Analizando factura con GPT‑5.4‑mini...
                    </div>
                `;
            }

            const response =
                await fetch(
                    this.API.INVOICE_ANALYZE,
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

            if (!response.ok) {

                throw new Error(
                    data.message ||
                    "Error IA"
                );
            }

            this.renderInvoiceAnalysis(
                data.analysis ||
                "Sin análisis disponible."
            );

        } catch (error) {

            console.error(
                error
            );

            if (analysis) {

                analysis.innerHTML = `
                    <div class="analysis-risk-high">
                        Error
                    </div>
                    <div class="analysis-section">
                        ${error.message}
                    </div>
                `;
            }
        }
    },

    renderInvoiceAnalysis(
        text
    ) {

        const container =
            document.getElementById(
                "invoiceAnalysis"
            );

        if (!container) {
            return;
        }

        let riskClass =
            "analysis-risk-low";

        const lower =
            String(text)
                .toLowerCase();

        if (
            lower.includes(
                "riesgo alto"
            )
        ) {

            riskClass =
                "analysis-risk-high";
        }

        else if (
            lower.includes(
                "riesgo medio"
            )
        ) {

            riskClass =
                "analysis-risk-medium";
        }

        container.innerHTML = `

            <div class="analysis-title">

                Informe IA

            </div>

            <div class="${riskClass}">

                Resultado Analizado

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
                    this.API.SAMPLE_DASHBOARD
                );

            const data =
                await response.json();

            if (
                data.facturas_procesadas
            ) {

                this.setText(
                    "invoiceCounter",
                    data.facturas_procesadas
                );
            }

            if (
                data.consultas_ia
            ) {

                this.setText(
                    "chatCounter",
                    data.consultas_ia
                );
            }

        } catch (error) {

            console.error(
                error
            );
        }
    },

    async loadExecutiveSummary() {

        try {

            const response =
                await fetch(
                    this.API.SAMPLE_SALES
                );

            const data =
                await response.json();

            if (
                !data.total_sales
            ) {
                return;
            }

            const value =
                "$" +
                Number(
                    data.total_sales
                ).toLocaleString();

            this.setText(
                "salesMetric",
                value
            );

            this.setText(
                "salesMetricReport",
                value
            );

        } catch (error) {

            console.error(
                error
            );
        }
    },

    async loadCustomerMetrics() {

        try {

            const response =
                await fetch(
                    this.API.SAMPLE_CUSTOMERS
                );

            const data =
                await response.json();

            this.setText(
                "pendingCustomers",
                data.pending_cases || 0
            );

        } catch (error) {

            console.error(
                error
            );
        }
    },

    async loadWarehouseData() {

        try {

            const response =
                await fetch(
                    this.API.SAMPLE_WAREHOUSE
                );

            const data =
                await response.json();

            console.log(
                "Warehouse:",
                data
            );

        } catch (error) {

            console.error(
                error
            );
        }
    },

    async loadAdminStatus() {

        try {

            const response =
                await fetch(
                    this.API.SAMPLE_ADMIN
                );

            const data =
                await response.json();

            console.log(
                "Admin Status:",
                data
            );

        } catch (error) {

            console.error(
                error
            );
        }
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

        try {

            recognition.start();

        } catch {

            this.showMessage(
                "No fue posible iniciar la captura de voz.",
                "error"
            );

            return;
        }

        recognition.onresult =
            event => {

                const transcript =
                    event.results[0][0]
                    .transcript;

                const textarea =
                    document.getElementById(
                        "question"
                    );

                if (textarea) {

                    textarea.value =
                        transcript;
                }
            };

        recognition.onerror =
            () => {

                this.showMessage(
                    "Error en reconocimiento de voz.",
                    "error"
                );
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

        const item =
            document.createElement(
                "div"
            );

        item.className =
            type === "user"
                ? "user-message"
                : "ai-message";

        item.innerHTML =
            String(text)
                .replace(
                    /\n/g,
                    "<br>"
                );

        container.appendChild(
            item
        );

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
        type = "error"
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
    () => RioClaroApp.initialize()
);
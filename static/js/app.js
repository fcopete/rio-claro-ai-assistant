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
            "/api/admin/status"
    },

    MAX_HISTORY: 20,

    chatCounter: 0,

    invoiceCounter: 0,

    conversationHistory: [],

    initialize() {

        console.log(
            "Rio Claro AI Assistant iniciado"
        );

        this.bindEvents();

        this.checkHealth();

        this.loadExecutiveSummary();

        this.loadCustomerMetrics();

        this.loadAdminStatus();
    },

    bindEvents() {

        document
            .getElementById("chatButton")
            ?.addEventListener(
                "click",
                () => this.sendQuestion()
            );

        document
            .getElementById("uploadButton")
            ?.addEventListener(
                "click",
                () => this.uploadInvoice()
            );

        document
            .getElementById("speechButton")
            ?.addEventListener(
                "click",
                () => this.startSpeech()
            );

        document
            .getElementById("question")
            ?.addEventListener(
                "keydown",
                e => {

                    if (
                        e.key === "Enter" &&
                        !e.shiftKey
                    ) {

                        e.preventDefault();

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

    updateStatus(
        healthy
    ) {

        const values =
            healthy
            ? {
                text:
                    "🟢 Disponible",
                status:
                    "🟢 Operativa",
                metric:
                    "🟢 Operativo"
            }
            : {
                text:
                    "🔴 Error",
                status:
                    "🔴 Error",
                metric:
                    "🔴 Error"
            };

        this.setText(
            "openAIStatus",
            values.text
        );

        this.setText(
            "docStatus",
            values.text
        );

        this.setText(
            "systemStatus",
            values.status
        );

        this.setText(
            "statusMetric",
            values.metric
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
                "Ingrese una pregunta",
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

            content: question
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
                data.answer,
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
                "Seleccione una factura",
                "error"
            );

            return;
        }

        const formData =
            new FormData();

        formData.append(
            "file",
            input.files[0]
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
                    data.message
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
                            invoiceData
                        })
                    }
                );

            const data =
                await response.json();

            this.renderInvoiceAnalysis(
                data.analysis
            );

        } catch (error) {

            console.error(error);
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
                ${String(text || "")
                    .replace(/\n/g,"<br>")
                }
            </div>
        `;
    },

    async loadExecutiveSummary() {

        try {

            const response =
                await fetch(
                    this.API
                        .EXECUTIVE_SUMMARY
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

        } catch (error) {

            console.error(error);
        }
    },

    async loadCustomerMetrics() {

        try {

            const response =
                await fetch(
                    this.API
                        .CUSTOMER_PENDING
                );

            const data =
                await response.json();

            this.setText(
                "pendingCustomers",
                data.pending_cases || 0
            );

        } catch (error) {

            console.error(error);
        }
    },

    async loadAdminStatus() {

        try {

            const response =
                await fetch(
                    this.API.ADMIN_STATUS
                );

            const data =
                await response.json();

            console.log(
                "Admin Status:",
                data
            );

        } catch (error) {

            console.error(error);
        }
    },

    startSpeech() {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {

            this.showMessage(
                "Reconocimiento de voz no disponible",
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

                const text =
                    event.results[0][0]
                    .transcript;

                const textarea =
                    document.getElementById(
                        "question"
                    );

                if (textarea) {

                    textarea.value =
                        text;
                }
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
            document.getElementById(id);

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
    }
};

document.addEventListener(
    "DOMContentLoaded",
    () =>
        RioClaroApp.initialize()
);
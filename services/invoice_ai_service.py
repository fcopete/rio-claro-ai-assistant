from services.chat_service import ask_chatbot
def analyze_invoice_risk(invoice_data, history=None):
    prompt=f"Analiza la factura y genera resumen ejecutivo, nivel de riesgo, duplicidad, inconsistencias y recomendacion. Factura: {invoice_data}"
    return ask_chatbot(prompt, history)

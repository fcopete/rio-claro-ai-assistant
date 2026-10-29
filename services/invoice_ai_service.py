from services.chat_service import ask_chatbot

def analyze_invoice_risk(invoice_data, history=None):
    prompt=f"""Eres un auditor financiero. Analiza la factura y genera resumen ejecutivo, nivel de riesgo, inconsistencias y recomendación.

Factura:
{invoice_data}"""
    return ask_chatbot(prompt, history)

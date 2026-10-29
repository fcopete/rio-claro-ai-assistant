from services.chat_service import ask_chatbot

def analyze_invoice_risk(invoice_data):
    prompt=f"""Revisa la factura.

Detecta:
- montos anómalos
- proveedor sospechoso
- pago duplicado

Factura:

{invoice_data}
"""
    return ask_chatbot(prompt)

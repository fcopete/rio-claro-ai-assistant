from flask import Blueprint, request, jsonify
from services.chat_service import ask_chatbot
chat_bp=Blueprint("chat",__name__)
@chat_bp.route("/ask",methods=["POST"])
def ask():
    payload=request.get_json()
    question=payload.get("question","").strip()
    history=payload.get("history",[])
    answer=ask_chatbot(question,history)
    return jsonify({"success":True,"answer":answer})
